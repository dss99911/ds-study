package spark.ml

import ml.dmlc.xgboost4j.scala.spark.XGBoostClassifier
import org.apache.spark.ml.feature.{StringIndexer, VectorAssembler}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, when}
import org.apache.spark.sql.types.{DoubleType, StringType, StructField, StructType}

/**
 * https://github.com/dmlc/xgboost/blob/master/jvm-packages/xgboost4j-example/src/main/scala/ml/dmlc/xgboost4j/scala/example/spark/SparkTraining.scala
 * https://xgboost.readthedocs.io/en/stable/jvm/xgboost4j_spark_tutorial.html
 * https://github.com/NVIDIA/spark-xgboost-examples/blob/spark-3/examples/notebooks/scala/agaricus-gpu.ipynb
 */
object XgboostSample {
  // - 학습만 하는 경우(전처리는 이전 프로세스에서 진행)
  // - pipeline에 preprocessing까지 포함하는 경우
  //    - eval_set을 쓸 수 없음(eval_set의 데이터는 이미 피쳐가 생성된 상태의 데이터야함)

  def iris(spark: SparkSession): Unit = {
    val schema = new StructType(Array(
      StructField("sepal length", DoubleType, true),
      StructField("sepal width", DoubleType, true),
      StructField("petal length", DoubleType, true),
      StructField("petal width", DoubleType, true),
      StructField("class", StringType, true)))
    val rawInput = spark.read.schema(schema).csv("data/iris.data")

    // transform class to index to make xgboost happy
    val stringIndexer = new StringIndexer()
      .setInputCol("class")
      .setOutputCol("classIndex")
      .fit(rawInput)
    val labelTransformed = stringIndexer.transform(rawInput).drop("class")
    // compose all feature columns as vector
    val vectorAssembler = new VectorAssembler().
      setInputCols(Array("sepal length", "sepal width", "petal length", "petal width")).
      setOutputCol("features")
    val xgbInput = vectorAssembler.transform(labelTransformed)
      .select("features", "classIndex")
      .withColumn("classIndex", when(col("classIndex") > 2, 1.0).otherwise(0.0))

    val Array(train, eval1, eval2, test) = xgbInput.randomSplit(Array(0.6, 0.2, 0.1, 0.1))


    val xgbParam = Map("eta" -> 0.1f,
      "max_depth" -> 2,
      "objective" -> "multi:softprob",
      "num_class" -> 3,
      "num_round" -> 100,
      "num_workers" -> 1,
      "tree_method" -> "auto",
      "eval_sets" -> Map("eval1" -> eval1, "eval2" -> eval2)
    )

    val xgbClassifier = new XGBoostClassifier(xgbParam)
      .setFeaturesCol("features")
      .setLabelCol("classIndex")
    val xgbClassificationModel = xgbClassifier.fit(train)
    val results = xgbClassificationModel.transform(test)
    results.show()

  }
}
