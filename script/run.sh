set -e
cd ..
sbt package
spark-submit  target/scala-2.12/spark_study_2.12-0.1.jar

#sbt assembly # making fat-jar
#spark-submit  target/scala-2.12/spark_study-assembly-0.1.jar