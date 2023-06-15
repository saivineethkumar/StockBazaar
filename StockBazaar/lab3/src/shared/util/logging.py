
import logging


def logger(service):
    logger = logging.getLogger(service)
    logger.setLevel(logging.DEBUG)
    console_logger = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(threadName)s (%(thread)d)] [%(levelname)s] - %(message)s')
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)
    return logger
