from fastapi import FastAPI, APIRouter, HTTPException

app = FastAPI()

router = APIRouter()

@router.get("/users/{user_id}")  # Attach route to router
async def get_user(user_id: int):
    if user_id != 1:  # Assuming only user 1 exists
        raise HTTPException(status_code=404, detail="User not found")  # FIX: Raise 404

    return {"user_id": 1, "name": "John Doe", "email": "john@example.com"}
