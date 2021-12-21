import sys
import os
import logging
from datetime import datetime


from utils.constants import ROOT_PATH


# Constants
NOW_STR = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE_NAME = f"task.{NOW_STR}.log"
LOG_FILE_PATH = os.path.join(ROOT_PATH, LOG_FILE_NAME)


def get_logger():
    return logging.getLogger(__name__)


def setup_logging():
    # Create a logger
    logger = get_logger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s %(message)s")

    # Configure a console output
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)

    # Configure a file output
    file_handler = logging.FileHandler(LOG_FILE_PATH, mode="w", encoding="Utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
