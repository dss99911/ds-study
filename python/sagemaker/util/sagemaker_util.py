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
from sagemaker.spark.processing import PySparkProcessor, SparkJarProcessor
from sagemaker.workflow.pipeline import Pipeline
# noinspection PyUnresolvedReferences
from sagemaker.workflow.parameters import ParameterString
# noinspection PyUnresolvedReferences
from sagemaker.workflow.functions import Join
# noinspection PyUnresolvedReferences
from sagemaker.workflow.step_collections import StepCollection
# noinspection PyUnresolvedReferences
from sagemaker.workflow.steps import ProcessingStep, Step
from sagemaker.workflow.steps import TrainingStep
from sagemaker.xgboost.estimator import XGBoost
# noinspection PyUnresolvedReferences
from sagemaker import TrainingInput
# noinspection PyUnresolvedReferences
from typing import Union, List, Optional
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
_zip_s3_path = f"{_schema_path}/code/pipeline.zip"
_schema = "hyun"
_schema_path = "s3://hyun/hyun"
_slack_channel: Optional[str] = None
_slack_token = None

def set_environment(is_debug=False, schema="hyun", schema_path=None, profile_name="default", slack_channel=None, is_upload_pyfiles=True):
    """
    :param is_debug: if running on local instance or aws instance type
    :param profile_name: local awscli profile name
    """
    global _is_debug, _region_name, _profile_name, _sess, _bucket, _role, _schema, _schema_path, _zip_s3_path, _slack_channel
    _is_debug = is_debug
    _profile_name = profile_name
    _schema = schema
    _schema_path = schema_path if schema_path is not None else f"s3://hyun/{schema}"
    _zip_s3_path = get_pipeline_zip_url(_schema_path)
    _slack_channel = slack_channel

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
    upload_file("python.zip", _zip_s3_path)
    os.remove("python.zip")


def upload_file(file_path, s3_path):
    upload_command = f'aws s3 cp "{file_path}" "{s3_path}"'
    if _is_local:
        upload_command += f" --profile {_profile_name}"

    os.system(upload_command)


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
        arg_list.append(str(v))

    pyspark_processor = PySparkProcessor(
        base_job_name="pyspark-process",
        framework_version="3.1",
        instance_count=instance_count,
        volume_size_in_gb=volume_size,
        **param(instance_type)
    )

    run_args = pyspark_processor.get_run_args(
        submit_app=submit_app,
        submit_py_files=[_zip_s3_path],
        submit_jars=submit_jars,
        arguments=arg_list,
        configuration=configuration
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


def get_spark_jar_step(submit_app, submit_class, instance_type="ml.r5.large", instance_count=1, arguments=[], configuration=None, submit_jars=None, volume_size=30, depends_on=[]):

    spark_processor = SparkJarProcessor(
        base_job_name="spark-java",
        framework_version="3.1",
        instance_count=instance_count,
        volume_size_in_gb=volume_size,
        **param(instance_type)
    )

    run_args = spark_processor.get_run_args(
        submit_app=submit_app,
        submit_class=submit_class,
        submit_jars=submit_jars,
        arguments=arguments,
        configuration=configuration,
    )

    name = submit_class.split(".")[-1].lower()  # for seeing log. upper character is not recognized.

    return ProcessingStep(
        name=name,
        processor=spark_processor,
        inputs=run_args.inputs,
        job_arguments=run_args.arguments,
        code=run_args.code,
        depends_on=[d.name for d in depends_on]
    )


def get_pyspark_emr_step(script, emr_instance_type="ml.r5.large", emr_instance_count=1, arguments={}, volume_size=128, max_runtime_in_seconds=None, depends_on=[]):
    py_path = get_code_url(schema_path(), script)
    upload_file(script, py_path)

    arguments.update({
        "py_path": py_path,
        "instance_type": emr_instance_type,
        "instance_count": emr_instance_count,
        "volume_size": volume_size
    })

    return get_sklearn_preprocess_step(
        "util/pyspark_emr_process.py",
        name=script.split("/")[-1].split(".")[0].replace("_", "-"),
        max_runtime_in_seconds=max_runtime_in_seconds,
        arguments=arguments,
        depends_on=depends_on
    )

def get_sklearn_preprocess_step(script, name=None, inputs=[], outputs=[], arguments={}, instance_type="ml.r5.large", max_runtime_in_seconds=7200, depends_on=[]):
    arguments.update({
        "schema": _schema,
        "schema_path": _schema_path,
    })

    arg_list = []
    for k, v in arguments.items():
        arg_list.append(f"--{k}")
        arg_list.append(str(v))

    script_processor = SKLearnProcessor(
        base_job_name="sklearn-processor",
        framework_version="0.23-1",
        instance_count=1,
        volume_size_in_gb=512,
        max_runtime_in_seconds=max_runtime_in_seconds,
        **param(instance_type)
    )
    if name is None:
        name = script.split("/")[-1].split(".")[0].replace("_", "-")

    step_sklearn_preprocess = ProcessingStep(
        name=name,
        processor=script_processor,
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


def start_pipeline(pipeline):
    execution = pipeline.start()
    thread = send_slack_message(f"SageMaker pipeline *{pipeline.name}* get started")
    notify_completed(pipeline, execution, thread)


def notify_completed(pipeline, execution, thread=None):
    previous_status_steps = defaultdict(set)
    step_start_time = {}
    while True:
        now = datetime.datetime.now()
        status = execution.describe()["PipelineExecutionStatus"]
        steps = execution.list_steps()
        step_status = {s["StepName"]: (s["StepStatus"], s["Metadata"]["ProcessingJob"]["Arn"].split("/")[-1]) for s in steps if "ProcessingJob" in s["Metadata"]}
        for s in steps:
            if "ProcessingJob" not in s["Metadata"] and "FailureReason" in s:
                log_text = f"[{s['StepName']}] status={s['StepStatus']} reason={s['FailureReason']}"
                print(f"{now} {log_text}")
                send_slack_message(log_text, thread)

        for k, v in step_status.items():
            if v[0] == "Executing" and step_start_time.get(k) is None:
                step_start_time[k] = now

            if v[0] not in ["Succeeded", "Failed", "Stopping", "Stopped"]:
                continue

            if k in previous_status_steps[v[0]]:
                continue

            previous_status_steps[v[0]].add(k)
            duration = str(now - step_start_time.get(k)) if step_start_time.get(k) is not None else ""

            log_text = f"[{k}] status={v[0]}, duration={duration}"
            print(f"{now} {log_text}, arn={v[1]}")
            send_slack_message(log_text, thread)

        if status in ["Succeeded", "Completed", "Failed", "Stopping", "Stopped"]:
            break
        time.sleep(30)

    step_status_failed = [(k, v) for k, v in step_status.items() if v[0] in ["Failed", "Stopping", "Stopped"]]

    send_slack_message(f"SageMaker pipeline *{pipeline.name}* is *{status}* {[k for k, v in step_status_failed]}", thread)

    cur_time = datetime.datetime.now()
    if step_status_failed:
        for k, v in step_status_failed:
            log_path = save_logs(pipeline.name, v[1], cur_time=cur_time)
            send_slack_file(v[1], log_path, thread)


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


def send_slack_file(comment, file_path: str, thread=None):
    if _slack_channel is None:
        print("slack channel is not configured")
        return

    import requests
    files = {
        'file': (file_path, open(file_path, 'rb'), 'text')
    }

    payload = {
        "title": file_path.split("/")[-1],
        "token": _slack_token,
        "channels": "#sagemaker_log",
        "initial_comment": comment
    }

    response_json = requests.post("https://slack.com/api/files.upload", params=payload, files=files).json()
    if response_json is None or not response_json["ok"]:
        print("can't upload file to slack")

    file_link = response_json["file"]["permalink"]

    send_slack_message(f"<{file_link}|error log of *{comment}*>", thread)

    return response_json


def send_slack_message(text, thread=None):
    if _slack_channel is None:
        print("slack channel is not configured")
        return

    import requests

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + _slack_token
    }

    payload = {
        "text": text,
        "channel": _slack_channel
    }

    if thread is not None:
        payload.update({
            "thread_ts": thread
        })

    # noinspection PyTypeChecker
    response_json = requests.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers).json()
    if response_json is None or not response_json["ok"]:
        print("can't send slack message")
    else:
        return response_json["ts"]


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
    stream_name_times = [(l["logStreamName"], l["lastIngestionTime"]) for l in json.loads(result)["logStreams"] if ("algo-1" in l["logStreamName"] and job_suffix.lower() in l["logStreamName"].lower())]
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
    return file_path


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
