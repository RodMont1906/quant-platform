import logging
import os
import sys

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

# Load environment variables from .env
load_dotenv()


def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d"
    )
    handler.setFormatter(formatter)

    # Explicitly attach loggers used in the platform
    for logger_name in ["quant-platform", "http_logger", "CostTracker", "LLMRouting"]:
        log = logging.getLogger(logger_name)
        log.setLevel(log_level)
        log.addHandler(handler)
        log.propagate = False


def get_logger(name: str = "quant-platform") -> logging.Logger:
    return logging.getLogger(name)
