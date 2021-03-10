name := "spark_study"

version := "0.1"

scalaVersion := "2.12.12"

mainClass in (Compile, run) := Some("spark.MainApp")
mainClass in (Compile, packageBin) := Some("spark.MainApp")
libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.1.1" % "provided",
  "org.apache.spark" %% "spark-sql" % "3.1.1" % "provided",
  "org.scalaj" %% "scalaj-http" % "2.4.2",
  "com.typesafe" % "config" % "1.4.1",
  "com.fasterxml.jackson.core" % "jackson-databind" % "2.11.3",

  //https://docs.scala-lang.org/getting-started/intellij-track/testing-scala-in-intellij-with-scalatest.html#conclusion
  "org.scalatest" %% "scalatest" % "3.0.8" % Test,
)

//for Jackson
assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}


//custom maven repo with java jar
//resolvers += "nexus-release" at "https://nexus.aaa.cc/nexus/content/repositories/releases"
//libraryDependencies ++= Seq("group-name" % "library-name" % "2.3.4")
