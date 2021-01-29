/* SimpleApp.kt */
@file:JvmName("SimpleApp")
import org.jetbrains.kotlinx.spark.api.*

fun main() {
    val logFile = "README.md" // Change to your Spark Home path
    withSpark(props = mapOf("spark.driver.host" to "127.0.0.1")) {
        spark.read().textFile(logFile).withCached {
            val numAs = filter { it.contains("a") }.count()
            val numBs = filter { it.contains("b") }.count()
            println("Lines with a: $numAs, lines with b: $numBs")
        }
    }
}