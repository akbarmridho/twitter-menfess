from typing import Dict, List
from flask import Blueprint, request, make_response, current_app
from mongoengine.queryset.queryset import QuerySet
from application.twitter import webhook_challenge, process_message, cancel_queue_rq
from application import User, Queue

bp = Blueprint('twitter', __name__)


@bp.route('/service/listen', methods=['GET', 'POST', 'PUT'])
def hook():
    """Twitter webhook endpoint

    GET and PUT request handle Twitter CRC

    POST request handle Twitter's User Activity API events
    """

    ok_response = make_response({'code': 200}, 200)

    if request.method == 'GET' or request.method == 'PUT':
        return webhook_challenge()
    elif request.method == 'POST':
        data: Dict = request.get_json()

        # check if it is direct message event
        if not "direct_message_events" in data:
            return ok_response

        direct_messages: List = data['direct_message_events']

        for direct_message in direct_messages:

            message_event: Dict = direct_message['message_create']

            for_user_id = int(data['for_user_id'])
            recipient_id = int(message_event['target']['recipient_id'])

            # if outgoing message
            if for_user_id != recipient_id:
                return ok_response

            # check if has hastag
            entities: Dict = message_event['message_data']
            if 'hashtags' in entities:
                hashtags = entities['hashtags']
                if isinstance(hashtags, List):
                    if len(hashtags) != 0:
                        return ok_response

            user_collection: QuerySet = User.objects(user_id=for_user_id)

            if user_collection.count() == 0:
                return ok_response

            user: User = user_collection.first()
            message_text: str = message_event['message_data']['text']
            media_url = ''
            sender_id = int(message_event['sender_id'])

            current_app.logger.info(
                'Incoming message event: ' + message_event.__str__())

            if 'attachment' in message_event['message_data'] and 'type' in message_event['message_data']['attachment'] and message_event['message_data']['attachment']['type'] == 'media':
                media_type = message_event['message_data']['attachment']['media']['type']

                if media_type == 'photo':
                    media_url = message_event['message_data']['attachment']['media']['media_url']

                elif media_type == 'video':
                    video_variants = message_event['message_data']['attachment']['media']['video_info']['variants']

                    for variant in video_variants:
                        if 'bitrate' in variant:
                            # take biggest bitrate
                            if int(variant['bitrate']) == 2176000:
                                media_url = variant['url']

            sender_queue: QuerySet = Queue.objects(
                user=user, sender_id=sender_id)

            # limit submission to 1000 chars
            if user.trigger in message_text and len(message_text) < 1000:
                # Do not process if sender have active queue
                if sender_queue.count() != 0:
                    return ok_response
                else:
                    process_message(user, message_text, media_url, sender_id)
            elif '/cancel' in message_text:
                # Cancel queue
                if sender_queue.count() != 0:
                    cancel_queue_rq(sender_queue.first())

        return ok_response
