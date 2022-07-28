package spark.ml

import org.apache.spark.ml.{Pipeline, PipelineModel}
import org.apache.spark.ml.classification.{LogisticRegression, LogisticRegressionModel}
import org.apache.spark.ml.evaluation.BinaryClassificationEvaluator
import org.apache.spark.ml.feature.{HashingTF, Tokenizer}
import org.apache.spark.ml.linalg.Vector
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.ml.tuning.{CrossValidator, CrossValidatorModel, ParamGridBuilder}
import org.apache.spark.sql.{Row, SparkSession}

/**
 * https://spark.apache.org/docs/latest/ml-tuning.html#cross-validation
 * - train과 test data set을 알아서 나눠서, 테스트해서, 평균 정확도를 구한다.
 * - 여러 param들로 테스트해서, 가장 최적의 param을 구한다.
 *
 * - Thinking : train과 test를 나눠서 테스트하는 것을 효과적으로 하려면, train에 비슷한 결과를 내는 데이터의 중복을 줄여서 과적합을 줄여야 하지 않을까?
 *
 */
class ParameterTuning {

  def validate(spark: SparkSession) = {
    import spark.implicits._

    // Prepare training data from a list of (id, text, label) tuples.
    val training = spark.createDataFrame(Seq(
      (0L, "a b c d e spark", 1.0),
      (1L, "b d", 0.0),
      (2L, "spark f g h", 1.0),
      (3L, "hadoop mapreduce", 0.0),
      (4L, "b spark who", 1.0),
      (5L, "g d a y", 0.0),
      (6L, "spark fly", 1.0),
      (7L, "was mapreduce", 0.0),
      (8L, "e spark program", 1.0),
      (9L, "a e c l", 0.0),
      (10L, "spark compile", 1.0),
      (11L, "hadoop software", 0.0)
    )).toDF("id", "text", "label")

    // Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
    val tokenizer = new Tokenizer()
      .setInputCol("text")
      .setOutputCol("words")
    val hashingTF = new HashingTF()
      .setInputCol(tokenizer.getOutputCol)
      .setOutputCol("features")
    val lr = new LogisticRegression()
      .setMaxIter(10)
    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, hashingTF, lr))


    // this grid will have 3 x 2 = 6 parameter settings for CrossValidator to choose from.
    val paramGrid = new ParamGridBuilder()
      .addGrid(hashingTF.numFeatures, Array(10, 100, 1000))
      .addGrid(lr.regParam, Array(0.1, 0.01))
      .build()


    //(train, test)셋 ( fold-1 : 1로 나눔)
    // 각 fold를 test셋으로 하는 학습을 fold갯수만큼 진행
    //folding 갯수(2) * grid의 갯수(3*2) = 총 학습 횟수(12)
    //bestParam으로 전체 데이터를 다시 학습한다(fold별 모델 성능의 평균이 가장 좋은 parameter셋을 선정한다)
    //pipeline의 뒤에 있는 것들의 파라미터만 변경한다면, 앞 스텝의 경우, 매 파라미터 테스트할 때마다 재학습하진 않고, 학습된 것을 사용하는 것 같음(skip이 뜸)
    val cv = new CrossValidator()
      .setEstimator(pipeline)

      // default metric is areaUnderROC.
      //label과 rawPredictionCol명을 변경한 경우, setLableCol, setRawPredictionCol 설정 필요.
      .setEvaluator(new BinaryClassificationEvaluator)
      .setEstimatorParamMaps(paramGrid)
      .setNumFolds(3)  // Use 3+ in practice.
      .setParallelism(3)  // Evaluate up to 2 parameter settings in parallel

    // Run cross-validation, and choose the best set of parameters.
    val cvModel = cv.fit(training)
    val bestModel = cvModel.bestModel.asInstanceOf[PipelineModel].stages(2)
      .asInstanceOf[LogisticRegressionModel]
    val modelParams = bestModel.extractParamMap()

    val bestParams = cvModel.bestEstimatorParamMap

    // Prepare test documents, which are unlabeled (id, text) tuples.
    val test = spark.createDataFrame(Seq(
      (4L, "spark i j k"),
      (5L, "l m n"),
      (6L, "mapreduce spark"),
      (7L, "apache hadoop")
    )).toDF("id", "text")

    // Make predictions on test documents. cvModel uses the best model found (lrModel).
    cvModel.transform(test)
      .select("id", "text", "probability", "prediction")
      .collect()
      .foreach { case Row(id: Long, text: String, prob: Vector, prediction: Double) =>
        println(s"($id, $text) --> prob=$prob, prediction=$prediction")
      }
  }

  implicit class BestParamMapCrossValidatorModel(cvModel: CrossValidatorModel) {
    def bestEstimatorParamMap: ParamMap = {
      if (cvModel.getEvaluator.isLargerBetter) {
        cvModel.getEstimatorParamMaps
          .zip(cvModel.avgMetrics)
          .maxBy(_._2)
          ._1
      } else {
        cvModel.getEstimatorParamMaps
          .zip(cvModel.avgMetrics)
          .minBy(_._2)
          ._1
      }
    }
  }
}
