package spark.ml

import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.regression.LinearRegression
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}
import org.apache.spark.sql.SparkSession

/**
 * TrainValidationSplit
 * - Train과 Test데이터 셋으로 나눔(CrossValidator와 동일)
 * - 여러 params중 최적의 param을 구함(CrossValidator와 동일)
 * - 한번만 체크함(Train과 test 데이터를 나눠서 k번 시도하는 CrossVlidator와 달리, 한번만 체크)
 *    - 작업량이 그만큼 줄어듬
 *    - 신뢰도는 그만큼 하락함(그래서, 데이터가 충분히 많을 때만 사용할 것)
 */
class TrainValidationSplitSample {
  def validate(spark: SparkSession) = {


    // Prepare training and test data.
    val data = spark.read.format("libsvm").load("data/mllib/sample_linear_regression_data.txt")
    val Array(training, test) = data.randomSplit(Array(0.9, 0.1), seed = 12345)

    val lr = new LinearRegression()
      .setMaxIter(10)

    // We use a ParamGridBuilder to construct a grid of parameters to search over.
    // TrainValidationSplit will try all combinations of values and determine best model using
    // the evaluator.
    val paramGrid = new ParamGridBuilder()
      .addGrid(lr.regParam, Array(0.1, 0.01))
      .addGrid(lr.fitIntercept)
      .addGrid(lr.elasticNetParam, Array(0.0, 0.5, 1.0))
      .build()

    // In this case the estimator is simply the linear regression.
    // A TrainValidationSplit requires an Estimator, a set of Estimator ParamMaps, and an Evaluator.
    val trainValidationSplit = new TrainValidationSplit()
      .setEstimator(lr)
      .setEvaluator(new RegressionEvaluator)
      .setEstimatorParamMaps(paramGrid)
      // 80% of the data will be used for training and the remaining 20% for validation.
      .setTrainRatio(0.8)
      // Evaluate up to 2 parameter settings in parallel
      .setParallelism(2)

    // Run train validation split, and choose the best set of parameters.
    val model = trainValidationSplit.fit(training)

    // Make predictions on test data. model is the model with combination of parameters
    // that performed best.
    model.transform(test)
      .select("features", "label", "prediction")
      .show()
  }

}
