import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/address")
async def get_address():
    return {
        "street": "1600 Amphitheatre Parkway",
        "city": "Mountain View",
        "state": "California",
        "country": "United States",
        "postcode": os.getenv("POSTCODE", "00000")  # ✅ Read dynamically
    }

