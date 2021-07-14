from typing import Dict, List

from flask.wrappers import Response
from application import User
from application.helpers import Encryption
from application.twitter import API, TweepyAPI, UserConfig
from flask import Blueprint, make_response, request
from mongoengine.queryset.queryset import QuerySet
from tweepy.models import User as TwitterUser

bp = Blueprint('register', __name__)


def get_autobase_list() -> List[Dict]:
    user_query: QuerySet = User.objects

    result = []

    for user in user_query:
        data = {
            "name": user.name,
            "trigger": user.trigger,
            "schedule": user.schedule,
            "forbidden_words": user.forbidden_words
        }

        result.append(data)

    return result


def handle_autobase_register(data: Dict) -> Response:
    required_keys = [
        'name',
        'trigger',
        'oauth_key',
        'oauth_secret',
        'start',
        'end',
        'interval',
        'forbidden_words'
    ]

    input_keys = data.keys()

    for key in required_keys:
        if not key in input_keys:
            return make_response('Missing data keys', 422)

    schedule = {
        'start_at': data['start'],
        'end_at': data['end'],
        'interval': int(data['interval'])
    }

    chiper = Encryption()

    oauth_key = chiper.decrypt(data['oauth_key'])
    oauth_secret = chiper.decrypt(data['oauth_secret'])

    config = UserConfig(oauth_key, oauth_secret)

    client = TweepyAPI(config)

    twitter_user: TwitterUser = client.app.me()

    user = User(user_id=twitter_user.id, name=data['name'], trigger=data['trigger'],
                oauth_key=data['oauth_key'], oauth_secret=data['oauth_secret'],
                schedule=schedule, forbidden_words=data['forbidden_words'], subscribed=False)

    user.save()

    return make_response('', 200)


def handle_autobase_update(name: str, data: Dict) -> Response:
    required_keys = [
        'trigger',
        'start',
        'end',
        'interval',
        'forbidden_words'
    ]

    input_keys = data.keys()

    for key in required_keys:
        if not key in input_keys:
            return make_response('Missing data keys', 422)

    schedule = {
        'start_at': data['start'],
        'end_at': data['end'],
        'interval': int(data['interval'])
    }

    user: User = User.objects(name=name).first()

    user.trigger = data["trigger"]
    user.schedule = schedule
    user.forbidden_words = data["forbidden_words"]

    user.save()

    return make_response('', 200)


def handle_autobase_delete(name: str) -> Response:
    user_query: QuerySet = User.objects(name=name)

    if user_query.count() == 0:
        return make_response('User not found', 404)
    user: User = user_query.first()

    if user.subscribed:
        chiper = Encryption()

        response = API(UserConfig(chiper.decrypt(user.oauth_key), chiper.decrypt(
            user.oauth_secret))).unsubscribe_events(user.user_id)

        if response.ok:
            user.subscribed = False
        else:
            return make_response('Failed to unsubscribe user', 500)

    user.delete()

    return make_response('', 200)


@bp.route('/api/users', methods=['GET', 'POST'])
def users():
    """User/autobase registration route

    result saved in database's user collection

    Request data for registration:
        name: user unique name identifier in application. Much like username. Should in alphanumeric without spaces
        trigger: autobase word trigger
        oauth_key: user's encrypted oauth access token
        oauth_secret: user's ecrypted oauth access token secret
        startt: time when to start menfess submission
        end: time when to end menfess submission
        interval: interval between each menfess submission
        schedule: autobase schedule with start_at, end_at, and interval key
        forbidden_words: list of forbidden words for corresponding autobase
    """

    if request.method == 'POST':
        data: Dict = request.get_json()
        return handle_autobase_register(data)
    elif request.method == 'GET':
        return get_autobase_list()

    return make_response('', 200)


@bp.route('/api/users/<name>', methods=['PUT', 'DELETE'])
def user(name: str):
    """Update and delete user/autobase by its name

    Args:
        name (str): user name identifier

    """
    if request.method == 'PUT':
        data: Dict = request.get_json()  # type: ignore
        return handle_autobase_update(name, data)
    elif request.method == 'DELETE':
        return handle_autobase_delete(name)

    return make_response('', 200)


@bp.route('/api/users/<name>/subscription', methods=['POST', 'DELETE'])
def subscription(name: str):
    """Subscribe and unsubscribe user to listen account activity API events

    Events will be delivered to this site webhook
    """

    user_query: QuerySet = User.objects(name=name)

    if user_query.count() == 0:
        return make_response('User not found', 404)
    elif user_query.count() > 1:
        return make_response('Duplicate users', 400)

    user: User = user_query.first()

    chiper = Encryption()

    config = UserConfig(chiper.decrypt(user.oauth_key),
                        chiper.decrypt(user.oauth_secret))

    client = API(config)

    if request.method == 'POST' and not user.subscribed:
        response = client.subscribe_events()

        if response.ok:
            user.subscribed = True
            user.save()
        else:
            return make_response('Failed to subscribe event', 400)

    elif request.method == 'DELETE' and user.subscribed:
        response = client.unsubscribe_events(user.user_id)

        if response.ok:
            user.subscribed = False
            user.save()
        else:
            return make_response('Failed to unsubscribe user', 500)

    return make_response('', 200)
