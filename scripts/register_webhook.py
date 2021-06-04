from dotenv import load_dotenv
from application.helpers import project_path
from application.twitter import UserConfig, API
from os import getenv

load_dotenv(project_path('.env'))

webhook_url = input('Webhook url: ')

config = UserConfig(getenv('TWITTER_OAUTH_KEY', ''),
                    getenv('TWITTER_OAUTH_SECRET', ''))

client = API(config)

response = client.register_webhooks(webhook_url)

if response.ok:
    print('Webhook registered')
else:
    print('Cannot register webhook')

print(response.text)
