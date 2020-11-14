name := "scala_example"

version := "0.1"

scalaVersion := "2.12.12"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.0.0" % "provided"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.0.0" % "provided"

//custom maven repo with java jar
//resolvers += "nexus-release" at "https://nexus.aaa.cc/nexus/content/repositories/releases"
//libraryDependencies ++= Seq("group-name" % "library-name" % "2.3.4")