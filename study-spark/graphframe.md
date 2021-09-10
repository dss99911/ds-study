# GraphFrame
- it's Dataframe version of GraphX(which is used with RDD)
- currently partitioning missing on 0.8.0 version
  
## Docs
* https://graphframes.github.io/graphframes/docs/_site/index.html
* https://graphframes.github.io/graphframes/docs/_site/quick-start.html
* https://graphframes.github.io/graphframes/docs/_site/user-guide.html
* https://databricks.com/blog/2016/03/16/on-time-flight-performance-with-graphframes-for-apache-spark.html


## Configuration
- https://graphframes.github.io/graphframes/docs/_site/quick-start.html#getting-started-with-apache-spark-and-spark-packages
- add the package
- check latest version https://mvnrepository.com/artifact/graphframes/graphframes
```shell
park-shell --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11

```

### add dependency (for IDE to recognize library)
repo : `https://repos.spark-packages.org/`
    - for Big Data Tools. it's not working if doesn't add this.
```sbt
libraryDependencies += "graphframes" % "graphframes" % "0.8.1-spark3.0-s_2.12"

```
