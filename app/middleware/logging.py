import logging
from fastapi import Request

async def log_requests(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Outgoing response: {response.status_code}")
    return response


