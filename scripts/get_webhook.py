from application.twitter import UserConfig, API
from os import getenv


def get_webhook():
    TWITTER_OAUTH_KEY = getenv('TWITTER_OAUTH_KEY')
    TWITTER_OAUTH_SECRET = getenv('TWITTER_OAUTH_SECRET')

    if not (TWITTER_OAUTH_KEY and TWITTER_OAUTH_SECRET):
        raise Exception()

    config = UserConfig(TWITTER_OAUTH_KEY, TWITTER_OAUTH_SECRET)

    client = API(config)

    response = client.get_webhooks()

    if response.ok:
        print('Webhook registered')
    else:
        print('Cannot register webhook')

    print(response.text)
