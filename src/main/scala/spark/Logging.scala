package spark

import org.apache.log4j.{Level, Logger}

class Logging {
  //diable spark logs.
  Logger.getLogger("org").setLevel(Level.OFF)
  Logger.getLogger("akka").setLevel(Level.OFF)
}
