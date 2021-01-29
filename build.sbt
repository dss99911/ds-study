name := "scala_example"

version := "0.1"

scalaVersion := "2.12.12"

mainClass in (Compile, run) := Some("spark.MainApp")
mainClass in (Compile, packageBin) := Some("spark.MainApp")
libraryDependencies += "org.apache.spark" %% "spark-core" % "3.0.0" % "provided"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.0.0" % "provided"
libraryDependencies += "org.scalaj" %% "scalaj-http" % "2.4.2"
libraryDependencies += "com.typesafe" % "config" % "1.4.1"
libraryDependencies += "com.fasterxml.jackson.core" % "jackson-databind" % "2.11.3"

//custom maven repo with java jar
//resolvers += "nexus-release" at "https://nexus.aaa.cc/nexus/content/repositories/releases"
//libraryDependencies ++= Seq("group-name" % "library-name" % "2.3.4")
