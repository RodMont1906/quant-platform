import logging
import os

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

# Load environment variables from .env
load_dotenv()


def get_logger(name: str = "quant-platform") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger  # Avoid duplicate handlers

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    log_handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        ("%(asctime)s %(levelname)s %(name)s %(message)s " "%(filename)s %(lineno)d")
    )

    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    return logger
