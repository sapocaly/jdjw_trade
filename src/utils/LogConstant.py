import logging
import logging.config

__author__ = 'Sapocaly'

logging.config.fileConfig("conf/jdjw_trade_logger.cfg")

FETCH_DIGEST_LOGGER = logging.getLogger("jdjw_trade_fetch_digest")
FETCH_DIGEST_LOGGER_ALERT = logging.getLogger("jdjw_trade_fetch_digest.alert")
DAL_DIGEST_LOGGER = logging.getLogger("jdjw_trade_dal")
DAL_DIGEST_LOGGER_ERROR = logging.getLogger("jdjw_trade_dal.err")
