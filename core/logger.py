# logger.py
import logging


def get_logger():
    logger = logging.getLogger(__name__)
    if len(logger.handlers) == 0:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        fh = logging.FileHandler(filename='./server.log')
        formatter = logging.Formatter(
            "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)  # 将日志输出至屏幕
        logger.addHandler(fh)  # 将日志输出至文件
    return logger
