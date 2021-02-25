#!/bin/sh

export PROPERTIES_FILE="/etc/spark/conf/spark-defaults.conf"
export EXEC_JAR="s3://some.jar"

DT=$1
DATA=$2

/usr/lib/spark/bin/spark-submit \
--properties-file ${PROPERTIES_FILE} \
--class com.MainClass \
--master "master-url" \
--deploy-mode "deploy-mode" \
--conf key=value \
--driver-java-options "-Dconfig.resource=application-dev.conf" \
${EXEC_JAR} "${DT}" "${DATA}"
