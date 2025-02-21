# FastAPI Task 

This is a simple **FastAPI backend** that exposes an API endpoint to return an address. The postcode is retrieved from environment variables.

## Features That Make It Production-Grade
Environment Variables Support: Uses .env file to store configuration values securely.

Logging: Implements structured logging for monitoring requests and responses.

Modular Code Structure: Organized into separate files (main.py, config.py) for maintainability.

Dependency Management: Uses requirements.txt to ensure consistent package installation.

Auto-reloading Server: Uses uvicorn --reload for efficient development. 

## To ensure production readiness, the following resources were referenced:
https://devdocs.io/fastapi/

https://github.com/zhanymkanov/fastapi-best-practices

https://12factor.net/

https://docs.python.org/3/howto/logging.html

##  Create a virtual environment & install dependencies
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
pip install -r requirements.txt  

## Create a .env file and add:
POSTCODE=12345

## Start the FastAPI server
uvicorn app.main:app --reload

## Open in browser:
API: http://127.0.0.1:8000/address

## Example API Response
{

  "street": "123 Main Street",
  
  "city": "New York",
  
  "postcode": "12345"
  
}
