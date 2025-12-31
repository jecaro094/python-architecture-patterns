
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request

from model import exceptions as ex

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except ex.AllocationException as exception:
            return JSONResponse(
                status_code=400,
                content={"detail": exception.message},
            )

        except Exception:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )