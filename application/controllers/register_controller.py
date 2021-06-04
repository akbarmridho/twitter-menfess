from typing import Dict
from application import User
from application.helpers import Encryption
from application.twitter import API, TweepyAPI, UserConfig
from flask import Blueprint, make_response, request
from mongoengine.queryset.queryset import QuerySet  # type: ignore
from tweepy.models import User as TwitterUser  # type: ignore

bp = Blueprint('register', __name__)


@bp.route('/user/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data: Dict = request.get_json()

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

    if not required_keys in data.keys():
        response = make_response('Missing data keys', 403)
        return response

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


@bp.route('/user/delete/<name>', methods=['DELETE'])
def delete(name: str):
    user_query: QuerySet = User.objects(name=name)
    if user_query.count() == 0:
        return make_response('User not found', 404)
    user: User = user_query.first()

    if user.subscribed:
        response = API(UserConfig('', '')).unsubscribe_events(user.user_id)
        if response.ok:
            user.subscribed = False
        else:
            return make_response('Failed to unsubscribe user', 500)

    user.delete()


@bp.route('/user/subscribe', methods=['POST'])
def subscribe():

    if request.method == 'POST':
        data: Dict = request.get_json()

    if not 'name' in data:
        response = make_response('Missing data keys', 400)
        return response

    user_query: QuerySet = User.objects(name=data['name'])

    if user_query.count() == 0:
        return make_response('User not found', 404)
    elif user_query.count() > 1:
        return make_response('Duplicate users', 400)

    user: User = user_query.first()

    chiper = Encryption()

    oauth_key = chiper.decrypt(user.oauth_key)
    oauth_secret = chiper.decrypt(user.oauth_secret)

    config = UserConfig(oauth_key, oauth_secret)

    client = API(config)

    response = client.subscribe_events()

    if response.ok:
        user.subscribed = True
        user.save()
    else:
        user.delete()
        return make_response('Failed to subscribe event', 214)


@bp.route('/user/unsubscribe/<name>', methods=['DELETE'])
def unsubscribe(name: str):
    user_query: QuerySet = User.objects(name=name)
    if user_query.count() == 0:
        return make_response('User not found', 404)
    user: User = user_query.first()

    if user.subscribed:
        response = API(UserConfig('', '')).unsubscribe_events(user.user_id)
        if response.ok:
            user.subscribed = False
            user.save()
        else:
            return make_response('Failed to unsubscribe user', 500)
