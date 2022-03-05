from sagemaker import TrainingInput
from sagemaker.estimator import Estimator
import sagemaker
from sagemaker.xgboost import XGBoost

# https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost.html

role = sagemaker.get_execution_role()


#%% Use XGBoost as a built-in algorithm

image_uri = sagemaker.image_uris.retrieve(
    framework="xgboost",
    region="ap-south-1",
    version="1.0-1",
    py_version="py3",
    instance_type="ml.m5.xlarge",
)

# instance 갯수를 설정하여, 병렬 학습이 가능한 듯(여러 하이퍼 파라미터 테스트시 등은 별도로 학습 가능하므로)
xgb_train = Estimator(
    image_uri=image_uri,
    instance_type="ml.m5.xlarge",
    instance_count=1,
    output_path="s3://hyun/model", # model.tar.gz 라는 파일명으로 저장됨
    role=role,
)
xgb_train.set_hyperparameters(
    objective="reg:linear",
    num_round=50,
    max_depth=5,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    subsample=0.7,
    silent=0
)

#%% Use XGBoost as a framework

hyperparameters = {
    "max_depth":"5",
    "eta":"0.2",
    "gamma":"4",
    "min_child_weight":"6",
    "subsample":"0.7",
    "verbosity":"1",
    "objective":"reg:linear", # https://github.com/dmlc/xgboost/blob/master/doc/parameter.rst#learning-task-parameters
    "num_round":"50"}

estimator = XGBoost(
    entry_point="train.py",
    hyperparameters=hyperparameters,# optional, you can set on the code
    framework_version='1.2-1',
    instance_count=1,
    instance_type='ml.m5.xlarge'
)
#%%
# define the data type and paths to the training and validation datasets
content_type = "libsvm"
train_input = TrainingInput("s3://hyun/train_data", content_type=content_type)
# train_input = TrainingInput(s3_data="s3://hyun/train_data/")
# train_input = TrainingInput(s3_data="s3://hyun/train_data/" content_type="application/x-parquet")
validation_input = TrainingInput("s3://hyun/validation_data", content_type=content_type)

#%% fit
import time
from time import gmtime, strftime
metric_name = "validation:rmse"
job_name = "xgboost-parquet-example-training-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
# execute the XGBoost training job
estimator.fit(
    inputs={'train': train_input, 'validation': validation_input},
    job_name=job_name,

)