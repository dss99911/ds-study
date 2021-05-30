
# Spark
- [Study Doc](study-spark)
## Run on local
```shell
sh script/run.sh
sh script/runPyspark.sh
```

## TODO
- [ ] [Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321/ref=sr_1_1?dchild=1&keywords=spark+data+application&qid=1602648326&sr=8-1)

## References(Not arranged)

- [x] [Overview & install](https://spark.apache.org/docs/latest/)
- [x] [Download](https://spark.apache.org/downloads.html)
- [x] [Install on Mac](https://medium.com/beeranddiapers/installing-apache-spark-on-mac-os-ce416007d79f)

### Programming Guides:
- [x] [Quick Start](https://spark.apache.org/docs/latest/quick-start.html): a quick introduction to the Spark API; start here!
- [x] [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html): overview of Spark basics - RDDs (core but old API), accumulators, and broadcast variables
- [x] [Spark SQL, Datasets, and DataFrames](https://spark.apache.org/docs/latest/sql-getting-started.html): processing structured data with relational queries (newer API than RDDs)
- [ ] [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html): processing structured data streams with relation queries (using Datasets and DataFrames, newer API than DStreams)
  - micro-batch processing model
  - Continuous Processing model

### Deployment Guides:
- [x] [Cluster Model Overview](study-spark/cluster-model-overview.md) : overview of concepts and components when running on a cluster
- [x] [Submitting Application](https://spark.apache.org/docs/latest/submitting-applications.html) : packaging and deploying applications
  - [ ] Amazon EC2: scripts that let you launch a cluster on EC2 in about 5 minutes
  - [ ] [Standalone Deploy Mode](http://spark.apache.org/docs/latest/spark-standalone.html#spark-standalone-mode): simplest way to deploy Spark on a private cluster. launch a standalone cluster quickly without a third-party cluster manager
    - 가장 가벼움.
    - Spark외에 다른 어플리케이션 사용 불가
  - [ ] Apache Mesos: deploy a private cluster using Apache Mesos
    - 무겁다
    - 내고장성. 탄력적 분산 시스템을 쉽게 구성
    - 큰 규모의 클러스터에 적합
  - [ ] Hadoop YARN: deploy Spark on top of Hadoop NextGen (YARN)
    - HDFS를 사용하는 애플리케이션에 적합(HDFS와 강하게 결합 됩.)
    - 클라우드 환경을 제대로 지원하지 못
  - [ ] Kubernetes: deploy Spark on top of Kubernetes
- [x] [Understand Cluster Manager, Master, Worker node](study-spark/understanding-cluster-manager-master-worker-node.md)
- [x] [Understanding Job, Stage, Task](study-spark/understanding-job-stage-task.md)
- [Setup Cluster](study-spark/setup-cluster.md)
- [Zeppelin Guide](study-spark/zeppelin.md)
- [Pyspark Guide](study-spark/pyspark.md)

### Other Documents:
- [x] [Spark Tuning & Monitoring](study-spark/spark-tuning-monitoring.md)
- [x] [Spark Kotlin](https://blog.jetbrains.com/kotlin/2020/08/introducing-kotlin-for-apache-spark-preview/)
- [ ] [Configuration](https://spark.apache.org/docs/latest/configuration.html): customize Spark via its configuration system
- [X] [Job Scheduling](study-spark/job-scheduling.md)
- [x] [Shuffle](study-spark/shuffle.md)
- [ ] Security: Spark security support
- [ ] Hardware Provisioning: recommendations for cluster hardware
- [ ] Integration with other storage systems:
- [ ] Cloud Infrastructures
- [ ] OpenStack Swift
- [ ] Migration Guide: Migration guides for Spark components
- [ ] Building Spark: build Spark using the Maven system
- [ ] Contributing to Spark
- [ ] Third Party Projects: related third party Spark projects
- [ ] Zeppelin add maven package
  - `export SPARK_SUBMIT_OPTIONS="--packages com.databricks:spark-csv_2.10:1.2.0"`
  - https://zeppelin.apache.org/docs/latest/interpreter/spark.html#1-export-spark_home
- [ ] [Spark with Excel](https://github.com/crealytics/spark-excel)

### External Resources:
- [ ] [Mastering Apache Spark 2.0](https://mallikarjuna_g.gitbooks.io/spark/content/)
- [ ] [위 책 번역본](https://wikidocs.net/24672)

### Example
- [x] [Spark Program](https://spark.apache.org/examples.html)
- [x] [Scala](https://github.com/apache/spark/tree/master/examples/src/main/scala/org/apache/spark/examples)
- [x] [Python](https://github.com/apache/spark/tree/master/examples/src/main/python)

### Books
- [x] Spark The Definitive Guide

### Later
- [ ] [UnitTest](https://spark.apache.org/docs/latest/rdd-programming-guide.html#unit-testing)
- [ ] [MLlib](https://spark.apache.org/docs/latest/ml-guide.html): applying machine learning algorithms
    - [ ] Spark NLP
- [ ] [GraphX](https://spark.apache.org/docs/latest/graphx-programming-guide.html): processing graphs


- [ ] Spark Streaming: processing data streams using DStreams (old API)
- [ ] [Spark Security](https://spark.apache.org/docs/latest/security.html)

# Zeppelin
- [Doc](study-zeppelin)

# Machine Learning
- [Doc](study-machinelearning)