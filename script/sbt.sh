#when sbt files are changed. reload
sbt reload

#Assemble jar
sbt package

#If assemble with sbt-assembly
sbt assembly

#jar path
scp -i ~/some.pem target/scala-2.12/some.jar hadoop@1.0.0.1:/home/hadoop/some.jar

#clean
#if build several times, out of memory error occurs
sbt clean