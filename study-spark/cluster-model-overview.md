
# Reference
[Cluster Model Overview](https://spark.apache.org/docs/latest/cluster-overview.html) : overview of concepts and components when running on a cluster
[Understanding of Cluster Manager, Master and Driver nodes](https://stackoverflow.com/a/40560068/4352506)
[reference](https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/)
[executor count](https://jaemunbro.medium.com/spark-executor-%EA%B0%9C%EC%88%98-%EC%A0%95%ED%95%98%EA%B8%B0-b9f0e0cc1fd8)

## Explanation
- Driver Node, Worker Node가 있다.(Node는 서버와 대응. 두개를 포괄하여, cluster라고 하는 듯)
- 각각의 Node에는 Cluster Manager의 프로세스가 존재하고, 각 리소스를 관리한다.(자체, Mesos, YARN등이 있음. Yarn과 자체는 Hadoop cluster에서 돌아감. mesos는 잘 모르겠음)
- Dirver program(Driver process)와 executor process가 있고, application이 시작될 때, 생성된다.(driver process는 cluster mode의 경우, worker node에서 실행됨. client mode의 경우, 실행한 node에 driver process가 생성)
- 한 클러스터에 여러 Application이 실행 될 수 있음. driver program은 application 마다 있고, cluster mamager는 한 클러스터당 있음
- Driver program이 생성된 후, sparkContext를 통한 cluster manager에 요청하여, executor process가 각 worker node에 생성된다.
- driver program은 SparkContext를 통해, 각 node의 executor로 application code를 전달한 후, task를 전달하여, 실행시키게 함
- sparkContext는 driver program에만 존재한다(cluster manager와 통신하는 용도이므로 당연)
- Spark는 cluster manager를 agnostic(인지하지 못하는)하다.
- application은 hadoop 및 spark library등을 내장하지 않고, runtime에서 받음 (dependency에 provided로 정의)
- worker node 중 하나는 처리에 사용 안되는 것 같은데, cluster manager를 위한 것인듯..?

## Executor and Core
- excutor : node = n : 1 (각 executor는 한 worker node의 전체 core를 가질 수도 있고, 일부만 가질 수 있음. 일부만 가질 경우, 한 worker node에 여러 executor가 생성됨)
  - 한 노드에 core가 24개 있는 경우, `spark.executor.cores=6` 와 같이 설정하면, 4개의 executor가 생성되고, 한 executor가 6개의 core를 가지고, 6개의 task를 동시에 수행
  - `spark.task.cpus=1` 하나의 task가 하나의 core에 대응되는게 기본값, 변경은 가능

- Executor : driver한테서 application code를 받아서, 각 core에 task를 할당함.
- Core : 노드의 cpu core와 일치하는 개념. executor 가 각 core를 담당.

- executor당 core갯수가 작으면, executor수가 많아지고, I/O operation 양이 많아짐(셔플등에서 executor수만큼 I/O가 발생)
- executor당 core갯수를 크게 설정하면, executor갯수가 작아지고, 병렬성이 낮아짐(task들을 각 executor들이 처리하는데, 동시에 처리하는 task갯수가 줄어듬. 대신에, core를 여러개 쓰므로,하나의 task를 완료하는 시간은 더 빠를 듯)

하나의 executor당 최대 5개까지의 core(2~5), 4g이상(~ 64gb) memory 권장

계산
- 각 node당 하나의 core는 cluster manager의 prcess로 남겨놓는다

시작 점 : ```—-executor-cores 2 --executor-memory 16GB```

## deploy mode
- clinet mode : spark-submit을 하는 서버가 driver가 되고, cluster에 대해서, 말그대로 client역할을 하는 것임(cluster에 요청하고, 결과를 받고 하는 식으로. )
  - driver program이 spark실행하는 서버에서 진행하기 때문에, driver program의 console로그를 확인가능(제플린 등에 적절)
- cluster mode : spark-submit을 멀리서 요청한 경우(local laptop에서 요청했을 때 등. driver program이 local이기 때문에, 지연이 심하여, 서버의 cluster에서만 호출되도록 처리)
  - driver program이 worker node에서 실행되고, driver program이 속한 node는 task를 처리 안함.
  - cluster mode를 하는 이유는 client mode는 driver가 driver node에서 돌아가는데, 이렇게 되면, driver node의 자원을 많이 쓰게되고, 만약 driver노드에 다른 애플리케이션들이 돌아가고 있으면, driver node의 자원이 부족해져 OOM 에러 날 수 있음. 각 application을 분산하여 관리하기 위해 필요. 여러 앱을 한번에 돌리거나, 하나의 앱이라 하더라도 driver node 자원이 충분하지 않으면 cluster mode 쓰기

## Cluster Manager
- master process : the term of cluster manager in Spark standalone mode
- resource manager : the term of cluster manager in YARN.
- standalone, YARN, Mesos, kubernate등은 cluster 방식의 차이
    - cluster의 자원 배분 방식이 다름.
