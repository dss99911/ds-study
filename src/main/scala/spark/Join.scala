package spark

import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.{broadcast, col, expr}

/**
 * join전에 dataframe을 적절히 분할하면 셔플이 계획되어 있더라도, 동일한 워커노드에 두 DataFrom의 데이터가 있다면, 셔플을 피할 수 도 있다고
 */
class Join {
  def join() = {
    //joinType default is inner, check comment on joinType on join method
    //'left', 'right'
    //'left_semi' : 오른쪽 df은 값이 존재하는지 조건 비교만하는 용도로만 쓰고, 조건이 성립하는 경우 왼쪽 df의 값만 가져온다. (교집합인데, 오른쪽 컬럼은 포함 안함)
    //'left_anti' : 왼쪽에만 존재하는 차집합. 오른쪽 컬럼은 당연히 포함안됨
    //'cross' : 교차 조인 n개와 m개의 경우, n*m개가 만들어
    val s = Read.getParquetDataFrame().as("s")
    val c = Read.getParquetDataFrame().as("c")
    s.join(c, col("s.id") === col("c.id"))//two 'id' column name exist
    s.join(c, "id")//one of 'id' column name dropped
    s.join(c, expr("array_contains(spark_status, id)"))

    //broadcast join : 워커노트에 한 df가 다 들어갈 수 있을 정도로, df가 작을 경우, broadcast로 모든 워커노드에 df을 복사한다.(처음에 모든 워커 노드에 복사가 이루어지느라 시간이 걸리지만, 이후로는 워커노드간의 통신이 없어서 빠르다)
    // broadcast() 설정하지 않아도, spark에서 phsical plan을 세울때, broadcast로 설정될 수도 있다.(Physical plan에 BroadcastHashJoin 이라고 나옴.
    // sql에서도 코맨트로 broadcast 힌트를 설정할 수 있지만, 강제성은 없다고..
    s.join(broadcast(c), col("s.id") === col("c.id"))
      .select(
        col("s.id").alias("id"),
        col("c.code").alias("code"),
        col("s.text").alias("text"),
        s.col("id").alias("sid")
      ).where("c.status = 1")
  }
}
