package spark

import org.apache.spark.sql.SparkSession

/**
 *
 * 1. hardware
 *  - instance type과 node type을 결정
 *    - ganglia를 보고, cpu, memory, I/O 부하를 확인한다.
 *    - memory, cpu, storage 어떤 것이 많이 필요하냐에 따라 instaance type 결정
 *      - caching, shuffling, and aggregating (using reduceByKey, groupBy, and so on) 은 메모리를 많이 차지할 수 있다.
 *    - node type
 *      - todo core, task 두개가 있는데, 구체적인 것은 잘 모르겠음(task는 저장을 안한다고 하는데.. core는 저장을 하므로, ondemand를 써야 한다고 함. 어떤 저장을 말하는 걸까?)
 *
 * 2. config 설정
 *  - GC config
 *  - executor, core, memory 설정
 *    - cpu사용량이 많으면, core수가 적은게 좋은 것 같다.
 * 3. 코드 개선
 *  - repartition
 *    - 데이터의 불균형이 큰데, 특정 컬럼으로 파티션이 나눠져있으면, 해당 컬럼으로 파티션은 나누되, 파티션 갯수를 크게하여, 불균형을 줄인다.
 *    - filter를 하게 되면, 특정 파티션의 row가 적거나 많은 현상이 생긴다. cpu사용이 많은 task가 있다면, 적절한 시점에 repartition을 해주는 것은 오히려 성능 향상이 될 수 있음.
 *
 * 성능 개선 방법
 * 1. 수동 테스트
 *  - row수를 줄여서, 빠르게 테스트해볼 수 있게 한다(너무 빠르면, 성능확인이 어려우니 적당한 크기로 설정)
 *  - 작업 처리 시간 및 ganglia, spark UI등을 확인한다.
 *  - hardware, config, 코드 개선 포인트를 찾고, 하나씩 적용해보면서, 시간이 단축되는지 확인한다.
 * 2. job분리
 *  - 작업할 데이터가 많으면, 한번에 전체다 처리하려고 하면, 잘 돌아가고 있는지 확인하려면, 몇 시간 후에 확인이 가능하고, 확인이 어렵다.
 *  - 처리 순서에 따라, 중간 데이터를 저장한 후에, 다시 처리하거나. 파티션으로 row들을 분리해서, 한 파티션씩 처리(user id prefix등으로)
 */
object Performance {
var builder: SparkSession.Builder = _

  def confs() = {
    builder
      .config("spark.network.timeout", "800s") //오래 걸리는 작업이 있으면, 이걸 설정하기. 설정안하면 timeout error가 발생
  }

  def gc() = {
    //처리 속도에 GC가 가장 치명적이다.
    builder
      //이걸로 하니까,오래걸리는 작업이 2배 빨라졌음.
      .config("spark.executor.defaultJavaOptions", "-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:OnOutOfMemoryError='kill -9 %p' -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=70 -XX:MaxHeapFreeRatio=70 -XX:+CMSClassUnloadingEnabled")
      .config("spark.driver.defaultJavaOptions", "-XX:OnOutOfMemoryError='kill -9 %p' -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=70 -XX:MaxHeapFreeRatio=70 -XX:+CMSClassUnloadingEnabled")

      //아래 문서에서는 아래를 권장하는데, 느렸음.
      // https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/
      .config("spark.executor.extraJavaOptions", "-XX:+UseG1GC -XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeConcMark -XX:InitiatingHeapOccupancyPercent=35 -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:OnOutOfMemoryError='kill -9 %p'")
      .config("spark.driver.extraJavaOptions", "-XX:+UseG1GC -XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeConcMark -XX:InitiatingHeapOccupancyPercent=35 -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:OnOutOfMemoryError='kill -9 %p'")
  }



  def dynamicResourceAllocation() = {
    //https://m.blog.naver.com/gyrbsdl18/220880041737
    //https://spark.apache.org/docs/latest/job-scheduling.html#dynamic-resource-allocation
    // spark.shuffle.service.enabled=true 를 통해 external shuffle service를 켜는 이유는.
    // 동정할당하게 되면, 의도치않게 셔플 도중에 executor가 Decommission 되는 경우가 있는데.
    // 이때, shuffle 데이터를 해당 executor에서 받는 게 아니라, 해당 서비스에서 받음.
    // todo spark.dynamicAllocation.shuffleTracking.enabled 이 실험적으로 추가됨. 이게 정식 릴리즈 되면, 이게 external shuffle 서비스가 없어도 되니, 더 좋을 수도??
    val spark = SparkSession.builder.appName("acs_tx_extractor")
      .config("spark.shuffle.service.enabled", true)//spark.dynamicAllocation.enabled를 사용하려면 true로 해줘야 함.
      .config("spark.dynamicAllocation.enabled", true)//spark.dynamicAllocation.maxExecutors를 사용하려면 true로 해줘야 함.
      .config("spark.dynamicAllocation.maxExecutors", 400) // executor 최대 갯수.
      .config("spark.dynamicAllocation.minExecutors", 350) // executor 최대 갯수.
      .config("spark.dynamicAllocation.enabled", value = true)
      .getOrCreate()
  }

  def memoryExecutorCore() = {
    //아래에서 제안한 방식인데, 설정안한 것보다 느리다...
    //https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/
    //https://blogs.perficient.com/2020/08/25/key-components-calculations-for-spark-memory-management/
    //  - hadoop daemon use 1 core 1 gb
    //  - memory overhead 10%, memory 90%
    // http://jason-heo.github.io/bigdata/2020/10/24/understanding-spark-memoryoverhead-conf.html
    //  - memory: on-heap memory
    //  - overhead memory : off-heap memory
    //    - min = 384mb
    //  - GC가 자주 발생하는 경우, memory올리기
    //  - 메모리 부족으로 kill되는 경우, overhead 올리기
    //m5.2xlarge 8 core 32gb
    val CORE_COUNT_PER_INSTANCE = 16
    val RAM_PER_INSTANCE = 65536
    val INSTANCE_COUNT = 20 //except for master node
    val executorCoreCount = 15
    val executorPerInstance = ((CORE_COUNT_PER_INSTANCE - 1) / executorCoreCount).toInt
    val executorCount = executorPerInstance * INSTANCE_COUNT
    val totalExecutorMemory =  (RAM_PER_INSTANCE / executorPerInstance).toInt
    val executorMemory = math.floor(totalExecutorMemory * 0.9).toInt
    val memoryOverhead = math.ceil(totalExecutorMemory * 0.1).toInt
    val parallelism = executorCount * executorCoreCount * 2
    builder
      .config("spark.executor.cores", executorCoreCount)
      .config("spark.driver.cores", executorCoreCount)
      .config("spark.executor.memory", executorMemory + "m") // executor의 memory
      .config("spark.driver.memory", executorMemory + "m")
      .config("spark.executor.memoryOverhead", memoryOverhead + "m")
      .config("spark.executor.instances", executorCount) // executor의 수, 하나의 instance에 executor가 여러개 있을 수도 있음
      .config("spark.default.parallelism", parallelism)
      .config("spark.sql.shuffle.partitions", parallelism)
  }

  def frequentlyUsed() = {
    builder
      .config("spark.executor.cores", 3) // 하나의 executor가 몇개의 cpu core를 사용할지. default : Yarn  1, 다른 모드에서는 worker node의 전체 core를 사용.
      .config("spark.files.maxPartitionBytes", 134217728)// 파일 읽을 때 파티션 수. 파티션이 적절히 있어야 빨리 읽어옮. default 128m
  }
}
