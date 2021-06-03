from typing import Dict
from flask import Blueprint, request, make_response
from application import User
from application.twitter import API, UserConfig
from application.helpers import Encryption

bp = Blueprint('register', __name__)


@bp.route('/user/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data: Dict = request.get_json()

    required_keys = [
        'name',
        'webhook_id',
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
        'interval': data['interval']
    }

    user = User(name=data['name'], trigger=data['trigger'],
                oauth_key=data['oauth_key'], oauth_secret=data['oauth_secret'],
                schedule=schedule, forbidden_words=data['forbidden_words'])

    chiper = Encryption()

    config = UserConfig(chiper.decrypt(
        data['oauth_key']), chiper.decrypt(data['oauth_secret']))

    client = API(config)

    response = client.subscribe_events()

    if response.ok:
        data: Dict = response.json()
        user_id = int(data['id'])
        user.user_id = user_id
        user.save()
    else:
        user.delete()
        return make_response('Failed to subscribe event', 214)
