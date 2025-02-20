# FastAPI Task 

This is a simple **FastAPI backend** that exposes an API endpoint to return an address. The postcode is retrieved from environment variables.

## Features
✅ FastAPI framework for high performance  
✅ Supports environment variables (`.env`)  
✅ `/address` endpoint returns a JSON response  
✅ Uses `uvicorn` for local development  
✅ Logs requests and responses  

Create a virtual environment & install dependencies
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
pip install -r requirements.txt  

Create a .env file and add:
POSTCODE=12345

Start the FastAPI server
uvicorn app.main:app --reload

Open in browser:
API: http://127.0.0.1:8000/address
