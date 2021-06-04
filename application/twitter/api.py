from os import getenv

import requests
from requests_oauthlib import OAuth1  # type: ignore
from tweepy import API as TweepyTwitterAPI  # type: ignore
from tweepy import OAuthHandler


class Config:
    """Base twitter API keys class
    """
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
        """Config with user decrypted oauth token and secret

        Args:
            oauth_token (str): access token
            oauth_secret (str): access token secret
        """
        super().__init__()
        self.OAUTH_TOKEN = oauth_token
        self.OAUTH_SECRET = oauth_secret


config = Config()


class API:
    host: str
    api_root: str
    config: UserConfig

    def __init__(self, user_config: UserConfig, host='api.twitter.com', api_root='/1.1', ):
        """Initialize the TwitterAPI

        Args:
            user_config (UserConfig): User config
            host (str, optional): Twitter API host. Defaults to 'api.twitter.com'.
            api_root (str, optional): Twitter API root. Defaults to '/1.1'.
        """
        self.host = host
        self.api_root = api_root
        self.config = user_config

    def _get_auth(self) -> OAuth1:
        """Get oauth1 object for outgoing request

        Returns:
            OAuth1: OAuth1 object filled with user's access token
        """
        return OAuth1(self.config.CUSTOMER_KEY,
                      self.config.CUSTOMER_SECRET,
                      self.config.OAUTH_TOKEN,
                      self.config.OAUTH_SECRET)

    def _execute(self, method: str, path: str, **kwargs) -> requests.Response:
        """Execute request

        Args:
            method (str): Request method. Impelemented methods: GET, POST, DELETE
            path (str): Request url

        Returns:
            requests.Response: response object
        """
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
        """Register application webhook

        Args:
            url (str): Webhook endpoint

        Returns:
            requests.Response: response object
        """

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
        """Delete application webhook

        Args:
            id (str): Webhook id

        Returns:
            requests.Response: response object
        """

        payload = {
            'auth': self._get_auth()
        }

        url = '/account_activity/all/{}/webhooks/{}.json'.format(
            self.config.ENV_NAME, id)

        return self._execute('DELETE', url, **payload)

    def subscribe_events(self) -> requests.Response:
        """Subscribe user to events
        Event will be delivered to application webhook endpoint

        Returns:
            requests.Response: response object
        """

        payload = {
            'auth': self._get_auth()
        }

        url = '/account_activity/all/{}/subscriptions.json'.format(
            self.config.ENV_NAME)

        return self._execute('POST', url, **payload)

    def unsubscribe_events(self, user_id: int) -> requests.Response:
        """Unsubscribe user to event

        Args:
            user_id (int): Twitter user id to unsubscribe

        Returns:
            requests.Response: resposne object
        """

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
        """Twitter Tweepy API

        Main usage:
        User lookup
        Send direct message
        Update tweet
        Get oauth token

        Args:
            user_config (UserConfig): user config
        """

        self.config = user_config

        self.auth = OAuthHandler(self.config.CUSTOMER_KEY,
                                 self.config.CUSTOMER_SECRET)

        self.auth.set_access_token(self.config.OAUTH_TOKEN,
                                   self.config.OAUTH_SECRET)

        self.app = TweepyTwitterAPI(self.auth)
