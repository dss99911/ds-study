import awswrangler as wr
import getpass
import boto3

subnet = getpass.getpass()
#%% create cluster
cluster_id = wr.emr.create_cluster(subnet)

#%% create cluster sample
import awswrangler as wr

steps = [wr.emr.build_spark_step(path="submit_script",
                                 name="name",
                                 docker_image="docker-image"
                                 )
         ]
class_name = "class_name"
jar_path = f"s3://some.jar"
p1 = "param1"
p2 = "param2"
steps = [wr.emr.build_spark_step(path=f"--driver-java-options -Dconfig.resource=application.conf --class {class_name} {jar_path} {p1} {p2}",
                                 name="name",
                                 )
         ]

cluster_id = wr.emr.create_cluster(subnet_id="subnet_id",
                                   docker=True,
                                   cluster_name="name",
                                   logging_s3_path="s3://aad",
                                   emr_release="emr-6.4.0",
                                   instance_type_master="m4.large",
                                   instance_type_core="instance_type",
                                   instance_type_task="instance_type",
                                   instance_ebs_size_master=64,
                                   instance_ebs_size_core=64,
                                   instance_ebs_size_task=64,
                                   instance_num_on_demand_core=1,
                                   applications=["Hadoop", "Spark", "Hive", "Ganglia"],
                                   maximize_resource_allocation=True,
                                   keep_cluster_alive_when_no_steps=False,
                                   steps=steps,
                                   key_pair_name="hyun",
                                   security_groups_master_additional=["ssh_security_group"],
                                   debugging=False,
                                   spark_defaults={
                                       "spark.executor.defaultJavaOptions": "-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:OnOutOfMemoryError='kill -9 %p' -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=70 -XX:MaxHeapFreeRatio=70 -XX:+CMSClassUnloadingEnabled",
                                       "spark.driver.defaultJavaOptions": "-XX:OnOutOfMemoryError='kill -9 %p' -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=70 -XX:MaxHeapFreeRatio=70 -XX:+CMSClassUnloadingEnabled"
                                   }
                                   )

#%% add step
step_id = wr.emr.submit_step(cluster_id, command=f"spark-submit s3://hyun.test/test.py")

#%% wait step
while wr.emr.get_step_state(cluster_id, step_id) != "COMPLETED":
    pass


#%% check cluster state
import time

def check_status(cluster_id):
    while True:
        time.sleep(30)
        status = wr.emr.get_cluster_state(cluster_id)
        if status not in ["STARTING", "BOOTSTRAPPING", "RUNNING"]:
            break
    # some cases, cluster state is terminated, but step is failed.
    # so, need to check all steps is completed or not
    return check_all_steps_completed(cluster_id)


def check_all_steps_completed(cluster_id):
    client = boto3.client('emr')
    states = set([s["Status"]["State"] for s in client.list_steps(ClusterId=cluster_id)["Steps"]])
    return states == set(['COMPLETED'])


#%% terminate cluster
wr.emr.terminate_cluster(cluster_id)

#%% check cluster
def emr_instance_running(name):
    client = boto3.client('emr')
    cluster_response = client.list_clusters(
        ClusterStates=[
            'STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING', 'TERMINATING',
        ]
    )

    if cluster_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        for c in cluster_response["Clusters"]:
            if c["Name"] == name:
                return True
        return False
    else:
        raise Exception(f"response error : {cluster_response}")

#%% use docker by ECR
# https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/016%20-%20EMR%20%26%20Docker.ipynb
# python library등을 emr에서 사용하려면, py-files 등을 사용하면, 번거로움이 많음
# docker에 python library를 설치해서 돌림.
# cluster를 생성할 때, docker 사용을 enabled시켜줘야 함
# cluster mode로만 해야지 되었던 것 같음. client mode에선 사용 못함
