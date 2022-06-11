# Monitoring
- [x] [Monitoring](https://spark.apache.org/docs/latest/monitoring.html)
    - [x] [Web UI](https://spark.apache.org/docs/latest/web-ui.html)
    - 4040 port
        - driver-node:4040
        - 앱이 실행될 동안만 유효한 것 같고, 설정에 따라, 마지막 실행된 앱에 대한 정보만 확인할 수 있는 듯하다.
    - Viewing After the Fact
        - 히스토리들을 볼 수 있음
        - ```./sbin/start-history-server.sh ``` 를 통해서 실행
        - `http://<server-url>:18080`
        - incompleted application history는 별도의 링크가 아래에 있음
        - 도중에 kill되면, 히스토리에서는 볼 수 없는듯. (Hadoop monitoring에서 킬된 정보는 뜨는데, 자세한 정보가 없음..)

    - Hadoop Monitoring
        - `http://<server-url>:8088`
        - Spark monitoring과 비슷한 정보를 줌. Hadoop cluster정보에 대한 모니터링 정보도 추가로 보여주는듯..
        - failure가 발생했을 때, 익셉션 정보 확인 가능(이상하게 spark web ui에서는 실패가 확인이 안됐음)
        - driver node log는 driver node 서버 접근 해서 확인 가능. `/home/hadoop/application_1605508398020_10199.log`
        - yarn log 확인하기. `yarn logs -applicationId application_16012459249102491 > application_16012459249102491.log`
    - [DAG understanding](dag/dag-understanding.md) : 실제 코드
    - [DAG understanding2](dag/dag-understanding2.md) : 책에 나오는 간단한 예제(이해하기 쉬움)
    - [DAG SQL Tab](dag/dag-sql-tab.md)
    - Ganglia
        - 클러스터 모니터링 도구. 클러스터 매니저 및 클러스터를 모니터링함
        - Spark앱이 아닌 클러스터를 모니터링.
        - `http://<server-url>/ganglia`
        - cluster의 cpu, memory, load, network 통계를 보여줌
        - instance, core의 load를 보여줌
        - 메모리가 부족한지, cpu가 부족한지, network i/o가 오래걸리는지 등을 확인 가능
        - 각 instance, core가 균형되게 처리하고 있는지도 확인 가능

# Performance
- [ ] [Tuning Guide](https://spark.apache.org/docs/latest/tuning.html): best practices to optimize performance and memory use
   - [Kryo serialization](https://spark.apache.org/docs/latest/tuning.html#data-serialization)
    - prefer arrays of objects, and primitive types, instead of the standard Java or Scala collection classes.
        - The [fastutil](http://fastutil.di.unimi.it/) library provides convenient collection classes for primitive types
- [ ] [Performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints-for-sql-queries)
- [x] [external article. Performance Tutorial](https://blog.scottlogic.com/2018/03/22/apache-spark-performance.html#:~:text=A%20shuffle%20occurs%20when%20data,likely%20on%20a%20different%20executor.)    
- [ ] How many partition is good?
    - [ ] [How Data Partitioning in Spark helps achieve more parallelism?](https://www.dezyre.com/article/how-data-partitioning-in-spark-helps-achieve-more-parallelism/297#:~:text=Having%20too%20large%20a%20number,or%20no%20data%20at%20all.)
    - [ ] [Apache Spark Partitioning](https://medium.com/@adrianchang/apache-spark-partitioning-e9faab369d14)
- [ ] [Adaptive Query Execution: Speeding Up Spark SQL at Runtime](https://databricks.com/blog/2020/05/29/adaptive-query-execution-speeding-up-spark-sql-at-runtime.html)

- [x] [Memory Managing](https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/)
  - Ganglia 사용하기
  - memory, executor, core 설정하기
  - GC 설정
  - Yarn설정

# read
https://jaemunbro.medium.com/apache-spark-partition-pruning%EA%B3%BC-predicate-pushdown-bd3948dcb1b6
https://dzone.com/articles/dynamic-partition-pruning-in-spark-30
## Partition pruning
- 데이터 파티션으로 나뉘어져있을 때, partition으로 filter를 하면, 메모리에 로딩전에 필터링 함
## Predicate push down
- 필터 조건에 따라, 데이터를 메모리에 로딩 자체를 안하게 하는 것. 보통 스캔 후, 필터링을 하는데, 필터를 스캔 밑으로 보내 수행한다고 해서, push down인듯?


# cloud integration
  - https://spark.apache.org/docs/latest/cloud-integration.html
  - s3의 경우, 파일 move가 오랜 시간이 걸리는 작업이라서, 기존 방식으로 처리하면 안됨.
  - emr의 경우, 자체 s3 connector를 사용하지만, sagemaker의 경우, spark에서 제공하는 cloud-integration을 사용함.
  - 자동으로 적용되기 때문에, 별도로 신경 쓰지 않아도 되지만, sagemaker에서 s3접근시 간혹, 에러가 나는 경우가 있음(emr에서는 정상 작동)
  - https://docs.amazonaws.cn/en_us/emr/latest/ReleaseGuide/emr-spark-s3select.html
    - pushdown for json, csv on emr

# Performance Advice
- " "또는 "EMPTY" 보다는 null을 쓰는게 좋음. null은 spark가 데이터가 없다는 걸 인지해서, 최적화된 처리 방법을 찾을 수 있음

##Slow Task
- 다른 테스크는 빨리 처리되는데, 몇몇 테스크만 엄청 오래 걸리는 경우
- 데이터가 파티션별로 치우쳐있는지 확인한다.
- partition수를 늘리는 걸 고려
- 메모리 늘리기
- 머신자체를 확인하기(ganglia등으로 확인?). 머신 내에 저장소 꽉찬 경우가 있을 수 있음
- Dataset을 사용할 경우, 가비지 콜렉션이 많은 시간을 차지 하지는 않는지 확인한다.

##Aggregation
- 파티션 수가 충분한지, 더 늘려야 하지 않는지 체크(집계전에 충분히 많은 파티션으로 분리하는게 좋음)
- 데이터가 많은 노드가 있는 경우, 익스큐터의 가용 메모리를 늘리면 좀더 빨라질 수 있음
- 데이터 불균형은 없는지 확인(aggregation후에도 속도가 느림) -> repartition
- collect_list/set 등은 가급적 피하기. 드라이버 노드로 데이터를 이동시킨다고함
- 집계연산은, 공통키와 관련된 많은 데이터를 메모리에 적재 한다고 한다. 각 worker node가 해당 공통키 데이터를 전부 가지고 있어서, 파티셔닝 및 join등을 할 때, shuffle을 해야 할지, 아니면, node내부에서 처리할지 알 수 있는 건가?
    - 만약 그렇다면, 공통 키의 데이터가 크면(id로 파티션 분할 하는 등), 작업이 엄청 느려질 수도 있을 듯.. 근데, 집계처리 안하면 상관 없을텐데..?
    - 파티션으로 분할된 파일의 경우, 분할이 너무 많이 된 경우, 저장소시스템에서 전체 파일의 목록을 읽을 때 오버헤드가 발생함

##Join
- Join시 broadcast join이 가능한 사이즈인지 확인(보통 spark가 자동으로 결정하지만, 통계 수집이 되 있는 경우만 가능하므로, 강제로 broadcast를 사용하거나, 통계 수집 명령을 내려야 한다고 함)
- prejoin partitioning 기법 고려(버켓팅, 특정 파티션으로 치우치지 않고, 균일하게 분할 할 수 있음)
- 데이터 치우침이 없는지 체크

##Out Of Memory
- 발생 위치가 드라이버인지 익스큐터인지 확인하기
- OutOfMemoryError 또는 가비지 컬렉션 관련 메시지 출력됨
- 명령이 장시간 실행되거나, 실행되지 않음. 반응이 거의 없음
- 드라이버 JVM 메모리 사용량이 많음
- collect등 드라이버에 대용량 데이터가 모이는 경우가 있는지 확
- broadcast하기에 큰 용량을 broadcast한 경우
- 장시간 실행도는 애플리케이션은 object가 반환이 안되는 경우, 많은 object를 가지고 있어서 발생할 수 있음 (jmap등의 힙 메모리의 히스토그램을 확인하는 도구 사용하여, 가장 많이 생성된 class명 확)
- 메모리, 익스큐터 증가시키기
- 적은 양의 데이터를 가지고 호출해보기. 적은 양의 데이터에서도 그러면, 데이터가 많아서 생기는 문제가 아님
- 파이썬 데이터 변환에 따른 문제임인지 확인  
- 노트북등 SparkContext를 공유하는 경우, 드라이버 노드로 대용량 데이터를 가져와서 출력하는 것을 막아야 함(그래서, 제플린에서 출력 제한이 있는 듯)
- 데이터가 치우쳐져있진 않은지 확인
- RDD, Dataset, UDF가 문제를 야기할 가능성이 큼인
- 가비지 콜렉션이 자주 발생하면, 캐시에 사용되는 메모리 양을 줄여야 함
- Full garbage collection과 minor garbage collection 중 어떤게 많이 발생하는지 파악하여, 적절히 조치취하기.

##Out of disk
- 공간 늘리기
- 애플리케이션 처리 중 데이터 치우침이 없는지 확인
- 스파크 설정 변경 (로그 유지 기간 등)
- 문제가 된 노드의 로그파일,셔플파일등 수동 제거(임시 처리)

##널이 있는 데이터
- 잘 작동하다가 작동을 안하거나, 일부 데이터가 없다.
- 어큐뮬레이터로, 특정 데이터 타입의 수를 확인한다.


##직접적인 성능 향상 방법
- 병렬성을 높이기(spark.default.parallelism, spark.shuffle.partitions의 값을 클러스터 코어 수에 따라 설정(CPU코어당 2~3개 테스크 할))
- 필터링을 최대한 먼저 하기
- 파티션 수를 줄일 때는 repartition대신 coalesce를 사용해서, 셔플을 방하기


## Performance Tuning for Athena(presto) Sql

### Partition
partitioned table 조회 시 partition 조건을 넣어주세요!
partitioned된 데이터의 경우 partition 조건을 통해 더 적은 리소스만 활용해 더 빠르게 결과를 받아볼 수 있다.

### Approximate Functions
100% 정확한 Unique Count가 필요한 케이스가 아니라면(추세를 보는 것으로 충분한 경우) distinct() 대신 approx_distinct()를 활용해 Approximate Unique Count를 활용할 수 있다.
이 방식은 hash값을 활용해 전체 string값을 읽는 것보다 훨씬 적은 메모리를 활용해 훨씬 빠르게 계산할 수 있도록 해준다. 표준오차율은 2.3%.

Example :
```sql
SELECT approx_distinct(l_comment) FROM lineitem;
```

### SELECT
asterisk(*)를 사용한 전체 선택은 지양하고 필요한 컬럼을 지정하여 SELECT

Parquet file 특성 상 컬럼별로 지정하여 원하는 컬럼만 read 하므로 불필요한 연산을 크게 줄일 수 있다.

### JOIN
Issue : Left에 작은 테이블, Right에 큰 테이블을 두면 Presto는 Right의 큰 테이블을 Worker node에 올리고 Join을 수행한다. (Presto는 join reordering을 지원하지 않음)

Best Practice : Left에 큰 테이블, Right에 작은 테이블을 두면 더 작은 메모리를 사용하여 더 빠르게 쿼리할 수 있다.

Example
Dataset: 74 GB total data, uncompressed, text format, ~602M rows

Query	Run time
```sql
SELECT count(*) FROM lineitem, part WHERE lineitem.l_partkey = part.p_partkey	//22.81 seconds
SELECT count(*) FROM part, lineitem WHERE lineitem.l_partkey = part.p_partkey	//10.71 seconds
```

### JOIN (Big Tables)
Issue : Presto는 Index 없이 fast full table scan 방식. Big table간 join은 아주 느리다. 따라서 AWS 가이드는 이런 류의 작업에 Athena 사용을 권장하지 않는다.

Best Practice : Big Table은 ETL을 통해 pre-join된 형태로 활용하는 것이 좋다.

### ORDER BY
Issue : Presto는 모든 row의 데이터를 한 worker로 보낸 후 정렬하므로 많은 양의 메모리를 사용하며, 오랜 시간 동안 수행하다가 Fail이 나기도 함.

Best Practice :
1. LIMIT 절과 함께 ORDER BY를 사용. 개별 worker에서 sorting 및 limiting을 가능하게 해줌.
2. ORDER BY절에 String 대신 Number로 컬럼을 지정. ORDER BY order_id 대신 ORDER BY 1

Example:
Dataset: 7.25 GB table, uncompressed, text format, ~60M rows

Query	Run time
```sql
SELECT * FROM lineitem ORDER BY l_shipdate //528 seconds
SELECT * FROM lineitem ORDER BY l_shipdate LIMIT 10000	//11.15 seconds
```


### GROUP BY
Issue : GROUPING할 데이터를 저장한 worker node로 데이터를 보내서 해당 memory의 GROUP BY값과 비교하며 Grouping한다.
Best Practice : GROUP BY절의 컬럼배치순서를 높은 cardinality부터 낮은 cardinality 순(unique count가 큰 순부터 낮은 순으로)으로 배치한다. 같은 의미의 값인 경우 가능하면 string 컬럼보다 number 컬럼을 활용해 GROUP BY한다.

Example :

```sql
SELECT state, gender, count(*) FROM census GROUP BY state, gender;
```

### LIKE
Issue : string 컬럼에 여러개의 like검색을 써야하는 경우 regular expression을 사용하는 것이 더 좋다.
Example :
```sql
SELECT count(*) FROM lineitem WHERE regexp_like(l_comment, 'wake|regular|express|sleep|hello')
```

## Performance tuning for Parquet
- https://parquet.apache.org/documentation/latest/
- 각 parquet파일당 적정 파일 크기?
- parquet, ORC format의 경우 data section별로 metadata를 보관한다. 따라서 filter(where) 조건을 잘 주면 data read를 skip할 수도 있다 -> 파티션과 별개로, 한 파일 내에서도, 데이터가 색션별로 나뉘어서, 각 색션별 각각의 컬럼의 데이터의 범위를 저장하고 있다는 얘기인지? 그래서, 파티션 키가 아니라고 하더라도, sorting을 해놓으면, sorting해놓은 값으로 필터링하게 되는 경우, 더 빠르게 필터링이 가능할 것으로 추측됨


### Compress and Split Files
Use splittable format like Apache Parquet or Apache ORC.

BZip2, Gzip로 split해서 쓰기를 권장하며 LZO, Snappy는 권장하지 않는다. (압축효율 대비 컴퓨팅 속도를 감안)

### Optimize File Size
optimal S3 file size is between 200MB-1GB (다른데서는 512mb to 1024mb라고 함)

file size가 아주 작은 경우(128MB 이하), executor engine이 S3 file을 열고, object metadata에 접근하고, directory를 리스팅하고, data transfer를 세팅하고, file header를 읽고, compression dictionary를 읽는 등의 행동을 해야하는 오버헤드로 인해 효율이 떨어지게 된다.

file size가 아주 크고 splittable하지 않은 경우, query processor는 한 파일을 다 읽을때까지 대기해야 하고 이는 athena의 강력한 parallelism 기능을 활용할 수 없게 한다.

Example

Query	Number of files	Run time
```sql
SELECT count(*) FROM lineitem	7GB, 5000 files	8.4 seconds
SELECT count(*) FROM lineitem	7GB, 1 file	2.31 seconds
```

### Join Big Tables in the ETL Layer
Athena는 index 없이 full table scan을 사용한다. 따라서 작은 규모의 데이터를 join할 때는 아무 문제 없지만 큰 데이터를 조인할 때는 ETL을 활용해 pre-join된 형태로 활용하는 것이 좋다.

### Optimize Columnar Data Store Generation
The stripe size or block size parameter : ORC stripe size, Parquet block size는 block당 최대 row수를 의미한다. ORC는 64MB, Parquet는 128MB를 default로 가진다. 효과적인 sequential I/O를 고려하여 column block size를 정의할 것.

