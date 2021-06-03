from typing import Dict
from flask import Blueprint, request
from mongoengine.queryset.queryset import QuerySet  # type: ignore
from application.twitter import webhook_challenge, validate_twitter_signature, process_message
from application import User

bp = Blueprint('twitter', __name__)


@bp.route('/service/listen', methods=['GET', 'POST', 'PUT'])
def hook():
    if request.method == 'GET' or request.method == 'PUT':
        return webhook_challenge()
    elif request.method == 'POST':
        if validate_twitter_signature():

            data: Dict = request.get_json()

            # check if it is direct message event
            if "direct_message_events" not in data:
                return

            message_event: Dict = data['direct_message_events']['message_create']

            for_user_id = int(data['for_user_id'])
            recipient_id = int(message_event['target']['recipient_id'])

            # if outgoing message
            if for_user_id != recipient_id:
                return

            user_collection: QuerySet = User.objects(user_id=for_user_id)

            if user_collection.count() == 0:
                return

            user: User = user_collection.first()
            message_text: str = message_event['message_data']['text']
            media_id = 0
            sender_id = int(message_event['sender_id'])

            if 'attachment' in message_event['message_data'] and 'type' in message_event['message_data']['attachment'] and message_event['message_data']['attachment']['type'] == 'media':
                media_id = int(
                    message_event['message_data']['attachment']['media']['id'])

            if user.trigger in message_text:
                process_message(user, message_text, media_id, sender_id)

            return
