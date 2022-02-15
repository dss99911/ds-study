from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep

step_process = ProcessingStep(
    name="AbaloneProcess",
    outputs=[
        ProcessingOutput(output_name="test", source="/opt/ml/processing/test")
    ],
    code="abalone/preprocessing.py",
)

# output에 s3위치를 고정하지 않으면, 각 execution별로 s3폴더가 생성되어, 거기에서 가져옴
ProcessingInput(
    source=step_process.properties.ProcessingOutputConfig.Outputs[
        "test"
    ].S3Output.S3Uri,
    destination="/opt/ml/processing/test"
)

#만약 pipeline에서 중간부터 실행하고 싶다고 하면, s3위치를 고정시키고, 고정된 s3위치를 정의해야 함
ProcessingInput(
    source="s3://bucket/path/to/file",
    destination="/opt/ml/processing/test"
)