
## Hooking
install Frida on spark server. and hooking functions

## Debugging
https://sparkbyexamples.com/spark/how-to-debug-spark-application-locally-or-remote/
```shell
spark-submit \
--name SparkByExamples.com \
--class org.sparkbyexamples.SparkWordCountExample \
--conf spark.driver.extraJavaOptions=-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005
spark-by-examples.jar
```

## log
```shell
yarn logs -applicationId <app ID>

# show container ids
yarn logs -applicationId <Application ID> -show_application_log_info

# see container logs
yarn logs -applicationId <Application ID> -containerId <Container ID>

# see laster bytes log
yarn logs -applicationId <Application ID> -containerId <Container ID> -size <bytes>

```
- able to see executor side container logs
- https://spark.apache.org/docs/latest/running-on-yarn.html#debugging-your-application