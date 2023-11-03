from enum import Enum
from datetime import datetime, timedelta

# 3rd party
from dateutil.relativedelta import relativedelta

class time_abrev(Enum):
    DAY = "D"
    WEEK = "W"
    MONTH = "M"

class scheduleOperations:

    @staticmethod
    def next_weekday(weekday, hour=0, minute=0, second=0):
        now = datetime.now()
        days_until_next_weekday = (weekday - now.weekday() + 7) % 7
        next_weekday = now + timedelta(days=days_until_next_weekday)
        next_weekday = datetime(
            next_weekday.year, next_weekday.month, next_weekday.day, hour=hour, minute=minute, second=second
        )
        return next_weekday

    @staticmethod
    def calculate_next_period(scheduled_time, interval):
        if isinstance(interval, str):
            if interval == time_abrev.DAY.value:
                interval = timedelta(days=1)
            elif interval == time_abrev.WEEK.value:
                interval = timedelta(weeks=1)
            elif interval == time_abrev.MONTH.value:
                interval = relativedelta(months=1)
        else:
            interval = timedelta(seconds=interval)
        new_scheduled_time = scheduled_time + interval
        return new_scheduled_time