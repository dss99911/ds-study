from common import *
# from util.common import *
import awswrangler as wr
import boto3
import time
from cheapest_spot_instance_retriever import get_cheapest_instance_types
# from util.cheapest_spot_instance_retriever import get_cheapest_instance_types

_region = "ap-south-1"
_emr_release_ver = "emr-6.6.0"
_subnet_id = "subnet-{1234}"
_key_pair_name = "{key-pair}"
_tags = {"Role": "ds", "Service": "sagemaker", "Application": "emr"}
_applications = ["Hadoop", "Spark", "Hive", "Ganglia"]
_cheapest_data_s3_path = "s3://{bucket}/{key}"
boto3.setup_default_session(region_name=_region)


def run_emr_spark_job(
        name: str,
        steps: list,
        logging_s3_path: str = None,
        instance_type_master="m5.2xlarge",
        instance_type_core="m5.2xlarge",
        instance_type_task="m5.2xlarge",
        instance_ebs_size_master=128,
        instance_ebs_size_core=128,
        instance_ebs_size_task=128,
        instance_num_on_demand_core=50,
        spark_conf={}
):
    cluster_id = wr.emr.create_cluster(
        subnet_id=_subnet_id,
        cluster_name=name,
        logging_s3_path=logging_s3_path,
        emr_release=_emr_release_ver,
        instance_type_master=instance_type_master,
        instance_type_core=instance_type_core,
        instance_type_task=instance_type_task,
        instance_ebs_size_master=instance_ebs_size_master,
        instance_ebs_size_core=instance_ebs_size_core,
        instance_ebs_size_task=instance_ebs_size_task,
        instance_num_on_demand_core=instance_num_on_demand_core,
        applications=_applications,
        maximize_resource_allocation=True,
        keep_cluster_alive_when_no_steps=False,
        steps=steps,
        key_pair_name=_key_pair_name,
        debugging=False,
        tags=_tags,
        spark_defaults=spark_conf
    )
    log_info(cluster_id)

    if not check_emr_cluster_status(cluster_id):
        raise Exception(f"cluster {cluster_id} is failed")


def create_emr_jar_step(jar_path, class_name, resource="application.conf", args=[]):
    return wr.emr.build_spark_step(
        path=f"{f'--driver-java-options -Dconfig.resource={resource} ' if resource else ''}--class {class_name} {jar_path} {' '.join(args)}",
        name=f"{class_name}"
    )


def create_emr_pyspark_step(schema_path, py_path: str, args=[]):
    py_files = ",".join([get_pipeline_zip_url(schema_path)])

    return wr.emr.build_spark_step(
        path=f"--py-files {py_files} {py_path} {' '.join(args)}",
        name=f"{py_path.split('/')[-1].split('.py')[0]}",
    )


def run_emr_spark_job_fleet(
        name: str,
        steps: list,
        instance_fleets,
        maximum_on_demand_capacity_units=10,
        maximum_capacity_units=200,
        logging_s3_path=None,
        spark_conf={}
):
    connection = boto3.client('emr')

    response = connection.run_job_flow(
        Name=name,
        LogUri=logging_s3_path,
        ReleaseLabel=_emr_release_ver,
        Applications=[{'Name': app} for app in _applications],
        Instances={
            'InstanceFleets': instance_fleets,
            'Ec2KeyName': _key_pair_name,
            'KeepJobFlowAliveWhenNoSteps': False,
            'Ec2SubnetId': _subnet_id,
        },
        ManagedScalingPolicy={
            "ComputeLimits": {
                "MaximumOnDemandCapacityUnits": maximum_on_demand_capacity_units,
                "UnitType": "InstanceFleetUnits",
                "MaximumCapacityUnits": maximum_capacity_units,
                "MinimumCapacityUnits": 3,
                "MaximumCoreCapacityUnits": 1
            }
        },
        ScaleDownBehavior='TERMINATE_AT_TASK_COMPLETION',
        Configurations=[
            {
                "Classification": "hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
                },
                "Configurations": []
            },
            {
                "Classification": "spark-hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
                },
                "Configurations": []
            },
            {
                "Classification": "spark-defaults",
                "Properties": spark_conf
            }
        ],
        Steps=steps,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole',
        Tags=[{'Key': k, 'Value': v} for k, v in _tags.items()]
    )
    cluster_id = response['JobFlowId']
    log_info(cluster_id)

    if not check_emr_cluster_status(cluster_id):
        raise Exception(f"cluster {cluster_id} is failed")


def create_emr_jar_step_fleet(jar_path, class_name, resource="application.conf", args=[]):
    return build_spark_step_fleet(
        path=f"{f'--driver-java-options -Dconfig.resource={resource} ' if resource else ''}--class {class_name} {jar_path} {' '.join(args)}",
        name=f"{class_name}"
    )


def build_spark_step_fleet(
        name,
        path: str,
):
    return {
        'Name': name,
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                *path.split(" ")
            ]

        }
    }


def get_cheapest_spot_instance_fleets(
        available_categories=["m"],
        max_frequency=1,
        min_ram=3,
        min_cores=4,
        max_cores=32,
        min_saving_ratio=70,
        limit=8,
        master_instance_type="m5.xlarge",
        core_instance_type="m5.xlarge",
        ebs_size=128,
        bid_percent=50
):
    master_fleet = {
        "Name": "Masterfleet",
        "InstanceFleetType": "MASTER",
        "TargetOnDemandCapacity": 1,
        "InstanceTypeConfigs": [
            {
                "WeightedCapacity": 1,
                "EbsConfiguration": {"EbsBlockDeviceConfigs": [{"VolumeSpecification": {"SizeInGB": ebs_size, "VolumeType": "gp2"}, "VolumesPerInstance": 1}]},
                "InstanceType": master_instance_type
            }
        ],
    }

    core_fleet = {
        "Name": "Corefleet",
        "InstanceFleetType": "CORE",
        "TargetOnDemandCapacity": 1,
        "InstanceTypeConfigs": [
            {
                "WeightedCapacity": 1,
                "EbsConfiguration": {"EbsBlockDeviceConfigs": [{"VolumeSpecification": {"SizeInGB": ebs_size, "VolumeType": "gp2"}, "VolumesPerInstance": 1}]},
                "InstanceType": core_instance_type}
        ]
    }
    try:
        task_df = get_cheapest_instance_types(
            region=_region,
            available_categories=available_categories,
            max_frequency=max_frequency,
            min_ram=min_ram,
            min_cores=min_cores,
            max_cores=max_cores,
            min_saving_ratio=min_saving_ratio,
            limit=limit
        )
        wr.s3.to_csv(task_df, _cheapest_data_s3_path)
    except Exception as e:
        log_exception(e)
        task_df = wr.s3.read_csv(_cheapest_data_s3_path).set_index("instance_type")


    def get_task_instance_dict(instance_row):
        instance_type = instance_row[0]
        weight = int(instance_row[1]["cores"] / 4)
        return {
            "WeightedCapacity": weight,
            "EbsConfiguration": {
                "EbsBlockDeviceConfigs": [
                    {
                        "VolumeSpecification": {
                            "SizeInGB": ebs_size,
                            "VolumeType": "gp2"},
                        "VolumesPerInstance": weight}]},
            "BidPriceAsPercentageOfOnDemandPrice": bid_percent,
            "InstanceType": instance_type
        }

    task_fleet = {
        "Name": "Taskfleet",
        "InstanceFleetType": "TASK",
        "TargetOnDemandCapacity": 0, "TargetSpotCapacity": 1,
        "LaunchSpecifications": {
            "SpotSpecification": {"TimeoutDurationMinutes": 10, "AllocationStrategy": "CAPACITY_OPTIMIZED",
                                  "TimeoutAction": "SWITCH_TO_ON_DEMAND"}
        },
        "InstanceTypeConfigs": [get_task_instance_dict(row) for row in task_df.iterrows()],
    }

    return [master_fleet, core_fleet, task_fleet]


def check_emr_cluster_status(cluster_id):

    while True:
        time.sleep(30)
        status = wr.emr.get_cluster_state(cluster_id)
        log_info(cluster_id, status)
        if status not in ["STARTING", "BOOTSTRAPPING", "RUNNING"]:
            break
    # some cases, cluster state is terminated, but step is failed.
    # so, need to check all steps is completed or not
    return check_emr_all_steps_completed(cluster_id)


def check_emr_all_steps_completed(cluster_id):
    client = boto3.client('emr')
    states = set([s["Status"]["State"] for s in client.list_steps(ClusterId=cluster_id)["Steps"]])
    return states == {'COMPLETED'}
