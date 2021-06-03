from mongoengine.queryset.queryset import QuerySet  # type: ignore
from application.helpers.filters import filter_messages
from application import User, Queue
from application.twitter import UserConfig, TweepyAPI
from application.helpers import filter_messages, Encryption, from_time, to_local
from datetime import datetime, timedelta


def process_message(user: User, message: str, media_id: int, sender_id: int):

    chiper = Encryption()
    config = UserConfig(chiper.decrypt(user.oauth_key),
                        chiper.decrypt(user.oauth_secret))
    APIClient = TweepyAPI(config)

    if filter_messages(message, user.forbidden_words):
        queues: QuerySet = Queue.objects(user=user).order_by('-scheduled_at')

        if queues.count() >= 150:
            full_message = 'Antrian penuh. Saat ini terdapat lebih dari 150 antrian. Silakan coba lagi nanti.'
            APIClient.app.send_direct_message(sender_id, full_message)
        else:
            latest_queue: Queue = queues.first()
            latest_schedule = latest_queue.scheduled_at
            start_time = from_time(user.schedule['start_at'])
            end_time = from_time(user.schedule['end_at'])
            interval = int(user.schedule['interval'])

            tweet_schedule = schedule_tweet(
                latest_schedule, start_time, end_time, interval)

            queue = Queue(user=user, message=message,
                          media_id=media_id, scheduled_at=tweet_schedule, sender_id=sender_id)
            queue.save()

            queue_number = queues.count() + 1
            date = to_local(tweet_schedule).strftime("%d %B %Y %H:%M")

            message = "Pesan anda akan diproses. Nomor antrian anda {}. Tweet akan dikirim pada {}.".format(
                queue_number, date)
            APIClient.app.send_direct_message(sender_id, message)
    else:
        error_message = 'Pesan yang anda kirim mengandung kata yang tidak diperbolehkan. Pesan anda tidak akan diproses'
        APIClient.app.send_direct_message(sender_id, error_message)


def process_queue(user: User, queue: Queue):
    chiper = Encryption()
    config = UserConfig(chiper.decrypt(user.oauth_key),
                        chiper.decrypt(user.oauth_secret))
    APIClient = TweepyAPI(config)

    if queue.media_id == 0:
        APIClient.app.update_status(status=queue.message)
    else:
        APIClient.app.update_status(
            status=queue.message, media_ids=[queue.media_id])


def schedule_tweet(latest_time: datetime, start: datetime, end: datetime, interval: int) -> datetime:
    if latest_time + timedelta(minutes=interval) > end:
        return start + timedelta(days=1)
    else:
        return latest_time + timedelta(minutes=interval)
