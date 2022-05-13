import os
import subprocess
from os import path
import time
import zipfile
import json
import boto3
import sagemaker
import platform
from collections import defaultdict
# noinspection PyUnresolvedReferences
from sagemaker import get_execution_role
# noinspection PyUnresolvedReferences
from sagemaker.processing import ProcessingInput, ProcessingOutput, ScriptProcessor
from sagemaker.spark.processing import PySparkProcessor
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.functions import Join
from sagemaker.workflow.step_collections import StepCollection
from sagemaker.workflow.steps import ProcessingStep, Step
from sagemaker.workflow.steps import TrainingStep
from sagemaker.xgboost.estimator import XGBoost
# noinspection PyUnresolvedReferences
from sagemaker import TrainingInput
from typing import Union, List
import datetime
from sagemaker.sklearn import SKLearnProcessor

# todo modify path properly.
# from util.common import *
from common import *

# todo need to change _local_role, _region_name for using
# change to the iam role on `aws iam list-roles | grep SageMaker-Execution`
_local_role = "arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001"
_is_local = platform.system() != "Linux"
_is_debug = False
_region_name = "ap-south-1"
_profile_name = "default"
_sess = None
_bucket = None
_role = ""

_schema = "hyun"
_schema_path = "s3://hyun/hyun"
_zip_s3_path = f"{_schema_path}/code/pipeline.zip"
_slack_webhook_url = None

def set_environment(is_debug=False, schema="hyun", schema_path="s3://hyun/hyun", profile_name="default", slack_webhook_url=None, is_upload_pyfiles=True):
    """
    :param is_debug: if running on local instance or aws instance type
    :param profile_name: local awscli profile name
    """
    global _is_debug, _region_name, _profile_name, _sess, _bucket, _role, _schema, _schema_path, _zip_s3_path, _slack_webhook_url
    _is_debug = is_debug
    _profile_name = profile_name
    _schema = schema
    _schema_path = schema_path
    _zip_s3_path = f"{_schema_path}/code/pipeline.zip"
    _slack_webhook_url = slack_webhook_url

    _profile_name = _profile_name if _is_local else None
    _sess = sagemaker.Session(boto3.session.Session(region_name=_region_name, profile_name=_profile_name))
    boto3.setup_default_session(region_name=_region_name, profile_name=_profile_name)
    dummy_iam_role = 'arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001'
    _bucket = _sess.default_bucket()

    if _is_local:
        _role = _local_role
    elif _is_debug:
        _role = dummy_iam_role
    else:
        _role = get_execution_role()

    print("boto3:", boto3.__version__)
    print("sagemaker:", sagemaker.__version__)
    print("role:", _role)
    print("bucket:", _bucket)
    print("schema:", _schema)

    if is_upload_pyfiles:
        upload_pyfiles()



def upload_pyfiles():

    #zip을 통한 방식, sagemaker에서는 zip이 없어서 안됨.
    # excludes=[".idea/\*", "jars/\*", "\*.ipynb", "\*.sh", "\*.json"]
    # import os
    # os.system(f'zip -r python.zip . -x {" ".join(excludes)}')
    _zip_py_files(".", "python.zip")
    upload_command = f'aws s3 cp python.zip "{_zip_s3_path}"'
    if _is_local:
        upload_command += f" --profile {_profile_name}"

    os.system(upload_command)
    os.remove("python.zip")


def param(instancetype=None):
    param_ = {
        'role': _role,
    }
    if not _is_debug:
        param_['sagemaker_session'] = _sess

    if instancetype is not None:
        param_['instance_type'] = instance_type(instancetype)
    return param_


def get_pyspark_step(submit_app, instance_type="ml.r5.large", instance_count=1, arguments={}, configuration=None, submit_jars=None, volume_size=30, depends_on=[]):
    arguments.update({
        "schema": _schema,
        "schema_path": _schema_path,
    })

    arg_list = []
    for k, v in arguments.items():
        arg_list.append(f"--{k}")
        arg_list.append(v)

    pyspark_processor = PySparkProcessor(
        base_job_name="pyspark-process",
        framework_version="3.0",
        instance_count=instance_count,
        volume_size_in_gb=volume_size,
        **param(instance_type)
    )

    run_args = pyspark_processor.get_run_args(
        submit_app=submit_app,
        submit_py_files=[_zip_s3_path],
        submit_jars=submit_jars,
        arguments=arg_list,
        configuration=configuration,
    )

    name = submit_app.split("/")[-1].split(".")[0].replace("_", "-")

    return ProcessingStep(
        name=name,
        processor=pyspark_processor,
        inputs=run_args.inputs,
        job_arguments=run_args.arguments,
        code=run_args.code,
        depends_on=[d.name for d in depends_on]
    )


def get_sklearn_preprocess_step(script, inputs=[], outputs=[], instance_type="ml.r5.large", arguments={}, max_runtime_in_seconds=7200, depends_on=[]):
    framework_version = "0.23-1"
    arguments.update({
        "schema": _schema,
        "schema_path": _schema_path,
    })

    arg_list = []
    for k, v in arguments.items():
        arg_list.append(f"--{k}")
        arg_list.append(v)


    sklearn_processor = SKLearnProcessor(
        framework_version=framework_version,
        instance_count=1,
        base_job_name="sklearn-processor",
        volume_size_in_gb=512,
        max_runtime_in_seconds=max_runtime_in_seconds,
        **param(instance_type)
    )

    name = script.split("/")[-1].split(".")[0].replace("_", "-")
    step_sklearn_preprocess = ProcessingStep(
        name=name,
        processor=sklearn_processor,
        inputs=inputs + _get_dependency_inputs("."),
        outputs=outputs,
        job_arguments=arg_list,
        code=f"{script}",
        depends_on=[d.name for d in depends_on]
    )

    return step_sklearn_preprocess


def get_xgboost_train_step(entry_point: str, instance_type, inputs, depends_on=[]):
    xgb_train = XGBoost(
        entry_point=entry_point,
        framework_version='1.2-1',
        instance_count=1,
        **param(instance_type)
    )

    name = entry_point.split("/")[-1].split(".")[0].replace("_", "-")

    return TrainingStep(
        name=name,
        estimator=xgb_train,
        inputs=inputs,
        depends_on=[d.name for d in depends_on],
    )


def _get_dependency_inputs(root_path):
    # only 10 inputs are allowed. select the python folders which is required if input is more than 10
    from os import listdir, path

    output = []
    for f in listdir(root_path):
        if f.startswith('.'):
            continue

        file_path = path.join(root_path, f)
        # root path is not supported because, only directory can bo copied.
        if path.isdir(file_path):
            output.append(ProcessingInput(source=file_path, destination=get_input_path(f"code/{file_path}")))
    return output

def instance_type(type):
    return 'local' if _is_debug else type


def make_pipeline(name: str, steps_depends_on, parameters=[]):
    steps = [(s[0] if type(s) is tuple else s) for s in steps_depends_on]
    depends_ons = [(s[1] if type(s) is tuple else []) for s in steps_depends_on]

    for step, depends_on in zip(steps, depends_ons):
        step.depends_on = [d.name for d in depends_on if d in steps]

    pipeline = Pipeline(
        name=name,
        parameters=parameters,
        steps=steps
    )
    print("making pipeline")
    parsed = json.loads(pipeline.definition())
    print(json.dumps(parsed, indent=2, sort_keys=True))
    pipeline.upsert(role_arn=role())
    return pipeline


def notify_completed(pipeline, execution):
    previous_status_steps = defaultdict(set)

    while True:
        status = execution.describe()["PipelineExecutionStatus"]
        step_status = {s["StepName"]: (s["StepStatus"], s["Metadata"]["ProcessingJob"]["Arn"].split("/")[-1]) for s in execution.list_steps()}
        for k, v in step_status.items():
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if k not in previous_status_steps[v[0]]:
                previous_status_steps[v[0]].add(k)
                print(f"{now} [{k}] status={v[0]}, arn={v[1]}")

        if status == "Succeeded" or status == "Completed" or status == "Failed" or status == "Stopping" or status == "Stopped":
            break
        time.sleep(30)

    step_status_failed = [(k, v) for k, v in step_status.items() if v[0] in ["Failed", "Stopping", "Stopped"]]
    cur_time = datetime.datetime.now()
    if step_status_failed:
        for k, v in step_status_failed:
            save_logs(pipeline.name, v[1], cur_time=cur_time)
    send_slack_message_to_url(f"SageMaker pipeline {pipeline.name} is {status} by {[k for k, v in step_status_failed]}")


def schema_path():
    return _schema_path


def schema():
    return _schema


def role():
    return _role


def processing_input(name, source=None):
    return ProcessingInput(
        source=f"{_schema_path}/{name}" if source is None else source,
        destination=get_input_path(name),
        input_name=name
    )


def processing_output(name, destination=None):
    return ProcessingOutput(
        source=get_output_path(name),
        s3_upload_mode='EndOfJob',
        output_name=name,
        destination=f"{_schema_path}/{name}" if destination is None else destination)


def send_slack_message_to_url(text):
    import requests
    payload = {
        "text": text
    }
    if _slack_webhook_url is None:
        print("slack_webhook_url is not configured")
        return
    # noinspection PyTypeChecker
    requests.post(_slack_webhook_url, json=payload)


def _zip_py_files(dir_path, zip_path):
    """zipfile로 하면, __init__.py를 추가하지 않으면, 인식을 못함.
        bash의 zip -r로 하면 인식 함. 차이를 잘 모르겠지만,
        sagemaker studio에서 돌릴 때, zip이 설치되어 있지 않아. 이렇게 처리
    """
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            apath = os.path.join(root, file)
            if not apath.endswith(".py"):
                continue
            relpath = os.path.relpath(apath, dir_path)
            print(apath)
            zipf.write(apath, f"{relpath}")

    zipf.close()


def save_logs(pipeline_name, job_name: str, repeat_count: int = 3, cur_time=datetime.datetime.now()):
    print("job_name:", job_name)
    job_prefix = "-".join(job_name.split('-')[0:-1])
    # suffix is lower case. but for accessing log, original case is needed.
    job_suffix = job_name.split('-')[-1]
    cmd_get_log_strema_name = (
        "aws logs describe-log-streams"
        " --log-group-name '/aws/sagemaker/ProcessingJobs'"
        f" --log-stream-name-prefix '{job_prefix}'"
        f" --region '{_region_name}'"
    )
    cmd_get_log_strema_name += f" --profile {_profile_name}"
    result = subprocess.check_output(cmd_get_log_strema_name, shell=True)
    stream_name_times = [(l["logStreamName"], l["lastIngestionTime"]) for l in json.loads(result)["logStreams"] if ("algo-1" in l["logStreamName"] and job_suffix in l["logStreamName"].lower())]
    if not stream_name_times:
        print("can't find logs for", job_name)
        return
    stream_name, last_ingestion_time = stream_name_times[0]
    print("stream_name:", stream_name)

    next_token = None
    current_time_str = cur_time.strftime("%Y-%m-%dT%H:%M:%S")
    log_dir = f"logs/{pipeline_name}-{current_time_str}"
    file_path = f"{log_dir}/{job_name}.log"
    if not path.exists(log_dir):
        os.makedirs(log_dir)

    print("file_path:", file_path)
    for i in range(repeat_count):
        next_token = _save_log_stream_name(file_path, stream_name, last_ingestion_time, next_token)
    print("logs saved")


def _save_log_stream_name(file_path, stream_name, last_ingestion_time, next_token=None):
    cmd_get_log = (
        f"aws logs get-log-events"
        " --log-group-name '/aws/sagemaker/ProcessingJobs'"
        f" --log-stream-name '{stream_name}'"
        f" --end-time {last_ingestion_time}"
        f" --limit 10000"
        f" --region '{_region_name}'"
    )
    if next_token:
        cmd_get_log += f" --next-token {next_token}"
    cmd_get_log += f" --profile {_profile_name}"

    result = subprocess.check_output(cmd_get_log, shell=True)
    obj = json.loads(result)
    events = obj["events"]

    output = "\n".join([_long_to_date(e['timestamp']) + "\t" + e["message"] for e in events])

    _prepend_text_to_file(file_path, output)
    next_forward_token = obj["nextForwardToken"]
    return next_forward_token


def _long_to_date(long_time: int):
    import datetime
    return datetime.datetime.fromtimestamp(long_time / 1000).strftime("%Y-%m-%d %H:%M:%S")


def _prepend_text_to_file(file_path: str, text: str):
    lines = []
    if path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
    with open(file_path, "w") as f:
        f.write(text)
        f.write("".join(lines))


def is_local():
    return _is_local