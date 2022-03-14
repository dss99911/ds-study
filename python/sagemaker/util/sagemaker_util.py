import os
import time
import zipfile

import boto3
import sagemaker
from sagemaker import get_execution_role
# noinspection PyUnresolvedReferences
from sagemaker.inputs import TrainingInput
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.sklearn import SKLearnProcessor
from sagemaker.spark import PySparkProcessor
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.xgboost import XGBoost
from util.common import *

_local_role = None
_is_local = True
_is_debug = False
_region_name = None
_profile_name = None
_sess = None
_bucket = None
_role = ""
_zip_s3_path = ""
_schema = "hyun"
_schema_path = "s3://hyun/hyun"


def set_environment(local_role=_local_role, is_local=_is_local, is_debug=_is_debug, region_name=_region_name, schema=_schema, schema_path=_schema_path, profile_name=_profile_name,
                    zip_s3_path=_zip_s3_path):
    """
    :param local_role: set to the iam role on `aws iam list-roles | grep SageMaker-Execution`
    :param is_local: run on local or sageMaker jupyter lab
    :param is_debug: if running on local instance or aws instance type
    :param region_name:
    :param profile_name: local awscli profile name
    :param zip_s3_path: s3 path to upload python.zip
    """
    global _local_role, _is_local, _is_debug, _region_name, _schema, _schema_path, _profile_name, _sess, _bucket, _role, _zip_s3_path
    _local_role = local_role
    _is_local = is_local
    _is_debug = is_debug
    _region_name = region_name
    _profile_name = profile_name
    _zip_s3_path = zip_s3_path
    _schema = schema
    _schema_path = schema_path

    _profile_name = profile_name if is_local else None
    _sess = sagemaker.Session(boto3.session.Session(region_name=_region_name, profile_name=_profile_name))
    boto3.setup_default_session(region_name=_region_name, profile_name=_profile_name)
    dummy_iam_role = 'arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001'
    _bucket = _sess.default_bucket()

    if _is_local:
        _role = _local_role
    elif is_debug:
        _role = dummy_iam_role
    else:
        _role = get_execution_role()

    print(boto3.__version__)
    print(sagemaker.__version__)
    print(_role)
    print(_bucket)


def is_local():
    return _is_local


def upload_pyfiles(excludes=[".idea/\*", "jars/\*", "\*.ipynb", "\*.sh", "\*.json"]):
    """
    :param excludes: if it's folder  .idea/\*
    """
    import os
    # os.system(f'zip -r python.zip . -x {" ".join(excludes)}')
    zip_py_files(".", "python.zip")
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


def instance_type(instancetype):
    return 'local' if _is_debug else instancetype


def get_pyspark_step(name, submit_app, instance_type_, instance_count, arguments=None, configuration=None, submit_jars=None, volume_size=30):
    if arguments is None:
        arguments = ["--schema", _schema, "--schema_path", _schema_path]

    pyspark_processor = PySparkProcessor(
        base_job_name="pyspark-process",
        framework_version="3.0",
        instance_count=instance_count,
        volume_size_in_gb=volume_size,
        **param(instance_type_)
    )

    run_args = pyspark_processor.get_run_args(
        submit_app=submit_app,
        submit_py_files=[_zip_s3_path],
        submit_jars=submit_jars,
        arguments=arguments,
        configuration=configuration,
    )

    return ProcessingStep(
        name=name,
        processor=pyspark_processor,
        inputs=run_args.inputs,
        job_arguments=run_args.arguments,
        code=run_args.code
    )


def get_sklearn_preprocess_step(name, script, inputs=[], outputs=[], instance_type="ml.r5.large"):
    framework_version = "0.23-1"
    arguments = ["--schema", _schema, "--schema_path", _schema_path]

    sklearn_processor = SKLearnProcessor(
        framework_version=framework_version,
        instance_count=1,
        base_job_name="sklearn-processor",
        volume_size_in_gb=512,
        max_runtime_in_seconds=7200,
        **param(instance_type)
    )

    step_sklearn_preprocess = ProcessingStep(
        name=name,
        processor=sklearn_processor,
        inputs=inputs + _get_dependency_inputs("."),
        outputs=outputs,
        job_arguments=arguments,
        code=script
    )

    return step_sklearn_preprocess


def get_xgboost_train_step(entry_point: str, instance_type, inputs):
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
        inputs=inputs
    )


def _get_dependency_inputs(root_path):
    # only 10 inputs are allowed
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


def run_steps_sequentially(*steps):
    for i, step in enumerate(steps):
        if (i + 1) >= len(steps):
            break
        steps[i + 1].add_depends_on([step.name])

    pipeline = Pipeline(name="hyun-test", steps=steps)
    pipeline.upsert(role_arn=_role)
    pipeline.start()


def run_pipeline(name: str, steps_depends_on):
    steps = [s[0] for s in steps_depends_on]

    for step, depends_on in steps_depends_on:
        step.depends_on = [d.name for d in depends_on if d in steps]

    return Pipeline(
        name=name,
        steps=steps
    )


def notify_completed(execution, slack_webhook_url=None):
    status = None

    while status != "Completed" and status != "Failed":
        time.sleep(30)
        status = execution.describe()["PipelineExecutionStatus"]

    step_name = execution.list_steps()[0]["StepName"]
    # send_slack_message_to_url(f"SageMaker Step {step_name} is {status}", slack_webhook_url)


def processing_input(name):
    return ProcessingInput(
        source=f"{_schema_path}/{name}",
        destination=get_input_path(name),
        input_name=name
    )


def processing_output(name):
    return ProcessingOutput(
        source=get_output_path(name),
        s3_upload_mode='EndOfJob',
        output_name=name,
        destination=f"{_schema_path}/{name}")


def zip_py_files(dir_path, zip_path):
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
