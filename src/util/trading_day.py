import datetime
from constants import Constants

def to_date(datestr="", format="%Y-%m-%d"):
    if not datestr:
        return datetime.today().date()
    return datetime.datetime.strptime(datestr, format).date()

def from_date(day, format="%Y-%m-%d"):
    if day:
        return day.strftime(format)
    return ''

class TradingDays(object):
    WEEKENDS = 5, 6
    def __init__(self, start_date, end_date):
        self.start_date = to_date(start_date)
        self.end_date = to_date(end_date)

        if self.start_date > self.end_date:
            self.start_date,self.end_date = self.end_date, self.start_date

        self.days_work = [x for x in range(7) if x not in self.WEEKENDS]
 
    def trading_days(self):
        tag_date = self.start_date
        while True:
            if tag_date > self.end_date:
                break
            if tag_date.weekday() in self.days_work:
                if not self.__is_festival_day(from_date(tag_date)):
                    yield tag_date
            tag_date += datetime.timedelta(days=1)
 
    def days_count(self):
        return len(list(self.trading_days()))
 
    def weeks_count(self, day_start=0):
        day_nextweek = self.start_date
        while True:
            if day_nextweek.weekday() == day_start:
                break
            day_nextweek += datetime.timedelta(days=1)
        if day_nextweek > self.end_date:
            return 1
        weeks = ((self.end_date - day_nextweek).days + 1)/7
        weeks = int(weeks)
        if ((self.end_date - day_nextweek).days + 1)%7:
            weeks += 1
        if self.start_date < day_nextweek:
            weeks += 1
        return weeks

    def is_trading_day(self, day):
        converted = to_date(day)
        if converted.weekday() in self.WEEKENDS:
            return False
        if self.__is_festival_day(day):
            return False
        return True

    def __is_festival_day(self, day):
        if day in Constants.FESTIVAL_2015 or day in Constants.FESTIVAL_2016:
            return True
        return False

if __name__ == "__main__":
    d = to_date('2016-01-01')
    wd = TradingDays('2016-01-01', '2016-01-31')
    for day in wd.trading_days():
        print day
    print wd.is_trading_day('2016-01-01')
