# src/core/security/middleware.py

import re

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class InputValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.max_body_size = 10000  # 10KB
        self.injection_patterns = [
            r"ignore.*previous.*instructions",
            r"system.*prompt",
            r"you.*are.*now",
            # Add more prompt injection regexes
        ]

    async def dispatch(self, request: Request, call_next):
        body = await request.body()

        if len(body) > self.max_body_size:
            return JSONResponse(
                status_code=413, content={"detail": "Request body too large"}
            )

        body_str = body.decode("utf-8", errors="ignore")
        for pattern in self.injection_patterns:
            if re.search(pattern, body_str, re.IGNORECASE):
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Potential prompt injection detected"},
                )

        return await call_next(request)
