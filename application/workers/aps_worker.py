from application import Queue, connect
from application.helpers import utc_now
from application.twitter import process_queue
from apscheduler.schedulers.blocking import BlockingScheduler  # type: ignore
from mongoengine.queryset.queryset import QuerySet  # type: ignore

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=5)
def process():
    connect()

    queue: QuerySet = Queue.objects(scheduled_at__lte=utc_now())

    for job in queue:
        process_queue(job)


sched.start()
