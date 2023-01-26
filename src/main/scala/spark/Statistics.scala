package spark

import org.apache.spark.ml.functions.vector_to_array
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.apache.spark.sql.functions._

class Statistics {

  /**
   * 두 컬럼 사이의 영향도 비교
   * 공분산(covariance)
   *  - 표본공분산(sample covariance)
   *  - 모공분산(population covariance)
   * 상관 계수(Correlation coefficient) : 두 값의 관계를 알고 싶을 때 사용.
   */
  def correlationCoefficient(df: DataFrame) = {


    //갯수와 가격과의 상관 관계를 알고 싶을 때
    df.stat.corr("quantity", "unitPrice")
    df.select(corr("quantity", "unitPrice"))
    df.select(covar_pop("quantity", "unitPrice"))
    df.select(covar_samp("quantity", "unitPrice"))
  }

  def describe(df: DataFrame) = {
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

  def summary(spark: SparkSession) = {
    val df = Read.createDataFrameByRow(spark)
    df.summary().show()
    /*
+-------+------------------+------------------+-------+
|summary|                aa|                bb|     bb|
+-------+------------------+------------------+-------+
|  count|                 3|                 3|      3|
|   mean|2.3333333333333335|3.3333333333333335|   null|
| stddev|1.5275252316519468|1.5275252316519468|   null|
|    min|                 1|                 2|string1|
|    25%|                 1|                 2|   null|
|    50%|                 2|                 3|   null|
|    75%|                 4|                 5|   null|
|    max|                 4|                 5|string3|
+-------+------------------+------------------+-------+

     */
    df.summary("count").show()//show count only

    df.summary("count", "min", "25%", "75%", "max").show()
  }

  /**
   * There is two type of standard deviation.
   * - 표본표준편차(sample standard deviation)
   * - 모표준편차(population standard deviation)
   * todo check what is the difference
   */
  def standardDeviation(df: DataFrame) = {
    df.select(var_pop("dd"), var_samp("dd"))
      .select(stddev_pop("dd"), stddev_samp("dd"))
      .select(stddev("dd"), variance("dd")) //use sample standard deviation
  }

  /**
   * 비대칭도(skewness) : 데이터 평균의 비대칭 정도 측정
   * 첨도(kurtosis) : 데이터 끝 부분 측정
   *
   * 확률변수(random variable)의 확률분포(probability distribution)로 데이터 모델링할 때 특히 중요
   */
  def skewnessKurtosis(df: DataFrame) = {
    df.select(skewness("dd"), kurtosis("dd"))
  }

  def approxQuantile(df: DataFrame) = {
    df.stat.approxQuantile("value", Array(0.25, 0.5, 0.75), 0.1)
    //    Seq(3,1,5).toDF() => 1, 3, 5 해당 값의 중위값, 25% 의 값. 등을 구하는 것, relativeError는 오차 허용 값.
    //만약 quantile의 값에 해당 하는 row를 찾고 싶다면, 찾은 quantile 의 값으로 필터링해서, 다시 query하면 됨
  }

  def crosstab(df: DataFrame) = {
    /**
+-----+-------+
| name|   item|
+-----+-------+
|Alice|   milk|
|  Bob|  bread|
| Mike| butter|
|Alice| apples|
|  Bob|oranges|
| Mike|   milk|
|Alice|  bread|
|  Bob| butter|
| Mike| apples|
|Alice|oranges|
+-----+-------+
     */
    //convert 'name' as row, 'item' as column
    //name과 item이 겹치는(cross) 횟수가 얼마나 되는지를 name과 item을 행렬에 넣고, count를 표시.
    //name과 item으로 groupby해도 count를 알 수 있지만 이 경우에 name, item, count 컬럼으로 표시됨.
    //두 컬럼간의 상관관계를 한눈에 보기 좋다.
    df.stat.crosstab("name", "item").show()

    /**
     * +---------+----+-----+------+------+-------+
     * |name_item|milk|bread|apples|butter|oranges|
     * +---------+----+-----+------+------+-------+
     * |      Bob|   6|    7|     7|     6|      7|
     * |     Mike|   7|    6|     7|     7|      6|
     * |    Alice|   7|    7|     6|     7|      7|
     * +---------+----+-----+------+------+-------+
     */
  }

  /**
   * 피벗이란, 컬럼이 pivot column과, groupby column, agg column으로 나뉘는데
   * 1차적으로, pivot + groupby column으로 group by한 후, agg 를 하고나서,
   * 2차적으로, pivot column을 없애고, pivot column의 값 * agg column 만큼 컬럼의 수를 늘려서 표현
   * groupby column이 행, pivot * agg 이 컬럼이 됨
   */
  def pivot(spark: SparkSession) = {

//    df.groupBy("A", "B").pivot("C").sum("D")
//    df.groupBy("i_category")
//      .pivot("qoy")
//      .agg(round(sum("ss_sales_price")/1000000,2))

    /**
+-----------+----+----+----+----+
| i_category|  Q1|  Q2|  Q3|  Q4|
+-----------+----+----+----+----+
|      Books|1.58|1.50|2.84|4.66|
|      Women|1.41|1.36|2.54|4.16|
|      Music|1.50|1.44|2.66|4.36|
|   Children|1.54|1.46|2.74|4.51|
|     Sports|1.47|1.40|2.62|4.30|
|      Shoes|1.51|1.48|2.68|4.46|
|    Jewelry|1.45|1.39|2.59|4.25|
|       null|0.04|0.04|0.07|0.13|
|Electronics|1.56|1.49|2.77|4.57|
|       Home|1.57|1.51|2.79|4.60|
|        Men|1.60|1.54|2.86|4.71|
+-----------+----+----+----+----+
     */

    val df = Read.getJsonDataFrame(spark)
      .groupBy("User")
      .pivot("Device")
      .agg(mean("x").as("x_mean"), mean("y"), mean("z")) // if agg col is just one, the alias is not added to pivot col
      .show()

    /**
+----+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
|User|     nexus4_1_x_mean|     nexus4_1_avg(y)|     nexus4_1_avg(z)|     nexus4_2_x_mean|     nexus4_2_avg(y)|     nexus4_2_avg(z)|
+----+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
|   a|0.003599388097819...|-0.01101592275727...|-0.01294094049487...|-1.99824861345699...|-0.01179157475498...| -0.0134396594929291|
|   b|0.005725377455290168|-0.01002688442186...| 0.00301379168606245|0.003871362451145...|-0.00457738337577...|0.004047036385482...|
|   g|-0.00208632560193...|-0.00458886436661...|-0.01359292073636...|-0.00915738772685...|-0.00674707920018...|-8.58561385894742...|
|   h|-0.00550125460978...|-0.01629924664220...|-0.01514300812328...|-0.00812230581684151|-0.00334332692963...|-0.01013436852453...|
|   c|-0.01031501807637...|-0.01126438007684...|0.005435273286384981|-0.00314085422213...|-0.00843141042762...| 7.44572477560036E-4|
|   f|5.218046479539427E-4|0.001307288067977916|-0.00214763700341581|0.001665551849316...|-0.00293695204561...|-0.00813034041972...|
|   e|0.005279993953300105|-0.00328142709653...|-0.01477646526443...|0.002328937919791...|-0.00873569839349...|-0.00929037744580688|
|   i|0.005543884501249...|7.770937977789401E-4|-0.01902953802691...|0.006655974396658514|0.003165126311478...|-0.02074983958154...|
|   d|0.007489964376762028|-0.01616286103086...|-0.01526198680015...|  0.0120939639176969|-0.00294628113406...|-0.01053154644331...|
+----+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+

     */
  }

  def correlationMatrix(spark: SparkSession) = {
    import spark.implicits._
    import org.apache.spark.ml.linalg.{Matrix, Vectors}
    import org.apache.spark.ml.stat.Correlation
    import org.apache.spark.sql.Row

    //4개의 컬럼이 있는 것으로 간주한다.
    //각 컬럼들 간의 상관계수를 구해서, matrix로 보여준다.
    //|1.0                   0.055641488407465814  NaN  0.4004714203168137
    //0.055641488407465814  1.0                   NaN  0.9135958615342522
    //NaN                   NaN                   1.0  NaN
    //0.4004714203168137    0.9135958615342522    NaN  1.0                 |
    val data = Seq(
      // sparse는 드문드문 값을 저장 싶을 때 사용한다.
      // 자연어 처리시, 단어 갯수는 무수히 많지만, 실제 한 문서에서 사용하는 단어는 제한되므로 이 경우, 단어의 vector를 spare로 저장하는게, 당연히 효율적.(vector, value)의 map이라고 보면 될듯.
      // size : vector key 갯수
      // Seq((0, 1.0) : 0의 key에 값 1.0설정
      // 저장시에는 (4, [0,3], [1.0,-2.0]) 형식으로 저장 되는듯.
      Vectors.sparse(4, Seq((0, 1.0), (3, -2.0))),
//      Vectors.sparse(4, Array(0, 3), Array(1.0, -2.0)),//위의 방식과 결과는 같지만, 표현이 다름
//      Vectors.dense(0, 1, 3, -2.0),
      Vectors.dense(4.0, 5.0, 0.0, 3.0),
      Vectors.dense(6.0, 7.0, 0.0, 8.0),
      Vectors.sparse(4, Seq((0, 9.0), (3, 1.0)))
    )

    val df = data.map(Tuple1.apply).toDF("features")
    val Row(coeff1: Matrix) = Correlation.corr(df, "features").head
    println(s"Pearson correlation matrix:\n $coeff1")

    val Row(coeff2: Matrix) = Correlation.corr(df, "features", "spearman").head
    println(s"Spearman correlation matrix:\n $coeff2")
  }

  /**
   * 관찰된 빈도가 기대되는 빈도와 의미있게 다른지의 여부를 검정하기 위해 사용되는 검정방법이다. 자료가 빈도로 주어졌을 때, 특히 명목척도 자료의 분석에 이용
   */
  def chiSquareTest(spark: SparkSession) = {
    import spark.implicits._
    import org.apache.spark.ml.linalg.{Vector, Vectors}
    import org.apache.spark.ml.stat.ChiSquareTest

    val data = Seq(
      (0.0, Vectors.dense(0.5, 10.0)),
      (0.0, Vectors.dense(1.5, 20.0)),
      (1.0, Vectors.dense(1.5, 30.0)),
      (0.0, Vectors.dense(3.5, 30.0)),
      (0.0, Vectors.dense(3.5, 40.0)),
      (1.0, Vectors.dense(3.5, 40.0))
    )

    val df = data.toDF("label", "features")
    val chi = ChiSquareTest.test(df, "features", "label").head
    println(s"pValues = ${chi.getAs[Vector](0)}")
    println(s"degreesOfFreedom ${chi.getSeq[Int](1).mkString("[", ",", "]")}")
    println(s"statistics ${chi.getAs[Vector](2)}")
  }

  def summaryVector(spark: SparkSession) = {
    import spark.implicits._
    import org.apache.spark.ml.linalg.{Vector, Vectors}
    import org.apache.spark.ml.stat.Summarizer._

    val data = Seq(
      (Vectors.dense(2.0, 3.0, 5.0), 1.0),
      (Vectors.dense(4.0, 6.0, 7.0), 2.0)
    )

    val df = data.toDF("features", "weight")

    val (meanVal, varianceVal) = df.select(metrics("mean", "variance")
      .summary($"features", $"weight").as("summary"))
      .select("summary.mean", "summary.variance")
      .as[(Vector, Vector)]
      .first()

    println(s"with weight: mean = ${meanVal}, variance = ${varianceVal}")

    val (meanVal2, varianceVal2) = df.select(mean($"features"), variance($"features"))
      .as[(Vector, Vector)].first()

    println(s"without weight: mean = ${meanVal2}, sum = ${varianceVal2}")
  }

  def vector2array() = {
    vector_to_array(col("column"))
  }
}
