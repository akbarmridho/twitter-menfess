from datetime import datetime
from pytz import UTC, timezone
from typing import Iterator


def _convert_string_to_time(time: str) -> Iterator[int]:
    if len(time.split('.')) == 2:
        return map(int, time.split('.'))
    elif len(time.split(':')) == 2:
        return map(int, time.split(':'))
    raise Exception('Cannot parse time')


def utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=UTC)


def from_time(time: str) -> datetime:
    [hours, minutes] = _convert_string_to_time(time)
    return utc_now().replace(hour=hours, minute=minutes)


def local_now() -> datetime:
    return utc_now().astimezone(timezone('Asia/Jakarta'))


def to_local(datetime: datetime) -> datetime:
    return datetime.astimezone(timezone('Asia/Jakarta'))
