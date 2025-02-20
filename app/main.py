import os
import logging
from fastapi import FastAPI, Request
from app.config import POSTCODE

os.makedirs("logs", exist_ok=True)


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)

app = FastAPI()

# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Outgoing response: {response.status_code}")
    return response

# API route to return address
@app.get("/address")
async def get_address():
    return {
        "street": "123 Main St",
        "city": "Sample City",
        "postcode": POSTCODE
    }
