from mongoengine import (connect as mongo_connect, Document, StringField,  # type: ignore
                         DictField, IntField, QuerySet, ListField, ReferenceField,
                         DateTimeField, CASCADE, UUIDField)  # type: ignore
from mongoengine.errors import ValidationError  # type: ignore
from typing import Dict
from os import getenv
from application.helpers import utc_now


def connect():
    db_name = getenv('DB_NAME')
    db_host = getenv('DB_HOST')
    return mongo_connect(db_name, host=db_host)


def validate_time(input: str) -> bool:
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
    name = StringField(required=True)
    value = DictField(required=True)


class User(Document):
    user_id = IntField(required=True, unique=True)
    name = StringField(required=True, unique=True)
    trigger = StringField(required=True, min_length=3, max_length=20)
    oauth_key = StringField(required=True)
    oauth_secret = StringField(required=True)
    schedule = DictField(required=True)
    forbidden_words = ListField(required=True)
    created_at = DateTimeField(default=utc_now())

    def clean(self):
        schedule = self.schedule
        if not ('start_at' in schedule and 'end_at' in schedule and 'interval' in schedule):
            raise ValidationError('Missing schedule dictionary key')

        if not (validate_time(schedule['start_at']) and validate_time(schedule['end_at'])):
            raise ValidationError('Time format error')

        if int(schedule['interval']) < 3:
            raise ValidationError('Interval time too low!')


class Queue(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    queue_id = UUIDField(primary_key=True)
    message = StringField(required=True)
    media_id = IntField()
    sender_id = IntField()
    scheduled_at = DateTimeField(required=True)


def get_configuration(name: str) -> Dict:
    result: QuerySet = Configuration.objects(name=name)
    if result.count() == 0:
        raise Exception('No configuration found!')
    document: Configuration = result.first()
    return document.value
