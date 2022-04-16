import sbt.Keys.libraryDependencies

name := "spark_study"

version := "0.1"

scalaVersion := "2.12.12"

mainClass in (Compile, run) := Some("spark.MainApp")
mainClass in (Compile, packageBin) := Some("spark.MainApp")
resolvers += "spark-packges" at "https://repos.spark-packages.org"
resolvers += "confluent" at "https://packages.confluent.io/maven/"

libraryDependencies ++={
  val sparkVer = "3.1.2"
  Seq(
    "org.apache.spark" %% "spark-core" % sparkVer % "provided",// provided추가하면, assembly를 해도, 추가를 안함
    "org.apache.spark" %% "spark-sql" % sparkVer % "provided",
    "org.apache.spark" %% "spark-mllib" % sparkVer % "provided",
    "org.scalaj" %% "scalaj-http" % "2.4.2",
    "com.typesafe" % "config" % "1.4.1",
    "com.fasterxml.jackson.core" % "jackson-databind" % "2.11.3",

    //xgboost https://mvnrepository.com/artifact/com.nvidia/xgboost4j-spark_3.0
    //여기에 emr버전별 사용 jar가 있음 : https://nvidia.github.io/spark-rapids/docs/get-started/getting-started-aws-emr.html
    //scala 3.0만 있어서, maven에서 직접 참고하면 에러남.
    // lib폴더에 jar파일 추가만 하면 아래 추가 안해도 자동으로 인식함
    // todo 1.6.0이 emr등에서 잘 작동하면 변경
    //"com.nvidia" %% "xgboost4j-spark" % "1.2.0-0.1.0" from "file:///Users/hyun.kim/xgboost4j-spark_3.0-1.2.0-0.1.0.jar",
    //Spark NLP
    "com.johnsnowlabs.nlp" %% "spark-nlp" % "3.4.2",

    //https://docs.scala-lang.org/getting-started/intellij-track/testing-scala-in-intellij-with-scalatest.html#conclusion
    "org.scalatest" %% "scalatest" % "3.2.5" % Test,

    /*TODO delta libraries are not working for fat jar. fix it!*/
    "io.delta" %% "delta-core" % "0.8.0",
    "graphframes" % "graphframes" % "0.8.1-spark3.0-s_2.12",

    //SchemaRegistry for streaming
    "io.confluent" % "kafka-schema-registry-client" % "5.5.0",
    "za.co.absa" %% "abris" % "4.2.0",
  )
}

//for Jackson
assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}


//custom maven repo with java jar
//resolvers += "nexus-release" at "https://nexus.aaa.cc/nexus/content/repositories/releases"
//libraryDependencies ++= Seq("group-name" % "library-name" % "2.3.4")
