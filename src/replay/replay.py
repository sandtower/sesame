import abc

class Replay(object):
    __metaclass__ = abc.ABCMeta 
    def start(self, stock_code, start_date, end_date):
        raise NotImplemented

    def stop(self):
        raise NotImplemented
