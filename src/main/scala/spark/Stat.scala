package spark

import org.apache.spark.sql.functions.corr

class Stat {
  val df = Read.getCsv()
  /**
   * 상관 계수 : 두 값의 관계를 알고 싶을 때 사용.
   */
  def correlationCoefficient() = {


    //갯수와 가격과의 상관 관계를 알고 싶을 때
    df.stat.corr("quantity", "unitPrice")
    df.select(corr("quantity", "unitPrice"))
  }

  def describe() = {
    df.describe("id", "uniform", "normal").show()
    /*
+-------+------------------+-------------------+--------------------+
|summary|                id|            uniform|              normal|
+-------+------------------+-------------------+--------------------+
|  count|                10|                 10|                  10|
|   mean|               4.5| 0.5215336029384192|-0.01309370117407197|
| stddev|2.8722813232690143|  0.229328162820653|  0.5756058014772729|
|    min|                 0|0.19657711634539565| -0.7195024130068081|
|    max|                 9| 0.9970412477032209|  1.0900096472044518|
+-------+------------------+-------------------+--------------------+
     */
  }
}
