from os import getenv

from mongoengine import (CASCADE, BooleanField, DateTimeField,  # type: ignore
                         DictField, Document, IntField, ListField, QuerySet,
                         ReferenceField, StringField, UUIDField)
from mongoengine import connect as mongo_connect  # type: ignore
from mongoengine.errors import ValidationError  # type: ignore
from pymongo import MongoClient  # type: ignore

from application.helpers import utc_now


def connect() -> MongoClient:
    """Make connection with MongoDB Database

    Returns:
        MongoClient: MongoDB Client Connection
    """
    db_name = getenv('DB_NAME')
    db_host = getenv('DB_HOST')
    return mongo_connect(db_name, host=db_host, connect=False)


def validate_time(input: str) -> bool:
    """Check if input satistify time with
    HH.MM or HH:MM format

    Args:
        input (str): Time in HH.MM or HH:MM ofrmat

    Returns:
        bool: True if input is in valid format
    """

    first = input.split('.')
    second = input.split(':')

    if len(first) == 2:
        try:
            map(int, first)
        except Exception:
            return False

        return True
    elif len(second) == 2:
        try:
            map(int, second)
        except Exception:
            return False

        return True
    else:
        return False


class Configuration(Document):
    """Key value pair configuration document

    Props:
    name: string
    value: string
    """
    name = StringField(required=True)
    value = StringField(required=True)


class User(Document):
    """User or registered autobase document file

    Props:
        user_id: User Twitter id
        name: user unique name identifier in application. Much like username. Should in alphanumeric without spaces
        trigger: autobase word trigger
        oauth_key: user's encrypted oauth access token
        oauth_secret user's ecrypted oauth access token secret
        schedule: autobase schedule with start_at, end_at, and interval key
        forbidden_words: list of forbidden words for corresponding autobase
        created_at: regular timestamp
        subscribed: to determine whether user have subscribed to events or not
    """
    user_id = IntField(required=True, unique=True)
    name = StringField(required=True, unique=True)
    trigger = StringField(required=True, min_length=3, max_length=20)
    oauth_key = StringField(required=True)
    oauth_secret = StringField(required=True)
    schedule = DictField(required=True)
    forbidden_words = ListField(required=True)
    created_at = DateTimeField(default=utc_now())
    subscribed = BooleanField(default=False)

    def clean(self):
        schedule = self.schedule
        if not ('start_at' in schedule and 'end_at' in schedule and 'interval' in schedule):
            raise ValidationError('Missing schedule dictionary key')

        if not (validate_time(schedule['start_at']) and validate_time(schedule['end_at'])):
            raise ValidationError('Time format error')

        if int(schedule['interval']) < 3:
            raise ValidationError('Interval time too low!')


class Queue(Document):
    """Tweet queue

    Props:
        user: user document reference field
        queue_id: queue id
        message: follower's message to tweet
        media_id: media (image or video) that attached to follower's message. 0 if no media attached
        job_id: Redis job id
        sender_id: sender twitter id
        scheduled_at: Tweet schedule
    """
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    queue_id = UUIDField(required=True)
    job_id = StringField()
    message = StringField(required=True)
    media_url = StringField()
    sender_id = IntField()
    scheduled_at = DateTimeField(required=True)


def get_configuration(name: str) -> str:
    """Get configuration value from configuration name

    Args:
        name (str): configuration name

    Returns:
        str: Configuration value
    """

    result: QuerySet = Configuration.objects(name=name)

    if result.count() == 0:
        raise Exception('No configuration found!')

    document: Configuration = result.first()

    return document.value
