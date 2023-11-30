from enum import Enum
from datetime import date, datetime, timedelta

# 3rd party
from dateutil.relativedelta import relativedelta

class time_abrev(Enum):
    DAY = "D"
    WEEK = "W"
    MONTH = "M"

class enumTime(Enum):
    minute = 60
    hourly = 60 * minute
    daily = 24 * hourly
    weekly = 7 * daily

class enumWeek(Enum):
    segunda = 0
    terca = 1
    quarta = 2
    quinta = 3
    sexta = 4
    sabado = 5
    domingo = 6

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

    @staticmethod
    def proximo_envio_diario(hour, minute=0):
        hoje = date.today()
        proxima_execucao = hoje + relativedelta(days=+1)
        dt_proxima_execucao = datetime(year = proxima_execucao.year, 
                                     month = proxima_execucao.month, 
                                     day = proxima_execucao.day, 
                                     hour = hour,
                                     minute=minute)
        return dt_proxima_execucao

if __name__ == '__main__':
    assert enumTime.hourly.value == 3600
    assert enumTime.daily.value == 86400
    assert enumTime.weekly.value == 604800
