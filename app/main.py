import os
import logging
from fastapi import FastAPI, Request
from app.core.config import POSTCODE 
from app.middleware.logging import log_requests
from app.routers.address import router as address_router

os.makedirs("logs", exist_ok=True)


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)

app = FastAPI()

app.middleware("http")(log_requests)

app.include_router(address_router)