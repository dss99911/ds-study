import os

# get slack api token from environment variable
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')

# if를 입력하면, 아래가 자동 완성 됨
if not SLACK_API_TOKEN:
    print("SLACK_API_TOKEN environment variable not set")
    exit(1)