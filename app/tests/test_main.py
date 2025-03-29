import os
import logging
import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from fastapi.testclient import TestClient
client = TestClient(app)

# ✅ Test - Config loading
def test_config_loading():
    postcode = os.getenv("POSTCODE", "00000")  # Use default if unset
    assert postcode.isdigit(), "Postcode should be a numeric string"

# ✅ Test - Logging Middleware
def test_logging_middleware(caplog):
    with caplog.at_level(logging.INFO):
        response = client.get("/address")
        assert response.status_code == 200
        # Ensure logging middleware actually logs these messages
        assert any("Incoming request" in record.message for record in caplog.records)
        assert any("Outgoing response" in record.message for record in caplog.records)

# ✅ Test - Correct Address Response
def test_get_address():
    response = client.get("/address")
    assert response.status_code == 200
    assert all(key in response.json() for key in ["street", "city", "postcode"])

# ✅ Test - Handles Different Postcodes 
def test_different_postcodes(monkeypatch):
    monkeypatch.setenv("POSTCODE", "98765")  # Set a new postcode
    response = client.get("/address")
    assert response.status_code == 200
    assert response.json()["postcode"] == "98765"  # Should match new value

# ✅ Test - Invalid Route
def test_invalid_route():
    response = client.get("/wrong-url")
    assert response.status_code == 404

# ✅ Test - Missing Environment Variable
def test_missing_env_variable(monkeypatch):
    monkeypatch.delenv("POSTCODE", raising=False)  # Remove POSTCODE
    response = client.get("/address")
    assert response.status_code == 200
    assert response.json()["postcode"] == "00000"  # Should return default

# ✅ Test - Empty Fields 
def test_empty_response_fields(monkeypatch):
    monkeypatch.setenv("POSTCODE", "")  # Set empty value
    response = client.get("/address")
    assert response.status_code == 200
    assert response.json()["postcode"] == ""

# ✅ Test - Large Input Handling 
def test_large_input_handling(monkeypatch):
    large_postcode = "9" * 100  # 100-character postcode
    monkeypatch.setenv("POSTCODE", large_postcode)
    response = client.get("/address")
    assert response.status_code == 200
    assert response.json()["postcode"] == large_postcode  # Should match input

# ✅ Test - Invalid HTTP Methods
@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_invalid_http_methods(method):
    response = getattr(client, method)("/address")
    assert response.status_code in [405, 400], "Should not allow non-GET requests"
