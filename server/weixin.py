# coding=utf-8
import hashlib
import msg_parser
import controller
import json
import tornado.httpserver
import tornado.options
import tornado.web
import logging

_logger = logging.getLogger(__name__)

def authenticate(request):
    if len(request.get_arguments()) <= 3:
        return False
    token = 'weixin'
    signature = request.get_argument('signature', None)
    timestamp = request.get_argument('timestamp', None)
    nonce = request.get_argument('nonce', None)
    echostr = request.get_argument('echostr', None)

    combine = "".join([signature, timestamp, nonce, echostr].sort())
    calcualte_signature = hashlib.sha1(combine).hexdigest()
    if calculate_signature == signature:
        return True
    else:
        return False

def process_user_request(request):
    xmldict = msg_parser.recv_msg(request.body)
    _logger.info("request = %r" % xmldict)
    _logger.info("process %s stock" % xmldict['Content']) 
    controller.process(xmldict)
    _logger.info("process result : %s" % xmldict['Content']) 
    reply = msg_parser.submit_msg(xmldict)
    _logger.info("response = %r" % reply)
    return reply 

class WeixinHandler(tornado.web.RequestHandler):
    def get(self):
        _logger.info("get request")
        try:
            if authenticate(self) == True:
                self.write(echostr)
            else:
                self.write("认证失败，不是微信服务器的请求！")
        except Exception as e:
            _logger.exception(e)
        self.write("you request is illegal")

    def post(self):
        _logger.info("put request")
        try:
            reply = process_user_request(self.request)
            self.set_header("Content-Type", "application/xml")
            self.write(reply)
        except Exception as e:
            _logger.exception(e)
            reply = "you request is invalid"
        _logger.info("POST finished.")
        self.write(reply)

from tornado.options import define, options
define('port', default=80, help='run on the given port', type=int)

def main():
    try:
        app = tornado.web.Application(handlers=[(r'/', WeixinHandler)])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        _logger.exception(e)

