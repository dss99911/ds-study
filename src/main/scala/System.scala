import scala.util.Properties

class System {
  //show scala version
  Properties.versionString

  //show current path
  System.getProperty("user.dir")

  def execute(command: String): Unit = {
    import scala.sys.process._
    command.!  //print output
    command.!!  //return output
  }
}
