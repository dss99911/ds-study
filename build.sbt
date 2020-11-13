name := "scala_example"

version := "0.1"

scalaVersion := "2.13.3"




//custom maven repo with java jar
//resolvers += "nexus-release" at "https://nexus.aaa.cc/nexus/content/repositories/releases"
//libraryDependencies ++= Seq("group-name" % "library-name" % "2.3.4")

//add scala library
libraryDependencies += "org.scala-lang.modules" %% "scala-parser-combinators" % "1.1.2"