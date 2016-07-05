# coding=utf-8
from collector.history_collector import HistoryCollector
from collector.realtime_collector import RealtimeCollector
from strategy.ma_strategy import MaStrategy as Strategy
from util.db import DB
from util.constants import Constants

import logging
_logger = logging.getLogger(__name__)

def check_valid(stock_code):
    if not stock_code.isdigit():
        return False
    for key, _ in Constants.STOCK_CODE_CATEGORIES:
        if stock_code.startswith(key):
            return True
    return False

def process(content_dict={"":""}):
    INVALID_STOCK_CODE_MSG = 'You input invalid stock code, please input such as 600001.'
    _logger.info("process, entered..........")
    stock_code = content_dict['Content']
    if not check_valid(stock_code):
        content_dict['Content'] = INVALID_STOCK_CODE_MSG
        return
    db = DB(Constants.DB_NAME)
    hist_collector = HistoryCollector(stock_code, db)
    hist_collector.collect_history_data()
    realtime_collector = RealtimeCollector()
    current_info = {}
    realtime_collector.collect_rt_data(stock_code, current_info)
    strategy = Strategy(db)
    content_dict['Content'] = strategy.decide(current_info)

if __name__ == '__main__':
    print "hello"

