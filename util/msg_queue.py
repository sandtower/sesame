import Queue
import threading
import time
import zmq
import logging

import json

_logger = logging.getLogger(__name__)

class MsgQueueException(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return repr(self.__msg)

class MsgQueue(threading.Thread):
    def __init__(self, port=5460):
        threading.Thread.__init__(self)
        self.__port = port
        self.__context = zmq.Context()
        self.__socket = None
        self.__queue = Queue.Queue()
        self.__stopped = threading.Event()
        self.__connect()

    def __connect(self):
        self.__socket = self.__context.socket(zmq.REQ)
        self.__socket.connect("tcp://localhost:%r" % self.__port)

    def run(self):
        self.__do_work()

    def __do_work(self):
        while not self.__stopped.isSet():
            try:
                msg = self.__queue.get(True, 0.05)
                self.__socket.send(msg)
            except Queue.Empty:
                continue
            except zmq.ZMQError:
                self.__socket.close()
                self.__connect()

    def stop(self, timeout=None):
        self.__stopped.set()
        self.join(timeout)

    def send(self, msg):
        if not self.__socket:
            raise MsgQueueException("not connect to server")
        self.__queue.put(msg)

    def recv(self):
        try:
            return self.__socket.recv()
        except zmq.ZMQError as e:
            raise MsgQueueException("exception when connecting to server")

if __name__ == "__main__":
    mq = MsgQueue()
    mq.start()
    test_deal = {'stock': '002657', 'start': '2016-01-01', 'end': '2016-06-30'}
    mq.send(json.dumps(test_deal))
    time.sleep(1)
    msg = mq.recv()
    total = 0
    for deal in json.loads(msg):
        print deal
        total -= float(deal['volume']) * float(deal['price'])
        print total
    print total
    time.sleep(10)
    mq.stop()
