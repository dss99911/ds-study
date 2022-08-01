
Service 'sparkDriver' could not bind on a random free port. You may check whether configuring an appropriate binding address
- https://nurilee.com/2020/04/25/service-sparkdriver-could-not-bind-on-a-random-free-port-you-may-check-whether-configuring-an-appropriate-binding-address/



ERROR datasources.AsyncFileDownloader: TID: 6469 - Download failed for file path: s3://some/key=2021-09-12/part-00890-745cd3ee-b423-4714-8b04-737d3a4965a2-c000.snappy.parquet, range: 0-4296142, partition values: [2021-09-12], isDataPresent: false, eTag: null
java.io.InterruptedIOException: getFileStatus on s3://some/key=2021-09-12/part-00890-745cd3ee-b423-4714-8b04-737d3a4965a2-c000.snappy.parquet: com.amazonaws.AbortedException:

- spark.sql.files.ignoreCorruptFiles true 를 해주면, 에러는 나지 않지만, 특별한 이유 없이 이걸 설정하면, 읽기 실패한 데이터들이 누락될 가능성이 있어보임.
- emr에서 처리시에는 에러가 안나서, 일단은 emr에서 처리하도록 진행함.




Decommission
- 작업 시간이 오래 걸리는 경우 발생 가능
22/07/29 19:11:23 INFO HealthTracker: Excluding node ip-10-50-4-252.ap-south-1.compute.internal with timeout 1659125483183 ms because node is being decommissioned by Cluster Manager with timeout 3600 seconds.
22/07/29 19:11:23 INFO BlockManagerMaster: Removed executors on host ip-10-50-7-146.ap-south-1.compute.internal successfully.
22/07/29 19:11:23 INFO DAGScheduler: Shuffle files lost for host: ip-10-50-7-146.ap-south-1.compute.internal (epoch 26)

아래 시도 했지만, 효과가 있는지는 모름
//    .config("spark.network.timeout", "3600s")
//    .config("spark.dynamicAllocation.executorIdleTimeout", "3600s")
//    .config("spark.blacklist.decommissioning.timeout", "10h")
//    .config("spark.yarn.resourcemanager.nodemanager-graceful-decommission-timeout-secs", "10h")
관련 자료
https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-configure.html#spark-decommissioning
https://aws.amazon.com/ko/blogs/big-data/spark-enhancements-for-elasticity-and-resiliency-on-amazon-emr/
https://docs.aws.amazon.com/ko_kr/emr/latest/ManagementGuide/emr-scaledown-behavior.html
https://aws.github.io/aws-emr-best-practices/features/managed_scaling/best_practices/