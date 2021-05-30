### Environment
- 설치형 클러스터 (on-premise cluster)
- 공개 클라우드(public cloud)
    - elastic cluster


## Cluster Manager
### Standalone mode
- 스파크를위한 경량화된 플랫폼.
- 스파크 어플리케이션만 실행 가능.

#### Manual Setup
Start on Driver node
```shell
$SPARK_HOME/sbin/start-master.sh
```
it prints URI(spark://HOST:PORT)

Start on Worker node
```shell
$SPARK_HOME/sbin/start-slave.sh <driver-spark-uri>
```

#### Automatic Setup
add all worker node's hostname on the file below
```shell
$SPARK_HOME/conf/slaves
```
- driver node connect worker node by SSH with private key

```shell
$SPARK_HOME/sbin/start-all.sh # start master & slaves
#or
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slaves.sh
```

Stop
```shell
$SPARK_HOME/sbin/stop-master.sh
$SPARK_HOME/sbin/stop-slaves.sh
$SPARK_HOME/sbin/stop-all.sh
```

#### Launch Script
- [ ] http://spark.apache.org/docs/latest/spark-standalone.html#cluster-launch-scripts

