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
    - [DAG understanding](dag/dag-understanding.md) : 실제 코드
    - [DAG understanding2](dag/dag-understanding2.md) : 책에 나오는 간단한 예제(이해하기 쉬움)
    - [DAG SQL Tab](dag/dag-sql-tab.md)
    - Ganglia
        - 클러스터 모니터링 도구. 클러스터 매니저 및 클러스터를 모니터링함
        - Spark앱이 아닌 클러스터를 모니터링.
        - `http://<server-url>/ganglia`

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