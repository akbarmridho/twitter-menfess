from application.twitter import schedule_tweet
from application.helpers import utc_now
from datetime import timedelta

daytime = utc_now().replace(hour=12)
daytime_almost_end = utc_now().replace(hour=23)
start = utc_now().replace(hour=7)
end = utc_now().replace(hour=23)
interval = 10


def test_today_schedule():
    result = schedule_tweet(daytime, start, end, interval)
    assert (result < end)


def test_tomorrow_schedule():
    result = schedule_tweet(daytime_almost_end, start, end, interval)
    assert result >= (start + timedelta(days=1))
