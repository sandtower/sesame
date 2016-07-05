# -*- coding: utf-8 -*-
import codecs
import re
import urllib2  

import logging

from util.constants import Constants
  
_logger = logging.getLogger(__name__)

class RealtimeCollector(object):  
    def __init__(self):  
        self.__basic_url = Constants.REALTIME_BASIC_QUERY_URL
        self.__flow_url = Constants.CURRENT_FLOW_QUERY_URL

    def __get_stock_code(self, stock_id):
        for key, value in Constants.STOCK_CODE_CATEGORIES:
            if stock_id.startswith(key):
                return value + stock_id
        _logger.warn("stock code : %s is unkown" % stock_id)
        return ''
  
    def __parse_stock_data(self, result, stock_info):
        stock_info['name'] = result[1].decode('gbk')
        stock_info['buy_one'] = float(result[9])
        stock_info['sell_one'] = float(result[19])
        stock_info['turnover'] = float(result[38].strip('%'))
        _logger.info("stock realtime info: %r." % stock_info)
        
    def __parse_stock_index(self, result, stock_info):
        stock_info['name'] = result[1].decode('gbk')
        stock_info['close_price'] = float(result[3])
        stock_info['high_price'] = float(result[33])
        stock_info['low_price'] = float(result[34])
        stock_info['amplitude'] = float(result[43].strip('%'))
        stock_info['updown'] = float(result[32].strip('%'))
        stock_info['volume'] = float(result[37])
        
    def collect_rt_data(self, stock_id, stock_info):  
        _logger.info('collect real time data, stock_id=%r.' % stock_id)
        try:  
            stock_code = self.__get_stock_code(stock_id)
            if len(stock_code) == 0:
                return 

            stock_info['code'] = stock_id
            url = self.__basic_url % stock_code
            _logger.info('collect real time data, url=%r' % url)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)  
            contents = response.read()  
            match_result = re.findall(r'v_.*?="(.*?)";', contents)
            if len(match_result) == 0:
                return
            result = match_result[0].split('~')
            if stock_id in Constants.STOCK_INDEX_CODES:
                self.__parse_stock_index(result, stock_info)
            else:
                self.__parse_stock_data(result, stock_info)
        except urllib2.URLError, e:  
            _logger.exception(e)

    def get_flow_data(self, stock_id, stock_info):  
        try:  
            stock_code = self.__get_stock_code(stock_id)
            if len(stock_code) == 0:
                return 

            url = self.__flow_url % stock_code
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)  
            contents = response.read()  
            match_result = re.findall(r'v_.*?="(.*?)";', contents)
            if len(match_result) == 0:
                return
            result = match_result[0].split('~')
            stock_info['main_inflow'] = float(result[1])
            stock_info['main_outflow'] = float(result[2])
            stock_info['main_net_inflow'] = float(result[3])
            stock_info['retail_inflow'] = float(result[5])
            stock_info['retail_outflow'] = float(result[6])
            stock_info['retail_net_inflow'] = float(result[7])
            stock_info['inflow_outlow_sum'] = float(result[9])
        except urllib2.URLError, e:  
            _logger.exception(e)

if __name__=='__main__':  
    query = RealtimeCollector()  
    stock_code = '002657'
    stock_info = {}
    query.collect_rt_data(stock_code, stock_info)
    print stock_info
