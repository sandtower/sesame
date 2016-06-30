from server.weixin import server
from util.logger import logger

import logging
_logger = logging.getLogger(__name__)



while True:
    try:
        server()
    except Exception as e:
        _logger.exception(e)
