from datetime import datetime, timedelta
from pytz import UTC, timezone
from typing import Iterator


def _convert_string_to_time(time: str) -> Iterator[int]:
    """Convert time string to int format

    Example:
    12:23 into [12, 23]
    or
    14.24 into [14, 24]

    Args:
        time (str): Should be in HH:MM or HH.MM format

    Raises:
        Exception: Raise exception if it contain more than two colon or double colon

    Returns:
        List[int]: First element is hours and second element is minutes
    """
    if len(time.split('.')) == 2:
        return map(int, time.split('.'))
    elif len(time.split(':')) == 2:
        return map(int, time.split(':'))
    raise Exception('Cannot parse time')


def utc_now() -> datetime:
    """Return datetime now with UTC timezone

    Returns:
        datetime: UTC Now
    """
    return datetime.utcnow().replace(tzinfo=UTC)


def replace_to_utc(value: datetime) -> datetime:
    """Replace current timezone info to UTC
    Does not convert timezone difference

    Args:
        value (datetime): [description]

    Returns:
        datetime: datetime aware
    """
    return value.replace(tzinfo=UTC)


def from_time(time: str) -> datetime:
    """Return today date with defined hour and minutes

    Args:
        time (str): HH:MM or HH.MM hour and minute format

    Returns:
        datetime: today date
    """
    [hours, minutes] = _convert_string_to_time(time)

    return utc_now().replace(hour=0, minute=0) + timedelta(hours=hours, minutes=minutes)


def local_now() -> datetime:
    """Return current datetime with local timezone
       In this case, it will use UTC+7 timezone

    Returns:
        datetime: current datetime in UTC+7
    """
    return utc_now().astimezone(timezone('Asia/Jakarta'))


def to_local(datetime: datetime) -> datetime:
    """Convert input datetime into localized timezone

    Args:
        datetime (datetime): input datetime

    Returns:
        datetime: localized datetime
    """
    return datetime.astimezone(timezone('Asia/Jakarta'))
