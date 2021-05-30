[Understanding of Cluster Manager, Master and Driver nodes](https://stackoverflow.com/a/40560068/4352506)


Cluster는 cluster manager와 worker node집합을 얘기하는 것 같음.
Cluster Manager는 cluster를 관리하는 노드로써, driver program과 커뮤니케이션 함.

driver program은 처음에 명령을 내리고,
cluster manager가 명령을 각 worker node들을 관리하여, 처리하게 함
한 클러스터에 여러 Application이 실행 될 수 있음. driver program은 application 마다 있고, cluster mamager는 한 클러스터당 있음

deploy mode
- clinet mode : spark-submit을 하는 서버가 driver가 되고, cluster에 대해서, 말그대로 client역할을 하는 것임(cluster에 요청하고, 결과를 받고 하는 식으로. )
- driver program이 spark실행하는 서버에서 진행하기 때문에, driver program의 console로그를 확인가능(제플린 등에 적절)
- cluster mode : spark-submit을 멀리서 요청한 경우(local laptop에서 요청했을 때 등. driver program이 local이기 때문에, 지연이 심하여, 서버의 cluster에서만 호출되도록 처리)


Cluster Manager
- master process : the term of cluster manager in Spark standalone mode
- resource manager : the term of cluster manager in YARN.
- standalone, YARN, Mesos, kubernate등은 cluster 방식의 차이
    - cluster의 자원 배분 방식이 다름.
    - cluster구축시 이 방식 중 하나를 골라야 하는 듯..?


