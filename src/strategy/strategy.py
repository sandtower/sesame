from abc import ABCMeta

class Strategy:
    __metaclass__ = ABCMeta
    BUY_IN = 1
    SELL_OUT = 2
    DO_NOTHING = 3
    #input: current_info : {'code':'002095', 'buy_one':10, 'sell_one':20, 'turnover':0.01}
    #input: user_info : {'user':'jordan', 'volume':100, 'cost_price':20, 'percent':10}
    #return: BUY_IN/SELL_OUT/DO_NOTHING, volume
    def decide(self, current_info, user_info):
        raise NotImplemented

class CompositeStrategy:
    __metaclass__ = ABCMeta
    #input: stock_info_list: 
    # [{'code':'002095', 'buy_one':10, 'sell_one':20, 'turnover':0.01}, ...]
    #input: user_info : {'user':'jordan', 'volume':100, 'cost_price':20, 'percent':10}
    #return: [{'code':'002095', 'op': BUY_IN, 'volume':10}, ...]
    def decide(self, stock_info_list, user_info):
        raise NotImplemented
