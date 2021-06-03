from application.helpers.filters import filter_messages
from application import User, Queue
from application.twitter import UserConfig, TweepyAPI
from application.helpers import filter_messages, Encryption


def process_message(user: User, message: str, media_id: int, sender_id: int):

    chiper = Encryption()
    config = UserConfig(chiper.decrypt(user.oauth_key),
                        chiper.decrypt(user.oauth_secret))
    APIClient = TweepyAPI(config)

    if filter_messages(message, user.forbidden_words):
        # check if queue is not full
        # jadwalkan twit
        queue = Queue(user=user, message=message,
                      media_id=media_id, scheduled_at='datetime now', sender_id=sender_id)
    else:
        error_message = 'Mohon maaf pesan yang anda kirim mengandung kata yang tidak diperbolehkan. Pesan anda tidak akan diproses'
        APIClient.app.send_direct_message(sender_id, error_message)
