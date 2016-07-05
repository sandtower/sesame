from strategy import Strategy
from util.db import Collection

import logging

_logger = logging.getLogger(__name__)

class MaStrategy(Strategy):
    def __init__(self, db):
        self.__db = db

    def decide(self, current_info):
        if not current_info:
            return 'sorry, current info is invalid.'

        stock_code = current_info['code']
        buy_one = current_info['buy_one']
        sell_one = current_info['sell_one']
        turnover = current_info['turnover']

        collection = Collection(stock_code, self.__db)
        last_data = collection.find_one('date')
        if not last_data:
            return 'not found history data.'
        ma_5 = last_data['ma5']
        ma_10 = last_data['ma10']
        ma_20 = last_data['ma20']
        if self.__should_buy(buy_one, ma_10) == True:
            return 'you should buy now.'
        if self.__should_sell(sell_one, ma_10) == True:
            return 'you should sell now.'
        return 'you hold, do nothing.'

    def __should_buy(self, buy_price, average):
        if buy_price < average:
            return False
        variation = (buy_price - average) / average
        _logger.info("should buy? buy_price(%r), ma10_price(%r), variation(%r)" % (buy_price, average, variation))
        if variation > 0.03:
            return True
        return False

    def __should_sell(self, sell_price, average):
        if sell_price > average:
            return False

        variation = (average - sell_price) / average
        _logger.info("should sell? sell_price(%r), ma10_price(%r), variation(%r)" % (sell_price, average, variation))
        if variation > 0.05:
            return True
        return False

if __name__ == "__main__":
    print "in ma strategy."
