from urllib.parse import urlencode
from tweepy import OAuthHandler, API as TwitterAPI
from tweepy.binder import bind_api
from os import environ


class ExtendedAPI(TwitterAPI):

    def register_webhooks(self, path: str):

        return bind_api(
            api=self,
            path='/account_activity/webhooks.json',
            method="POST",
            payload_type="status",
            allowed_param=['url'],
            require_auth=True
        )


class API:
    app: TwitterAPI
    CUSTOMER_KEY: str = ''
    CUSTOMER_SECRET: str = ''
    OAUTH_TOKEN: str = ''
    OAUTH_SECRET: str = ''

    def __init__(self) -> None:
        self._set_configuration()
        auth = OAuthHandler(self.CUSTOMER_KEY, self.CUSTOMER_SECRET)
        auth.set_access_token(self.OAUTH_TOKEN, self.OAUTH_SECRET)
        self.app = TwitterAPI(auth)

    def _set_configuration(self) -> None:
        self.CUSTOMER_KEY = environ.get('TWITTER_CUSTOMER_KEY')
        self.CUSTOMER_SECRET = environ.get('TWITTER_CUSTOMER_SECRET')
        self.OAUTH_TOKEN = environ.get('TWITTER_OAUTH_TOKEN')
        self.OAUTH_SECRET = environ.get('TWITTER_OAUTH_SECRET')
