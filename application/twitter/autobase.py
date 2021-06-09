import uuid
from datetime import datetime, timedelta
from typing import Union

from application import Queue, User, get_redis_queue
from application.helpers import (Encryption, filter_messages, from_time,
                                 replace_to_utc, to_local)
from application.helpers.dates import utc_now
from application.helpers.filters import filter_messages
from application.twitter import TweepyAPI, UserConfig
from mongoengine.queryset.queryset import QuerySet  # type: ignore
from rq.job import Job  # type: ignore


def process_message(user: User, message: str, media_url: str, sender_id: int):
    """Process incoming message

    Flow:
    1. Check profanity
    2. Check current queue
    3. Create queue and schedule to Redis Queue
    4. Send response tweet

    Args:
        user (User): User object
        message (str): Direct message to process
        media_url (str): Attached medai url
        sender_id (int): Sender twitter id
    """

    chiper = Encryption()

    config = UserConfig(chiper.decrypt(user.oauth_key),
                        chiper.decrypt(user.oauth_secret))

    APIClient = TweepyAPI(config)

    # Check if message contain forbidden words
    if filter_messages(message, user.forbidden_words):
        # Check current queue and get all queues order by schedule (descending or from latest to earliest)
        queues: QuerySet = Queue.objects(user=user).order_by('-scheduled_at')

        if queues.count() >= 50:
            full_message = 'Antrian penuh. Saat ini terdapat lebih dari lima puluh antrian. Silakan coba lagi nanti.'
            APIClient.app.send_direct_message(sender_id, full_message)
        else:
            now = utc_now()

            if queues.count() == 0:
                latest_schedule = now
            else:
                latest_queue: Queue = queues.first()
                latest_queue_schedule = replace_to_utc(
                    latest_queue.scheduled_at)
                if latest_queue_schedule > now:
                    latest_schedule = latest_queue_schedule

            start_time = from_time(user.schedule['start_at'])
            end_time = from_time(user.schedule['end_at'])
            interval = int(user.schedule['interval'])

            # Get tweet schedule based on latest queue
            tweet_schedule = schedule_tweet(
                latest_schedule, start_time, end_time, interval)

            queue_id = uuid.uuid4()

            # schedule tweet with Redis Queue
            redis_scheduler = get_redis_queue()

            job: Job = redis_scheduler.enqueue_at(
                tweet_schedule, process_queue_rq, queue_id)

            # if message has media, strip trailing https://t.co/xxxx link
            link_index = message.find('https://t.co/')
            if link_index != -1 and media_url != '':
                message = message[:link_index].strip()

            # Create new queue
            queue = Queue(user=user, message=message, queue_id=queue_id, job_id=job.id,
                          media_url=media_url, scheduled_at=tweet_schedule, sender_id=sender_id)

            queue.save()

            queue_number = queues.count()

            date = to_local(tweet_schedule).strftime("%-d %B %Y %H:%M")

            response_message = "Pesan anda akan diproses. Nomor antrian anda {}. Tweet akan dikirim pada {}. Gunakan perintah /cancel untuk membatalkan pesan".format(
                queue_number, date)

            APIClient.app.send_direct_message(sender_id, response_message)
    else:
        error_message = 'Pesan yang anda kirim mengandung kata yang tidak diperbolehkan. Pesan anda tidak akan diproses'
        APIClient.app.send_direct_message(sender_id, error_message)


def process_queue(queue: Queue):
    """Process queue and send tweet to corresponding autobase

    Args:
        queue (Queue): Queue to process
    """

    user: User = queue.user

    chiper = Encryption()

    config = UserConfig(chiper.decrypt(user.oauth_key),
                        chiper.decrypt(user.oauth_secret))

    APIClient = TweepyAPI(config)

    if queue.media_url == '':
        APIClient.app.update_status(status=queue.message)
    else:
        media_id = APIClient.upload_from_url(queue.media_url)

        APIClient.app.update_status(
            status=queue.message, media_ids=[media_id])

    queue.delete()


def cancel_queue_rq(queue: Queue):
    """Cancel active queue

    Args:
        queue (Queue): Queue document
    """

    redis = get_redis_queue()
    job: Job = redis.fetch_job(queue.job_id)
    job.delete()
    queue.delete()

    user: User = queue.user

    chiper = Encryption()

    config = UserConfig(chiper.decrypt(user.oauth_key),
                        chiper.decrypt(user.oauth_secret))

    APIClient = TweepyAPI(config)

    APIClient.app.send_direct_message(
        queue.sender_id, 'Pesan anda sudah dibatalkan')


def process_queue_rq(id: Union[str, uuid.UUID]):
    """Redis queue processor

    Args:
        id (Union[str, uuid.UUID]): Queue id
    """
    if not isinstance(id, uuid.UUID):
        id = uuid.UUID(id)

    queue_query: QuerySet = Queue.objects(queue_id=id)

    if queue_query.count() != 0:
        try:
            process_queue(queue_query.first())
        except:
            queue_query.first().delete()


def schedule_tweet(latest_time: datetime, start: datetime, end: datetime, interval: int) -> datetime:
    """Schedule tweet based on latest queue schedule

    Args:
        latest_time (datetime): Latest queue schedule
        start (datetime): Autobase today start time
        end (datetime): Autobase today end time
        interval (int): Autobase tweet interval

    Returns:
        datetime: Queue schedule
    """
    if utc_now() < start:
        return start + timedelta(minutes=interval)
    elif latest_time + timedelta(minutes=interval) > end:
        return start + timedelta(days=1)
    else:
        return latest_time + timedelta(minutes=interval)
