package spark

import org.apache.spark.sql.functions.{approx_count_distinct, avg, col, collect_list, collect_set, count, countDistinct, expr, first, grouping, grouping_id, last, max, min, struct, sum, sumDistinct, udf, when}
import org.apache.spark.sql.types.IntegerType
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import spark.Read.Person

import scala.collection.mutable

class AggregationAndGrouping {
  private val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._
  private val df: DataFrame = Read.getParquetDataFrame()

  def onSelect() = {
    df.select(count($"code"))//if code is null then it's not counted. if use '*' then count all rows
      .select(countDistinct("code"))//select count(distinct code) from some_table
      .select(approx_count_distinct("code", 0.1))//대략적인 count. 데이터가 클 경우, 정확하지 않지만, 빠르게 근사치를 얻고 싶을 때
      .select(first("code"))
      .select(last("code"))
      .select(min("code"))
      .select(max("code"))
      .select(sumDistinct("code"))
      .select(avg("code"))
      .select(sum('count), expr("avg(count)"), expr("count(distinct(age))"))//able to use aggregation function
  }

  def withAgg() = {
    df.agg(collect_list("value").as("list"))
    df.agg(collect_set("value").as("set"))
    df.agg(count("value").as("count"), expr("count(value)").as("count2"))
    df.agg(count("*").as("count"))
    df.agg("value" -> "avg", "value" -> "count")//column -> agg method name
    df.agg(sum(when($"result" === "SUCCESS", 1).otherwise(0)).as("success_count"))//sumif
    df.agg(count(when($"result" === "SUCCESS", true)).as("success_count"))//countif, if not add 'otherise', then it returns null if it's not matched

  }

  def makeListPerGroup = {
    //if you want to handle list by groups which is handled by each partition.
    //this may be best way to handle.
    //other ways may not be handled by each node per group.
    df.repartition($"name")
      .mapPartitions((rows: Iterator[Row]) =>
        rows.map(_.getAs[String](0))
      )


    //agg to list and map. change it to data set
    //WARNING : collect_list, collect_set bring data to driver node. so, it can make slow
    // collect_list를 mapPartitions으로 변환 했음에도 불구하고, 성능 개선이 되지 않은 경우가 있음.
    // collect_list를 할 때, shuffle이 일어날테고, 그게 속도저하의 문제인듯..
    val numDF = (1 to 100).toDF()
      .withColumn("ten", ($"value" / 10).cast(IntegerType))
    numDF
      .groupBy("ten")
      .agg(collect_list("value").as("list"))
      .agg(collect_list(struct(numDF.columns.map(col):_*)).as("all_list"))//make all column as list
      .map(r => r.getAs[List[Int]]("list").sum)
      .show(100)

    //the approach above use driver program, the below handle list on distributed processing
    //we have to consider partition as well. group by object's field may not be efficient. because it may cause full shuffle
    def someFunction(name: String, persons: Iterator[Person]) = {
      "???"
    }

    df.as[Person]
      .groupByKey(_.name)
      .mapGroups((name: String, persons: Iterator[Person]) => {
        someFunction(name, persons)
      })
    df.as[Person]
      .groupByKey(_.name)
      .mapGroups(someFunction)//able to use function name directly.

    //agg to list and convert list by udf.
    // - able to keep Dataframe
    val updateList = udf((list: mutable.WrappedArray[Int]) => list.sum)
    (1 to 100).toDF()
      .withColumn("ten", ($"value"/10).cast(IntegerType))
      .groupBy("ten")
      .agg(collect_list("value").as("list"))
      .withColumn("list", updateList($"list"))
      .show(100)
  }

  def group() = {
    df.groupBy("age").count()// (age, count), count()'s column name is 'count'
    df.groupBy().min("age")// agg for all rows.
    df.agg(min("age"), collect_set("age"))// same with `groupBy().min("age")`
  }

  /**
   * grouping set
   * - https://www.sqlservertutorial.net/sql-server-basics/sql-server-grouping-sets/
   */
  def groupingSet() = {
    //this is supported by sql only
    val dfNoNull = df.na.drop()
    dfNoNull.createOrReplaceTempView("dfNoNull")
    spark.sql("select customerId, stockCode, sum(quantity) from dfNoNull\n" +
      "group by customerId, stockCode grouping sets((customerId, stockCode), (stockCode), ())\n" +
      "order by sum(quantity) desc, customerId desc, stockCode desc")
  }

  /**
   * this is for grouping set
   */
  def rollUp() = {
    val dfNoNull = df.na.drop()
    dfNoNull
      .rollup("date", "country")
      .agg(sum("quantity"))
      .selectExpr("date", "country", "`sum(quantity)` as total_quantity")//sum의 이름을 바꿀려고, select문을 쓴 것 같은데..??
      .orderBy("date")
      .show()
    //date+country별, date별, 전체에 대한 총양을 구하기
  }

  def cube() = {
    val dfNoNull = df.na.drop()
    dfNoNull
      .cube("date", "country")
      .agg(sum("quantity"))
      .agg(grouping_id(), sum("quantity"))//show grouping Id.
      .agg(grouping("date"), sum("quantity"))//aggregated or not.
      .orderBy("date")
      .show()
    //date+country별, date별, country별, 전체에 대한 총양을 구하기
  }

  /**
   * cube와 rollup의 차이 : https://www.mikulskibartosz.name/cube-and-rollup-in-apache-spark/#:~:text=Both%20functions%20are%20used%20to,from%20the%20first%20given%20column.
CUBE	GROUP BY
year, month, day	SELECT COUNT(*) FROM table GROUP BY year, month, day
year, month	SELECT COUNT(*) FROM table GROUP BY year, month
year, day	SELECT COUNT(*) FROM table GROUP BY year, day
year	SELECT COUNT(*) FROM table GROUP BY year
month, day	SELECT COUNT(*) FROM table GROUP BY month, day
month	SELECT COUNT(*) FROM table GROUP BY month
day	SELECT COUNT(*) FROM table GROUP BY day
null, null, null	SELECT COUNT(*) FROM table
If I used the rollup function, the grouping would look like this:

ROLLUP	GROUP BY
year, month, day	SELECT COUNT(*) FROM table GROUP BY year, month, day
year, month	SELECT COUNT(*) FROM table GROUP BY year, month
year	SELECT COUNT(*) FROM table GROUP BY year
null	SELECT COUNT(*) FROM table
   */

  /**
   * https://databricks.com/blog/2016/02/09/reshaping-data-with-pivot-in-apache-spark.html
   * 특정 컬럼의 값들을 행과 열로 변환하고, 해당 행과 열에 대한 특정 값을 보여준다.
   * - groupBy()를 하는 컬럼의 값이 행이 되고,
   * - pivot()를 하는 컬럼의 값이 열이 된다.
   * - 마지막에 어떤 값을 보여줄지 정의한다 (ex: sum()). 값이 여러개면, 열에 pivot_v1, pivot_v2 같은 식으로 열에 여러개의 컬럼이 표시된다.
   *
   * 예1
   * userId, date, country, quantity, price 인 테이블을
   * date, USA_sum(quantity), KOREA_sum(quantity), USA_sum(price), KOREA_sum(price) 인 테이블로 변환(각 날짜별, 나라들의 가격 및 양의 합계)
   * groupBy(date).pivot(country).sum() //다른 각 컬럼들의 합계.
   *
   * 예2
   * userId, movie, rating 테이플을
   * userId, movie들 컬럼(컬럼의 값은 rating) 인 테이블로 변환(유저별, 각 movie의 rating을 보여줌)
   * groupBy(userId), pivot(movie), first(rating)
   * 예3
   * 트랜젝션 테이블에서, 각유저의 트랜젝션 카테고리별 aggregation 데이터를 볼때
   * groupBy(userId).pivot(category).agg(agg1,agg2,agg3)
   */
  def pivot() = {
    df
      .groupBy("date")
      .pivot("country")
      .sum()
    //날짜별, 나라별, 합계 테이블을 만든다
  }


  /**
   * UDAF : User defined aggregation function
   * 사용자 정의 집계 함수
   */
}
