import org.scalatest._
import org.apache.spark.sql.{SQLContext, SQLImplicits, SparkSession}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should

abstract class BaseSpec extends AnyFlatSpec with BeforeAndAfterEach with should.Matchers {
  var spark: SparkSession = _

  object testImplicits extends SQLImplicits with Serializable {
    protected override def _sqlContext: SQLContext = spark.sqlContext
  }

  override protected def beforeEach(): Unit = {
    super.beforeEach()


    spark = SparkSession
      .builder()
      .appName("testing")
      .config("spark.driver.host", "127.0.0.1")
      .master("local")
      .config("spark.driver.allowMultipleContexts", "false")
      .getOrCreate()

  }

}
