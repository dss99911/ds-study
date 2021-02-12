# Run on local
sh run.sh

# Spark Study

- [x] [Overview & install](https://spark.apache.org/docs/latest/)
- [x] [Download](https://spark.apache.org/downloads.html)
- [x] [Install on Mac](https://medium.com/beeranddiapers/installing-apache-spark-on-mac-os-ce416007d79f)

## Programming Guides:
- [x] [Quick Start](https://spark.apache.org/docs/latest/quick-start.html): a quick introduction to the Spark API; start here!
- [x] [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html): overview of Spark basics - RDDs (core but old API), accumulators, and broadcast variables
- [x] [Spark SQL, Datasets, and DataFrames](https://spark.apache.org/docs/latest/sql-getting-started.html): processing structured data with relational queries (newer API than RDDs)

## Deployment Guides:
- [x] [Cluster Model Overview](cluster-model-overview.md) : overview of concepts and components when running on a cluster
- [x] [Submitting Application](https://spark.apache.org/docs/latest/submitting-applications.html) : packaging and deploying applications
  - [ ] Amazon EC2: scripts that let you launch a cluster on EC2 in about 5 minutes
  - [ ] Standalone Deploy Mode: simplest way to deploy Spark on a private cluster. launch a standalone cluster quickly without a third-party cluster manager
  - [ ] Apache Mesos: deploy a private cluster using Apache Mesos
  - [ ] Hadoop YARN: deploy Spark on top of Hadoop NextGen (YARN)
  - [ ] Kubernetes: deploy Spark on top of Kubernetes
- [x] [Understand Cluster Manager, Master, Worker node](understanding-cluster-manager-master-worker-node.md)
- [x] [Understanding Job, Stage, Task](understanding-job-stage-task.md)

## Other Documents:
- [x] [Spark Tuning & Monitoring](spark-tuning-monitoring.md)
- [x] [Spark Kotlin](https://blog.jetbrains.com/kotlin/2020/08/introducing-kotlin-for-apache-spark-preview/)
- [ ] [Configuration](https://spark.apache.org/docs/latest/configuration.html): customize Spark via its configuration system
- [X] [Job Scheduling](job-scheduling.md)
- [ ] Security: Spark security support
- [ ] Hardware Provisioning: recommendations for cluster hardware
- [ ] Integration with other storage systems:
- [ ] Cloud Infrastructures
- [ ] OpenStack Swift
- [ ] Migration Guide: Migration guides for Spark components
- [ ] Building Spark: build Spark using the Maven system
- [ ] Contributing to Spark
- [ ] Third Party Projects: related third party Spark projects

## External Resources:
- [ ] [Mastering Apache Spark 2.0](https://mallikarjuna_g.gitbooks.io/spark/content/)
- [ ] [위 책 번역본](https://wikidocs.net/24672)

## Example
- [x] [Spark Program](https://spark.apache.org/examples.html)
- [x] [Scala](https://github.com/apache/spark/tree/master/examples/src/main/scala/org/apache/spark/examples)
- [x] [Python](https://github.com/apache/spark/tree/master/examples/src/main/python)

## Later
- [ ] [UnitTest](https://spark.apache.org/docs/latest/rdd-programming-guide.html#unit-testing)
- [ ] [MLlib](https://spark.apache.org/docs/latest/ml-guide.html): applying machine learning algorithms
- [ ] [GraphX](https://spark.apache.org/docs/latest/graphx-programming-guide.html): processing graphs
- [ ] [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html): processing structured data streams with relation queries (using Datasets and DataFrames, newer API than DStreams)
- [ ] Spark Streaming: processing data streams using DStreams (old API)
- [ ] [Spark Security](https://spark.apache.org/docs/latest/security.html)