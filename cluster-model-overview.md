[Cluster Model Overview](https://spark.apache.org/docs/latest/cluster-overview.html) : overview of concepts and components when running on a cluster
- 여러 클러스터가있고, sparkContext가 조율한다
- Driver program, Worker node가 있다.
- ClusterManager라는 얘가 있고, 얘가 리소스들을 각 클러스터에 적절히 할당한다(자체, Mesos, YARN등이 있음)
- SparkContext에서부터, 각 node의 executor로 application code를 전달한 후, task를 전달하여, 실행시키게 함
- sparkContext는 driver program에만 존재한다.
- Spark는 cluster manager를 agnostic(인지하지 못하는)하다.
- application은 hadoop 및 spark library등을 내장하지 않고, runtime에서 받음 (dependency에 provided로 정의)
- deploy 모드에는 client, cluster모드가 있음. cluster모드는 driver를 cluster안에 런치하고, client는 밖에 런치함