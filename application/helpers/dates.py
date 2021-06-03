from datetime import datetime
from pytz import UTC


def utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=UTC)
