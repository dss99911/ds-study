
Sample

https://github.com/aws/amazon-sagemaker-examples

Build Your Own Processing Container
- for additional dependency
- https://docs.aws.amazon.com/sagemaker/latest/dg/build-your-own-processing-container.html


## Sagemaker Project
- pipeline CI/CD 자동화
- 정교한 프로세스가 요구되는 경우
- 파이프라인들을 하나의 프로젝트로 관리하고 싶은 경우
- endpoint, pipeline, ML model, experiments, repository를 하나로 관리하고 싶은 경우
- 그런데, 이런 것을 하기 위해서, 추가적인 학습이 필요. 

## Error

### 에러 로그 확인하기
- CloudWatch에서 algo-1의 로그를 확인해야함
- 로그가 많아서, 실제 원인을 설명하는 에러로그를 찾기가 어려움. 에러 발생시점에서 몇 초 사이로 필터링하고, Caused by, ERROR, TraceBack 등으로 검색