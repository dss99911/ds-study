
Service 'sparkDriver' could not bind on a random free port. You may check whether configuring an appropriate binding address
- https://nurilee.com/2020/04/25/service-sparkdriver-could-not-bind-on-a-random-free-port-you-may-check-whether-configuring-an-appropriate-binding-address/



ERROR datasources.AsyncFileDownloader: TID: 6469 - Download failed for file path: s3://some/key=2021-09-12/part-00890-745cd3ee-b423-4714-8b04-737d3a4965a2-c000.snappy.parquet, range: 0-4296142, partition values: [2021-09-12], isDataPresent: false, eTag: null
java.io.InterruptedIOException: getFileStatus on s3://some/key=2021-09-12/part-00890-745cd3ee-b423-4714-8b04-737d3a4965a2-c000.snappy.parquet: com.amazonaws.AbortedException:

- spark.sql.files.ignoreCorruptFiles true 를 해주면, 에러는 나지 않지만, 특별한 이유 없이 이걸 설정하면, 읽기 실패한 데이터들이 누락될 가능성이 있어보임.
- emr에서 처리시에는 에러가 안나서, 일단은 emr에서 처리하도록 진행함.