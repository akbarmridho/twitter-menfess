from dotenv import load_dotenv
from application.helpers import project_path
from application.twitter import UserConfig, API
from os import getenv


def register_webhook():
    load_dotenv(project_path('.env'))

    host = input('Webhook url: ')
    endpoint = '/service/listen'

    webhook_url = host + endpoint

    TWITTER_OAUTH_KEY = getenv('TWITTER_OAUTH_KEY')
    TWITTER_OAUTH_SECRET = getenv('TWITTER_OAUTH_SECRET')

    if not (TWITTER_OAUTH_KEY and TWITTER_OAUTH_SECRET):
        raise Exception()

    config = UserConfig(TWITTER_OAUTH_KEY, TWITTER_OAUTH_SECRET)

    client = API(config)

    response = client.register_webhooks(webhook_url)

    if response.ok:
        print('Webhook registered')
    else:
        print('Cannot register webhook')

    print(response.text)
