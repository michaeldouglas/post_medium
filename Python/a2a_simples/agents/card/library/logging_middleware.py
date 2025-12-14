import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from library.request_context import request_id_ctx

logger = logging.getLogger("a2a")


class A2ALoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        token = request_id_ctx.set(request_id)

        start_time = time.perf_counter()
        request.state.request_id = request_id

        response: Response | None = None

        logger.info(
            "request.start",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            },
        )

        try:
            response = await call_next(request)
            return response
        except Exception:
            logger.exception("request.error")
            raise
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "request.end",
                extra={
                    "status_code": response.status_code if response else None,
                    "duration_ms": round(duration_ms, 2),
                },
            )

            request_id_ctx.reset(token)
