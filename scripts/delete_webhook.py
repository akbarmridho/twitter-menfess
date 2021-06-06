from application.twitter import UserConfig, API
from os import getenv


def delete_webhook():
    webhook_id = getenv('WEBHOOK_ID')

    if not webhook_id:
        raise Exception('Webhook id not found')

    TWITTER_OAUTH_KEY = getenv('TWITTER_OAUTH_KEY')
    TWITTER_OAUTH_SECRET = getenv('TWITTER_OAUTH_SECRET')

    if not (TWITTER_OAUTH_KEY and TWITTER_OAUTH_SECRET):
        raise Exception()

    config = UserConfig(TWITTER_OAUTH_KEY, TWITTER_OAUTH_SECRET)

    client = API(config)

    response = client.delete_webhooks(webhook_id)

    if response.ok:
        print('Webhook deleted')
    else:
        print('Cannot delete webhook')
        print(response.text)
