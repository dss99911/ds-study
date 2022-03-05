from util.common import *
import joblib
import pandas as pd
import numpy as np
import os
from pandas import DataFrame


def install_dependency(*dependencies):
    import sys
    import subprocess

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", *dependencies
    ])


def run_emr_spark_job(
        name: str,
        steps: list,
        subnet_id: str,
        instance_type_master="m5.2xlarge",
        instance_type_core="m5.2xlarge",
        instance_type_task="m5.2xlarge",
        instance_ebs_size_master=128,
        instance_ebs_size_core=128,
        instance_ebs_size_task=128,
        instance_num_on_demand_core=50,
):
    install_dependency("awswrangler")
    import awswrangler as wr
    import boto3

    aws_access_key_id = "{access_key}"
    aws_secret_access_key = "secret_access_key"


    boto3.setup_default_session(region_name="ap-south-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    cluster_id = wr.emr.create_cluster(
        subnet_id=subnet_id,
        cluster_name=name,
        logging_s3_path=f"s3://hyun/log/{name}",
        emr_release="emr-6.4.0",
        instance_type_master=instance_type_master,
        instance_type_core=instance_type_core,
        instance_type_task=instance_type_task,
        instance_ebs_size_master=instance_ebs_size_master,
        instance_ebs_size_core=instance_ebs_size_core,
        instance_ebs_size_task=instance_ebs_size_task,
        instance_num_on_demand_core=instance_num_on_demand_core,
        applications=["Hadoop", "Spark", "Hive"],
        maximize_resource_allocation=True,
        keep_cluster_alive_when_no_steps=False,
        steps=steps,
        key_pair_name="hyun",
        debugging=False,
        spark_defaults={
            "spark.executor.defaultJavaOptions": "-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:OnOutOfMemoryError='kill -9 %p' -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=70 -XX:MaxHeapFreeRatio=70 -XX:+CMSClassUnloadingEnabled",
            "spark.driver.defaultJavaOptions": "-XX:OnOutOfMemoryError='kill -9 %p' -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=70 -XX:MaxHeapFreeRatio=70 -XX:+CMSClassUnloadingEnabled"
        }
    )

    if not check_emr_cluster_status(cluster_id):
        raise Exception(f"cluster {cluster_id} is failed")


def create_emr_acs_sms_parser_step(jar_path, class_name, resource="application.conf", args=[]):
    import awswrangler as wr

    return wr.emr.build_spark_step(
        path=f"--driver-java-options -Dconfig.resource={resource} --class {class_name} {jar_path} {' '.join(args)}",
        name=f"{class_name}"
    )


def check_emr_cluster_status(cluster_id):
    import time
    import awswrangler as wr

    while True:
        time.sleep(30)
        status = wr.emr.get_cluster_state(cluster_id)
        if status not in ["STARTING", "BOOTSTRAPPING", "RUNNING"]:
            break
    # some cases, cluster state is terminated, but step is failed.
    # so, need to check all steps is completed or not
    return check_emr_all_steps_completed(cluster_id)


def check_emr_all_steps_completed(cluster_id):
    import boto3
    client = boto3.client('emr')
    states = set([s["Status"]["State"] for s in client.list_steps(ClusterId=cluster_id)["Steps"]])
    return states == set(['COMPLETED'])
