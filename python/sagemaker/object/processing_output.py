from sagemaker.processing import ProcessingOutput

ProcessingOutput(output_name="evaluation",
                 source="/opt/ml/processing/evaluation",
                 destination="s3://bucket/output/evaluation"  # s3저장할 위치 설정, 없으면 자동으로 default s3 bucket에 생성됨

                 )