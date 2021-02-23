package spark

import org.apache.spark.sql.functions.{corr, covar_pop, covar_samp, kurtosis, skewness, stddev, stddev_pop, stddev_samp, var_pop, var_samp, variance}

class Stat {
  val df = Read.getCsv()
  /**
   * 두 컬럼 사이의 영향도 비교
   * 공분산(covariance)
   *  - 표본공분산(sample covariance)
   *  - 모공분산(population covariance)
   * 상관 계수(Correlation coefficient) : 두 값의 관계를 알고 싶을 때 사용.
   */
  def correlationCoefficient() = {


    //갯수와 가격과의 상관 관계를 알고 싶을 때
    df.stat.corr("quantity", "unitPrice")
    df.select(corr("quantity", "unitPrice"))
    df.select(covar_pop("quantity", "unitPrice"))
    df.select(covar_samp("quantity", "unitPrice"))
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

  /**
   * There is two type of standard deviation.
   * - 표본표준편차(sample standard deviation)
   * - 모표준편차(population standard deviation)
   * todo check what is the difference
   */
  def standardDeviation() = {
    df.select(var_pop("dd"), var_samp("dd"))
      .select(stddev_pop("dd"), stddev_samp("dd"))
      .select(stddev("dd"), variance("dd"))//use sample standard deviation
  }

  /**
   * 비대칭도(skewness) : 데이터 평균의 비대칭 정도 측정
   * 첨도(kurtosis) : 데이터 끝 부분 측정
   *
   * 확률변수(random variable)의 환률분포(probability distribution)로 데이터 모델링할 때 특히 중요
   */
  def skewnessKurtosis() = {
    df.select(skewness("dd"), kurtosis("dd"))
  }

}
