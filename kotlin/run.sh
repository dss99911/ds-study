./gradlew shadowJar
spark-submit --class "SimpleApp" --master local build/libs/kotlin-1.0-SNAPSHOT-all.jar