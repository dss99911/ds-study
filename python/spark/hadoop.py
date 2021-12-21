
#check file exists on s3
path = sc._jvm.org.apache.hadoop.fs.Path("s3://path")
fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(path.toUri(), sc._jsc.hadoopConfiguration())
fs.exists(path)