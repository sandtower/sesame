from util.db import DB, Collection
from util.constants import Constants
from util.util import Util

import tushare as ts
import logging

_logger = logging.getLogger(__name__)

class HistoryCollector(object):
    def __init__(self, stock_code, db):
        self.__stock_code = stock_code
        self.__db = db
        self.__collection = Collection(stock_code, self.__db)

    def collect_history_data(self):
        begin_date = None
        last_record = self.__collection.find_one('date')
        if last_record:
            begin_date = last_record['date']
            _logger.info('collect stock(%s) history data, begin date: %r.' % (self.__stock_code, begin_date))

        end_date = Util.get_today()
        _logger.info('collect stock(%s) history data, end date: %r.' % (self.__stock_code, end_date))
        if begin_date == end_date:
            return
        elif not begin_date or len(begin_date) == 0:
            result = ts.get_hist_data(self.__stock_code)
        else:
            result = ts.get_hist_data(code=self.__stock_code, start=begin_date, end=end_date)

        if result is None:
            _logger.warn('could get stock(%r) history data from tushare.' % self.__stock_code)
            return
        datas = result.to_dict()
        for attr, data, in datas.iteritems():
            for date, value in data.iteritems():
                self.__collection.insert_and_update('date', date, **{attr: value})

if __name__ == '__main__':
    db = DB(Constants.DB_NAME)
    collector = HistoryCollector('600036', db)
    collector.collect_history_data()
