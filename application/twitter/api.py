import mimetypes
import tempfile
from os import getenv
from typing import Tuple

import requests
from requests_oauthlib import OAuth1
from tweepy import API as TweepyTwitterAPI
from tweepy import OAuthHandler
from tweepy.models import Media, Status
from application.helpers import split_message


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
            'data': {
                'url': url
            },
            'auth': self._get_auth()
        }

        api_url = '/account_activity/all/{}/webhooks.json'.format(
            self.config.ENV_NAME)

        return self._execute('POST', api_url, **payload)

    def get_webhooks(self) -> requests.Response:
        """Get all registered webhook

        Returns:
            requests.Response: Response object
        """

        payload = {
            'headers': {
                'authorization': 'Bearer ' + self.config.BEARER_TOKEN
            }
        }

        url = '/account_activity/all/webhooks.json'

        return self._execute('GET', url, **payload)

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
                'authorization': 'Bearer ' + self.config.BEARER_TOKEN
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

    def _guess_extension(self, url) -> str:
        """Guess file extension from url

        Returns:
            str: File extension (with dot)
        """
        mime_types: Tuple = mimetypes.guess_type(url)
        for mime_type in mime_types:
            if not mime_type == None:
                guess = mimetypes.guess_extension(mime_type)
                if not guess == None:
                    return guess  # type: ignore
        raise Exception('Cannot guess extension')

    def upload_from_url(self, url) -> int:
        """Upload image, video, or gif from url

        Args:
            url: file url

        Returns:
            int: Twitter media id
        """
        file = tempfile.NamedTemporaryFile(suffix=self._guess_extension(url))

        res = requests.get(url, stream=True, auth=self.auth.apply_auth())

        if res.ok:
            for chunk in res:
                file.write(chunk)
        else:
            raise Exception('Cannot load file')

        twitter_media: Media = self.app.media_upload(file.name, file=file)

        file.close()

        return twitter_media.media_id

    def update_status(self, message: str, media_id: int = None):
        """Update status with and without media id

        Automatically split long messages into several tweet

        Args:
            message (str): [description]
            media_id (int, optional): [description]. Defaults to None.
        """

        tweets = split_message(message)

        if media_id is not None:
            response: Status = self.app.update_status(
                status=tweets[0], media_ids=[media_id])
        else:
            response = self.app.update_status(status=tweets[0])

        to_quote_id: int = response.id

        if len(tweets) > 1:
            for tweet in tweets[1:]:
                response = self.app.update_status(
                    status=tweet, in_reply_to_status_id=to_quote_id, auto_populate_reply_metadata=True)
                to_quote_id = response.id
