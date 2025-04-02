import requests 
import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/address")
async def get_address():
    postcode = os.getenv("POSTCODE")
    if postcode is None: 
        postcode = "00000"

    return {
        "street": "1600 Amphitheatre Parkway",
        "city": "Mountain View",
        "state": "California",
        "country": "United States",
        "postcode": postcode
    }

