from application.twitter import UserConfig, API
from os import getenv

webhook_id = getenv('WEBHOOK_ID')

if not webhook_id:
    raise Exception('Webhook id not found')

config = UserConfig(getenv('TWITTER_OAUTH_KEY', ''),
                    getenv('TWITTER_OAUTH_SECRET', ''))

client = API(config)

response = client.delete_webhooks(webhook_id)

if response.ok:
    print('Webhook deleted')
else:
    print('Cannot delete webhook')
    print(response.text)
