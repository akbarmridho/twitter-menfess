from apscheduler.schedulers.blocking import BlockingScheduler  # type: ignore
from mongoengine.queryset.queryset import QuerySet  # type: ignore
from application import connect, Queue
from application.helpers import utc_now
from application.twitter import process_queue

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=5)
def process():
    connect()
    queue: QuerySet = Queue.objects(scheduled_at__lte=utc_now())
    for job in queue:
        process_queue(job)


sched.start()
