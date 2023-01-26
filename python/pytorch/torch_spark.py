# - [spark + pytorch inference](https://docs.microsoft.com/ko-kr/azure/databricks/_static/notebooks/deep-learning/pytorch-images.html)
# - [spark + pytorch](https://docs.microsoft.com/ko-kr/azure/synapse-analytics/machine-learning/tutorial-horovod-pytorch)


# - `"spark.rapids.memory.gpu.reserve": "10g"` 이 설정 안해주면 메모리 에러남
#   이 설정을 안해주면, Rapid memory manager가 메모리를 다 차지해서, torch가 메모리 점유를 못함
#   10g의 의미는 10g외의 메모리는 RMM이 차지한다는 의미 torch가 10g를 쓸 수 있게 하는 것. 인스턴스당 메모리 양인듯.

## Troubleshooting
# - cuda out of memory
    # - GPU memory를 초과해서 사용한 경우 발생
    # - nvidia-smi 를 통해, 어떤 task나 java 앱이 gpu를 얼마나 사용하는지 확인
    # - java가 많이 사용하고 있는데, torch등 python에서 돌리고 있다면, spark.rapids.memory.gpu.reserve 설정 필요.
    # - 몇 개의 task가 동시에 처리되고 있는지. java가 얼마나 사용하고 있는지 체크. python process 수 = spark.executor.cores / spark.task.cpus
    # - 하나의 task가 1277mb의 gpu메모리를 사용하는데, 그렇게 고정되는 이유는 불명확
# - spark gpu 호환
    # - spark gpu는 한 instance에 executor 1개로 고정하고 사용하는 듯한데,
    # - torch udf를 쓰게 되면, 한번에 여러 python process가 생성되고, 메모리를 1277mb를 사용해서. gpu메모리 부족 문제가 발생한다.
    # - 뭔가 torch 사용을 고려해서 nvdia에서 가이드 주지는 않아서, 사용이 어려움