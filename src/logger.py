import datetime
import logging
import os
from util import WORKSPACE

LOG_DIR = os.path.join(WORKSPACE, "logs")

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

log_file = os.path.join(LOG_DIR, f"log-{datetime.datetime.now().date()}.log")
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def info(msg, *args, **kwargs):
    logger.info(msg, args, kwargs)


def warn(msg, *args, **kwargs):
    logger.warning(msg, args, kwargs)


def error(msg, *args, **kwargs):
    logger.error(msg, args, kwargs)

def log(ex):
    error(ex)
