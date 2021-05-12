package util

import com.typesafe.config.ConfigFactory
import scalaj.http.{Http, HttpOptions}

object Slack {
  val conf = ConfigFactory.load
  val SLACK_WEBHOOK_URL = ""
  val USERNAME = ""
  val CHANNEL = ""

  def sendMessage(emoji: String, color: String, title: String, message: String) = {
    val body=s"""{"channel":"#$CHANNEL","username":"$USERNAME","icon_emoji":"$emoji","attachments": [{"color": "$color","title": "$title","text": "$message"}]}"""

    println(body)

    Http(SLACK_WEBHOOK_URL).postData(body)
      .header("Content-Type", "application/json")
      .header("Charset", "UTF-8")
      .option(HttpOptions.readTimeout(10000)).asString
  }
}

