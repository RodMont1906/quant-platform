import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Setup named logger
logger = logging.getLogger("http_logger")

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        "%(timestamp)s %(method)s %(path)s %(status_code)d %(duration_sec)f %(client)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = datetime.utcnow()
        response = await call_next(request)
        duration = (datetime.utcnow() - start).total_seconds()

        log_entry = {
            "timestamp": start.isoformat(),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_sec": duration,
            "client": request.client.host,
        }

        logger.info(log_entry)
        return response
