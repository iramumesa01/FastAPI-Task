import pytest
import importlib
import logging
from unittest.mock import patch
from fastapi import Request
from fastapi.responses import Response
from fastapi.testclient import TestClient
from app.main import app
from app.core import config
from app.middleware.logging import log_requests
from app.routers.address import get_address

client = TestClient(app)

# ✅ Config Test: Ensure POSTCODE loads correctly from env
@patch("app.core.config.os.getenv", return_value="94043")
def test_config_postcode(mock_getenv):
    importlib.reload(config)  
    assert config.POSTCODE == "94043"

# ✅ Middleware Test: Ensure logging middleware logs requests
@pytest.mark.asyncio
@patch("logging.info")
async def test_logging_middleware(mock_log):
    async def mock_call_next(request):
        return Response(content="Mock Response", status_code=200)

    request = Request(scope={"type": "http", "method": "GET", "path": "/", "headers": []})
    await log_requests(request, mock_call_next)

    mock_log.assert_called()

# ✅ Router Test: Ensure get_address() returns correct data
@pytest.mark.asyncio
@patch("app.routers.address.os.getenv", return_value="12345")
async def test_get_address(mock_getenv):
    response = await get_address()
    assert response["postcode"] == "12345"

# ✅ Router Test: Ensure default postcode is used when env var is missing
@pytest.mark.asyncio
@patch("app.routers.address.os.getenv", return_value=None)
async def test_get_address_default(mock_getenv):
    response = await get_address()
    assert response["postcode"] == "00000"

# ✅ Router Test: Ensure response contains all expected keys
@pytest.mark.asyncio
@patch("app.routers.address.os.getenv", return_value="67890")
async def test_get_address_response_structure(mock_getenv):
    response = await get_address()
    expected_keys = {"street", "city", "state", "country", "postcode"}
    assert set(response.keys()) == expected_keys

# ✅ Router Test: Ensure empty postcode is handled correctly
@pytest.mark.asyncio
@patch("app.routers.address.os.getenv", return_value="")
async def test_get_address_empty_postcode(mock_getenv):
    response = await get_address()
    assert response["postcode"] == ""


# ✅ User Route Test: Ensure /api/users/{user_id} returns correct response
def test_get_user():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "name": "John Doe", "email": "john@example.com"}

# ✅ User Route Test: Ensure /api/users/{user_id} returns 404 for non-existent user
def test_get_user_not_found():
    response = client.get("/api/users/999")  # Non-existent user
    assert response.status_code == 404

# ✅ Test invalid user_id type (string instead of integer)
def test_get_user_invalid_type():
    response = client.get("/api/users/abc")
    assert response.status_code == 422

# ✅ Test: Negative user_id
def test_get_user_negative():
    response = client.get("/api/users/-1")
    assert response.status_code == 404  # Should return Not Found

# ✅ Test: Large user_id value
def test_get_user_large_value():
    response = client.get("/api/users/9999999999999999999")
    assert response.status_code == 404

# ✅ Test: Ensure POST is not allowed
def test_post_user_not_allowed():
    response = client.post("/api/users/1")
    assert response.status_code == 405  # Method Not Allowed

# ✅ Test: Ensure response is always JSON
def test_get_user_response_type():
    response = client.get("/api/users/1")
    assert response.headers["Content-Type"].startswith("application/json")

# ✅ Test: Ensure /api/users/{user_id}/ (with trailing slash) works
def test_get_user_trailing_slash():
    response = client.get("/api/users/1/")
    assert response.status_code == 200

# ✅ Test: Ensure headers are included in response
def test_get_user_headers():
    response = client.get("/api/users/1")
    assert "Content-Type" in response.headers


# ✅ Test: API response time should be acceptable
def test_api_response_time():
    import time
    start_time = time.time()
    response = client.get("/api/users/1")
    end_time = time.time()
    assert (end_time - start_time) < 1  # Response should be under 1 second

# ✅ Test: Ensure get_address() handles None postcode correctly
@pytest.mark.asyncio
@patch("app.routers.address.os.getenv", return_value=None)
async def test_get_address_none_postcode(mock_getenv):
    response = await get_address()
    assert response["postcode"] == "00000"

# ✅ Test: Ensure get_address() handles empty space postcode
@pytest.mark.asyncio
@patch("app.routers.address.os.getenv", return_value=" ")
async def test_get_address_empty_space_postcode(mock_getenv):
    response = await get_address()
    assert response["postcode"] == " "

# ✅ Test: Ensure get_address() does not return unexpected keys
@pytest.mark.asyncio
@patch("app.routers.address.os.getenv", return_value="67890")
async def test_get_address_no_extra_keys(mock_getenv):
    response = await get_address()
    expected_keys = {"street", "city", "state", "country", "postcode"}
    assert set(response.keys()) == expected_keys

# ✅ Test: API response with unexpected query parameters
def test_get_user_with_extra_params():
    response = client.get("/api/users/1?extra_param=value")
    assert response.status_code == 200
    assert "user_id" in response.json()

# ✅ Test: User API - Edge cases for user_id
@pytest.mark.parametrize("user_id, expected_status", [
    (0, 404),               # Edge case: user_id is zero
    (-1, 404),              # Edge case: user_id is negative
    ("abc", 422),          # Edge case: user_id is a string
    (9999999999, 404)       # Edge case: user_id is extremely large
])
def test_get_user_edge_cases(user_id, expected_status):
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == expected_status


# ✅ Test: Middleware - Logging when request has special characters
@pytest.mark.asyncio
@patch("logging.info")
async def test_logging_middleware_special_chars(mock_log):
    async def mock_call_next(request):
        return Response(content="Mock Response", status_code=200)
    
    request = Request(scope={
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"user-agent", b"test-client!@#$%")]
    })
    await log_requests(request, mock_call_next)
    mock_log.assert_called()
