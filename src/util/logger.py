# -*- encoding:utf-8 -*-
import logging
import os

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create file handler
log_dir = "./log"
if not os.path.exists(os.path.join(os.getcwd(), log_dir)):
    os.mkdir(log_dir, 0755)

log_file = "app.log"
log_path = os.path.join(log_dir, log_file)
fh = logging.FileHandler(log_path)
fh.setLevel(logging.DEBUG)

# create formatter
fmt = "%(asctime)-15s, %(levelname)s, %(filename)s, line=%(lineno)d, PID=%(process)d, %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)

if __name__ == "__main__":
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
