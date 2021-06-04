from os import getenv
from requests_oauthlib import OAuth1  # type: ignore
from tweepy import OAuthHandler, API as TweepyTwitterAPI  # type: ignore
import requests


class Config:
    CUSTOMER_KEY: str = ''
    CUSTOMER_SECRET: str = ''
    BEARER_TOKEN: str = ''
    ENV_NAME: str = ''

    def __init__(self):
        self.CUSTOMER_KEY = getenv('TWITTER_CUSTOMER_KEY')
        self.CUSTOMER_SECRET = getenv('TWITTER_CUSTOMER_SECRET')
        self.ENV_NAME = getenv('TWITTER_ENV_NAME')
        self.BEARER_TOKEN = getenv('TWITTER_BEARER_TOKEN')


class UserConfig(Config):
    OAUTH_TOKEN: str = ''
    OAUTH_SECRET: str = ''

    def __init__(self, oauth_token: str, oauth_secret: str):
        super().__init__()
        self.OAUTH_TOKEN = oauth_token
        self.OAUTH_SECRET = oauth_secret


config = Config()


class API:
    host: str
    api_root: str
    config: UserConfig

    def __init__(self, user_config: UserConfig, host='api.twitter.com', api_root='/1.1', ):
        self.host = host
        self.api_root = api_root
        self.config = user_config

    def _get_auth(self) -> OAuth1:
        return OAuth1(self.config.CUSTOMER_KEY,
                      self.config.CUSTOMER_SECRET,
                      self.config.OAUTH_TOKEN,
                      self.config.OAUTH_SECRET)

    def _execute(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self.api_root + path
        full_url = 'https://' + self.host + url

        if method == 'GET':
            return requests.get(full_url, **kwargs)
        elif method == 'POST':
            return requests.post(full_url, **kwargs)
        elif method == 'DELETE':
            return requests.delete(full_url, **kwargs)
        else:
            raise Exception('Unavailable methods')

    def register_webhooks(self, url: str) -> requests.Response:
        payload = {
            'params': {
                'url': url
            },
            'auth': self._get_auth()
        }
        url = '/account_activity/all/{}/webhooks.json'.format(
            self.config.ENV_NAME)
        return self._execute('POST', url, **payload)

    def delete_webhooks(self, id: str) -> requests.Response:
        payload = {
            'auth': self._get_auth()
        }
        url = '/account_activity/all/{}/webhooks/{}.json'.format(
            self.config.ENV_NAME, id)
        return self._execute('DELETE', url, **payload)

    def subscribe_events(self) -> requests.Response:
        payload = {
            'auth': self._get_auth()
        }
        url = '/account_activity/all/{}/subscriptions.json'.format(
            self.config.ENV_NAME)
        return self._execute('POST', url, **payload)

    def unsubscribe_events(self, user_id: int) -> requests.Response:
        payload = {
            'headers': {
                'Auth': 'Bearer ' + self.config.BEARER_TOKEN
            }
        }
        url = '/account_activity/all/{}/subscriptions/{}.json'.format(
            self.config.ENV_NAME, user_id)
        return self._execute('DELETE', url, **payload)


class TweepyAPI:
    app: TweepyTwitterAPI
    auth: OAuthHandler
    config: UserConfig

    def __init__(self, user_config: UserConfig):
        self.config = user_config
        self.auth = OAuthHandler(self.config.CUSTOMER_KEY,
                                 self.config.CUSTOMER_SECRET)
        self.auth.set_access_token(self.config.OAUTH_TOKEN,
                                   self.config.OAUTH_SECRET)
        self.app = TweepyTwitterAPI(self.auth)
