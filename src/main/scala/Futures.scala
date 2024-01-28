import java.util.concurrent.{LinkedBlockingQueue, ThreadPoolExecutor, TimeUnit}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.{FiniteDuration, SECONDS}
import scala.concurrent.{Await, ExecutionContext, Future}
import scala.util.{Failure, Success, Try}

/**
 * https://docs.scala-lang.org/overviews/scala-book/futures.html
 */
object Futures extends App {

  // use this to determine the “delta time” below
  val startTime = currentTime

  // (a) create three futures
  val aaplFuture = getStockPrice("AAPL")
  val amznFuture = getStockPrice("AMZN")
  val googFuture = getStockPrice("GOOG")

  // (b) get a combined result in a for-expression
  // use global executor
  val result: Future[(Double, Double, Double)] = for {
    aapl <- aaplFuture
    amzn <- amznFuture
    goog <- googFuture
  } yield (aapl, amzn, goog)

  // (c) do whatever you need to do with the results
  result.onComplete {
    case Success(x) => {
      val totalTime = deltaTime(startTime)
      println(s"In Success case, time delta: ${totalTime}")
      println(s"The stock prices are: $x")
    }
    case Failure(e) => e.printStackTrace
  }

  // important for a short parallel demo: you need to keep
  // the jvm’s main thread alive
  sleep(5000)

  def sleep(time: Long): Unit = Thread.sleep(time)

  // a simulated web service
  def getStockPrice(stockSymbol: String): Future[Double] = Future {
    val r = scala.util.Random
    val randomSleepTime = r.nextInt(3000)
    println(s"For $stockSymbol, sleep time is $randomSleepTime")
    val randomPrice = r.nextDouble * 1000
    sleep(randomSleepTime)
    randomPrice
  }

  def currentTime = System.currentTimeMillis()
  def deltaTime(t0: Long) = currentTime - t0


  // define executor
  val executorService = new ThreadPoolExecutor(3, 10,
    600000L, TimeUnit.MILLISECONDS,
    new LinkedBlockingQueue[Runnable](128), new ThreadPoolExecutor.DiscardPolicy())
  implicit val executionContext = ExecutionContext.fromExecutorService(executorService)



  def futures() = {
    List(
      Future {
        sleep(1000)
        println("1")
        Await.result(Future {
          sleep(1000)
//          1 / 0
          println("1.1")

          Await.result(Future {
            sleep(3000)
                      1 / 0
            println("1.2")

          }, FiniteDuration(1, SECONDS))

        }, FiniteDuration(5, SECONDS))

        println("1 finish again")
      },
      Future {
        sleep(1000)
        println("2")
        Await.result(Future {
          sleep(1000)
          println("2.1")
        }, FiniteDuration(5, SECONDS))
      }
    ).foreach(future => Await.result(future, FiniteDuration(5, SECONDS)))

    println("processed")
  }

  // need to use Try for catching the failure.
  // if no Try, just stop running
  Try(futures()) match {
    case Success(_) => {
      print("1 success")
    }
    case Failure(e) => {
      print("1 failure " + e)
    }
  }

  println("finished")

  // if executor running, app is not terminated even if all is processed. so, need to terminate manually.
  executorService.shutdown()
  if (!executorService.awaitTermination(60, TimeUnit.SECONDS)) {
    executorService.shutdownNow
  }

}