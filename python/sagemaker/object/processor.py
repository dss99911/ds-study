from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker import get_execution_role

framework_version = "0.23-1"
processing_instance_type = "ml.r5.2xlarge"
processing_instance_count = 1
role = get_execution_role()

sklearn_processor = SKLearnProcessor(
    framework_version=framework_version,
    instance_type=processing_instance_type,
    instance_count=processing_instance_count,
    base_job_name="sklearn-abalone-process",
    role=role,
)
# image docker
# https://github.com/aws/sagemaker-scikit-learn-container/blob/master/docker/0.23-1/base/Dockerfile.cpu

#%%
from sagemaker.spark.processing import PySparkProcessor

schema = "hyun2"
volume_size = 128
instance_type = "ml.m5.xlarge"

spark_processor = PySparkProcessor(
    base_job_name="spark-preprocessor",
    framework_version="3.0",
    role=role,
    instance_count=2,
    instance_type=instance_type,
    max_runtime_in_seconds=1200,
    volume_size_in_gb=volume_size,
)