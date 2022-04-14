package spark.ml

import org.apache.spark.ml.functions.vector_to_array
import org.apache.spark.ml.linalg.Vectors
import org.apache.spark.sql.functions.col

class VectorSample {
  def sparse() = {
    //sparse는 드문드문 값을 설정하고 싶을 때 사용한다. 4의 크기의 배열에 0번째에 1.0을 3번째에 -2.0을 설정하고, 나머지는 0을 설정한다는 의미
    val sparseVector = Vectors.sparse(4, Seq((0, 1.0), (3, -2.0)))
    val sparseVector2 = Vectors.sparse(4, Array(0, 3), Array(1.0, -2.0))//위의 방식과 결과는 같지만, 표현이 다름
    val denseVector = Vectors.dense(1.0, 0, 0, -2.0)//위의 방식과 결과는 같지만, 표현이 다름

    sparseVector.toDense
    denseVector.toSparse
  }

  def vector2array() = {
    vector_to_array(col("column"))
  }
}
