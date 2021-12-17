import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename='../logs/log.log', level=logging.DEBUG, force=True, format=LOG_FORMAT)
logger = logging.getLogger()
