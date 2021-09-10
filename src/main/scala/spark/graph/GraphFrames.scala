package spark.graph

import org.apache.spark.sql.Column
import org.apache.spark.sql.functions.{col, lit, sum, when}
import spark.SparkSessions


/**
*Vertex DataFrame: A vertex DataFrame should contain a special column named “id” which specifies unique IDs for each vertex in the graph.
*Edge DataFrame: An edge DataFrame should contain two special columns: “src” (source vertex ID of edge) and “dst” (destination vertex ID of edge).
 * https://graphframes.github.io/graphframes/docs/_site/user-guide.html
 */
class GraphFrames {
  val spark = SparkSessions.createSparkSession()
  def tutorials = {
    // import graphframes package
    import org.graphframes._
    // Create a Vertex DataFrame with unique ID column "id"
    val v = spark.createDataFrame(List(
      ("a", "Alice", 34),
      ("b", "Bob", 36),
      ("c", "Charlie", 30),
      ("d", "dd", 30),
      ("e", "ee", 30),
    )).toDF("id", "name", "age")
    // Create an Edge DataFrame with "src" and "dst" columns
    val e = spark.createDataFrame(List(
      ("a", "b", "friend"),
      ("b", "c", "follow"),
      ("c", "b", "follow"),
      ("b", "d", "follow"),
      ("d", "e", "follow"),
      ("e", "b", "follow"),
    )).toDF("src", "dst", "relationship")
    // Create a GraphFrame
    import org.graphframes.GraphFrame
    val g = GraphFrame(v, e)

    // Query: Get in-degree of each vertex.
    // 자신을 참조하는 vertex 수. 자기가 참조하는 vertex는 포함 안됨.
    // 다른 곳에서 참조하여, 자신을 참조하므로, 화살표 방향이 자신이라서, 화살표가 안으로 향한다고 해서 inDegree인듯?
    g.inDegrees.show()

    //모든 방향의 수
    g.degrees.show()

    //밖으로 향하는 참조 수
    g.outDegrees.show()

    // Query: Count the number of "follow" connections in the graph.
    print(g.edges.filter("relationship = 'follow'").count())

    // Run PageRank algorithm, and show results.
    // todo pageRank? 참조가 많은 경우 rank가 높은 듯. resetProbability의 0.01은 참조가 없는 경우.
    // d,c,e는 참조가 한번만 이러난 경우인데, c, d의 숫자가 미묘하게 큰데, 랭크가 큰 b한테서 참조가 일어났기 때문.
    // b는 3개의 vertex에게서 참조를 받고 있는데, 1.9로 이 수치의 의미가 무엇인지 모르겠음.
    val results = g.pageRank.resetProbability(0.01).maxIter(20).run()
    results.vertices.select("id", "pagerank").show()

    /**
     *
+---+--------+
| id|inDegree|
+---+--------+
|  d|       1|
|  b|       3|
|  c|       1|
|  e|       1|
+---+--------+

+---+--------------------+
| id|            pagerank|
+---+--------------------+
|  a|0.010000000000000005|
|  e|  0.9972317036228282|
|  b|  1.9967633398233573|
|  d|  0.9980024782769071|
|  c|  0.9980024782769071|
+---+--------------------+

     */
  }


  def get_vertices_edges() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    // Display the vertex and edge DataFrames
    g.vertices.show()
    // +--+-------+---+
    // |id|   name|age|
    // +--+-------+---+
    // | a|  Alice| 34|
    // | b|    Bob| 36|
    // | c|Charlie| 30|
    // | d|  David| 29|
    // | e| Esther| 32|
    // | f|  Fanny| 36|
    // | g|  Gabby| 60|
    // +--+-------+---+

    g.edges.show()
    // +---+---+------------+
    // |src|dst|relationship|
    // +---+---+------------+
    // |  a|  b|      friend|
    // |  b|  c|      follow|
    // |  c|  b|      follow|
    // |  f|  c|      follow|
    // |  e|  f|      follow|
    // |  e|  d|      friend|
    // |  d|  a|      friend|
    // |  a|  e|      friend|
    // +---+---+------------+
  }

  def find() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    // Search for pairs of vertices with edges in both directions between them.
    // (vertex)와 (edge)의 관계를 명시하면, 그와 일치하는 조합들을 찾아준다. 변수, a,b,e,e2 를 컬럼명으로 하여 DF 생성함
    val motifs = g.find("(a)-[e]->(b); (b)-[e2]->(a)")
    motifs.show()

    /**
    +----------------+--------------+----------------+--------------+
    |               a|             e|               b|            e2|
    +----------------+--------------+----------------+--------------+
    |    [b, Bob, 36]|[b, c, follow]|[c, Charlie, 30]|[c, b, follow]|
    |[c, Charlie, 30]|[c, b, follow]|    [b, Bob, 36]|[b, c, follow]|
    +----------------+--------------+----------------+--------------+
     */

    // More complex queries can be expressed by applying filters.
    motifs.filter("b.age > 30").show()
    /**

+----------------+--------------+------------+--------------+
|               a|             e|           b|            e2|
+----------------+--------------+------------+--------------+
|[c, Charlie, 30]|[c, b, follow]|[b, Bob, 36]|[b, c, follow]|
+----------------+--------------+------------+--------------+
     */

    val chain4 = g.find("(a)-[ab]->(b); (b)-[bc]->(c); (c)-[cd]->(d)")
    def sumFriends(cnt: Column, relationship: Column): Column = {
      when(relationship === "friend", cnt + 1).otherwise(cnt)
    }
    //  (b) Use sequence operation to apply method to sequence of elements in motif.
    //      In this case, the elements are the 3 edges.
    val condition = { Seq("ab", "bc", "cd")
      .foldLeft(lit(0))((cnt, e) => sumFriends(cnt, col(e)("relationship"))) }
    //  (c) Apply filter to DataFrame.
    val chainWith2Friends2 = chain4.where(condition >= 2)
  }


  def subgraph() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends

    // Select subgraph of users older than 30, and relationships of type "friend".
    // Drop isolated vertices (users) which are not contained in any edges (relationships).
    val g1 = g.filterVertices("age > 30").filterEdges("relationship = 'friend'").dropIsolatedVertices()
  }

  def subgraph_by_finding() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    // Select subgraph based on edges "e" of type "follow"
    // pointing from a younger user "a" to an older user "b".
    val paths = { g.find("(a)-[e]->(b)")
      .filter("e.relationship = 'follow'")
      .filter("a.age < b.age") }
    // "paths" contains vertex info. Extract the edges.
    val e2 = paths.select("e.src", "e.dst", "e.relationship")
    // In Spark 1.5+, the user may simplify this call:
    //  val e2 = paths.select("e.*")

    // Construct the subgraph
    val g2 = GraphFrame(g.vertices, e2)
  }

  /**
   * Breadth-first search (BFS) finds the shortest path(s) from one vertex (or a set of vertices) to another vertex (or a set of vertices)
   * 특정 조건에 해당하는 최단거리 구하기.
   */
  def bfs() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    // Search from "Esther" for users of age < 32.
    val paths = g.bfs.fromExpr("name = 'Esther'").toExpr("age < 32").run()
//    val paths = g.bfs.fromExpr("name = 'Alice'").toExpr("name = 'David'").run()
    paths.show()

    /* for Alice to David
+--------------+--------------+---------------+--------------+--------------+
|          from|            e0|             v1|            e1|            to|
+--------------+--------------+---------------+--------------+--------------+
|[a, Alice, 34]|[a, e, friend]|[e, Esther, 32]|[e, d, friend]|[d, David, 29]|
+--------------+--------------+---------------+--------------+--------------+
     */

    // Specify edge filters or max path lengths.
    { g.bfs.fromExpr("name = 'Esther'").toExpr("age < 32")
      .edgeFilter("relationship != 'friend'")
      .maxPathLength(3).run() }

  }

  /**
   * 최단거리 구하기
   * 각 vertex에서 landmark들과의 거리를 vertex별로 보여줌.
   */
  def shortestPath() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    val results = g.shortestPaths.landmarks(Seq("a", "d")).run()
    results.select("id", "distances").show()
    /*
+---+----------------+
| id|       distances|
+---+----------------+
|  b|              []|
|  e|[a -> 2, d -> 1]|
|  a|[a -> 0, d -> 2]|
|  f|              []|
|  g|              []|
|  d|[a -> 1, d -> 0]|
|  c|              []|
+---+----------------+
     */
  }

  /**
   * https://en.wikipedia.org/wiki/Component_(graph_theory)
   * - 연결이 있는 vertex들의 집합과 연결점이 전혀 없는 다른 vertex들의 집합이 있을 때, vertex들의 집합을 component라고 함
   */
  def component() = {
    //todo 아래와 같은 에러가 남.
    // Checkpoint directory is not set. Please set it first using sc.setCheckpointDir().

    import org.graphframes.{examples,GraphFrame}
    val g = examples.Graphs.friends  // get example graph
    val result = g.connectedComponents.run()
    result.select("id", "component").orderBy("component").show()

    //strongly connected

    val result2 = g.stronglyConnectedComponents.maxIter(10).run()
    result2.select("id", "component").orderBy("component").show()
  }

  /**
   * Label Propagation Algorithm (LPA)
   * https://en.wikipedia.org/wiki/Label_Propagation_Algorithm
   * 커뮤니티를 찾아준다는데..
   * (1) convergence is not guaranteed
   * (2) one can end up with trivial solutions (all nodes are identified into a single community)
   */
  def lpa() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    val result = g.labelPropagation.maxIter(5).run()
    result.select("id", "label").show()
  }

  /**
   * maxIter : The first one uses the org.apache.spark.graphx.graph interface with aggregateMessages and runs PageRank for a fixed number of iterations. This can be executed by setting maxIter.
   * tol : The second implementation uses the org.apache.spark.graphx.Pregel interface and runs PageRank until convergence and this can be run by setting tol.
   * parallelPersonalizedPageRank : Personalized PageRank is used by Twitter to present users with other accounts they may wish to follow.
   * https://en.wikipedia.org/wiki/PageRank
   */
  def pageRanks() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    // Run PageRank until convergence to tolerance "tol".
    val results = g.pageRank.resetProbability(0.15).tol(0.01).run()
    // Display resulting pageranks and final edge weights
    // Note that the displayed pagerank may be truncated, e.g., missing the E notation.
    // In Spark 1.5+, you can use show(truncate=false) to avoid truncation.
    results.vertices.select("id", "pagerank").show()
    results.edges.select("src", "dst", "weight").show()

    // Run PageRank for a fixed number of iterations.
    val results2 = g.pageRank.resetProbability(0.15).maxIter(10).run()

    // Run PageRank personalized for vertex "a"
    val results3 = g.pageRank.resetProbability(0.15).maxIter(10).sourceId("a").run()

    // Run PageRank personalized for vertex ["a", "b", "c", "d"] in parallel
    val results4 = g.parallelPersonalizedPageRank.resetProbability(0.15).maxIter(10).sourceIds(Array("a", "b", "c", "d")).run()
  }

  def triangleCount() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    val results = g.triangleCount.run()
    results.select("id", "count").show()
    /*
+---+-----+
| id|count|
+---+-----+
|  a|    1|
|  b|    0|
|  c|    0|
|  d|    1|
|  e|    1|
|  f|    0|
|  g|    0|
+---+-----+
     */
  }

  def saveLoad() = {
    import org.graphframes.{examples,GraphFrame}
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    // Save vertices and edges as Parquet to some location.
    g.vertices.write.parquet("hdfs://myLocation/vertices")
    g.edges.write.parquet("hdfs://myLocation/edges")

    // Load the vertices and edges back.
    val sameV = spark.read.parquet("hdfs://myLocation/vertices")
    val sameE = spark.read.parquet("hdfs://myLocation/edges")

    // Create an identical GraphFrame.
    val sameG = GraphFrame(sameV, sameE)
  }

  /**
   * 인근 연결된 vertex에 자신의 값을 전달한다. 각 vertex는 받은 값을 aggregation한다.
   * 주변 사람들의 aggregate된 정보를 구할 때 쓰는듯(주변 사람들의 평균 나이 등)
   */
  def aggregateMessage() = {
    import org.graphframes.{examples,GraphFrame}
    import org.graphframes.lib.AggregateMessages
    val g: GraphFrame = examples.Graphs.friends  // get example graph

    // We will use AggregateMessages utilities later, so name it "AM" for short.
    val AM = AggregateMessages

    // For each user, sum the ages of the adjacent users.
    val msgToSrc = AM.dst("age")
    val msgToDst = AM.src("age")
    val agg = { g.aggregateMessages
      .sendToSrc(msgToSrc)  // send destination user's age to source
      .sendToDst(msgToDst)  // send source user's age to destination
      .agg(sum(AM.msg).as("summedAges")) } // sum up ages, stored in AM.msg column
    agg.show()

    /*
sendToDst
+---+----------+
| id|summedAges|
+---+----------+
|  d|        32|
|  a|        29|
|  f|        32|
|  b|        64|
|  c|        72|
|  e|        34|
+---+----------+
sendToSrc
+---+----------+
| id|summedAges|
+---+----------+
|  d|        34|
|  a|        68|
|  f|        30|
|  b|        30|
|  c|        36|
|  e|        65|
+---+----------+
sendToDst, sendToSrc
+---+----------+
| id|summedAges|
+---+----------+
|  d|        66|
|  a|        97|
|  f|        62|
|  b|        94|
|  c|       108|
|  e|        99|
+---+----------+
     */
  }
}
