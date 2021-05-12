from pyspark.sql import DataFrame
from slackclient import SlackClient

def send_slack_message(text, channel = "@hyun", username = "", icon_emoji = ""):
    slack = SlackClient("oauth-token")

    if isinstance(text, DataFrame):
        text = text._jdf.showString(20, int(False), False)

    slack.api_call(
        'chat.postMessage',
        channel=channel,
        text=text,
        username=username,
        icon_emoji=icon_emoji
    )
