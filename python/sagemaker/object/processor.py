from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker import get_execution_role

framework_version = "0.23-1"
processing_instance_type = "ml.r5.2xlarge"
processing_instance_count = 1
role = get_execution_role()

# add dependencies file
# https://stackoverflow.com/questions/69046990/how-to-pass-dependency-files-to-sagemaker-sklearnprocessor-and-use-it-in-pipelin
#   - add as input. code is added to /opt/ml/processing/input/code



sklearn_processor = SKLearnProcessor(
    framework_version=framework_version,
    instance_type=processing_instance_type,
    instance_count=processing_instance_count,
    base_job_name="sklearn-abalone-process",
    role=role,
)
# image docker
# https://github.com/aws/sagemaker-scikit-learn-container/blob/master/docker/0.23-1/base/Dockerfile.cpu

# docker를 이용해서, dependency를 추가하는 방법도 있지만, 매번 실행할 때마다, 설치하는 방법도 있음
def install_dependency():
    import sys
    import subprocess

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r",
        "/opt/ml/processing/input/code/my_package/requirements.txt",
    ])

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