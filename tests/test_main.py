import os
import logging
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import POSTCODE
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)

# Test - Config loading
def test_config_loading():
    assert POSTCODE.isdigit(), "Postcode should be a numeric string"

# Test - Logging Middleware
def test_logging_middleware(caplog):
    with caplog.at_level(logging.INFO):
        response = client.get("/address")
        assert response.status_code == 200
        assert "Incoming request" in caplog.text
        assert "Outgoing response" in caplog.text

# Test - Correct Address response
def test_get_address():
    response = client.get("/address")
    assert response.status_code == 200
    assert "street" in response.json()
    assert "city" in response.json()
    assert "postcode" in response.json()

# Test - Handles Different Postcodes
def test_different_postcodes(monkeypatch):
    monkeypatch.setenv("POSTCODE", "98765")
    response = client.get("/address")
    assert response.json()["postcode"] == "98765"

# Test - Invalid Route
def test_invalid_route():
    response = client.get("/wrong-url")
    assert response.status_code == 404

# Test - Missing Environment Variable
def test_missing_env_variable(monkeypatch):
    monkeypatch.delenv("POSTCODE", raising=False)
    response = client.get("/address")
    assert "postcode" in response.json()

# Test - Empty Fields
def test_empty_response_fields(monkeypatch):
    monkeypatch.setenv("POSTCODE", "")
    response = client.get("/address")
    assert response.json()["postcode"] == ""

# Test - Large Input Handling
def test_large_input_handling(monkeypatch):
    monkeypatch.setenv("POSTCODE", "9" * 100)  # 100-character postcode
    response = client.get("/address")
    assert len(response.json()["postcode"]) == 100

# Test - Invalid HTTP Methods
@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_invalid_http_methods(method):
    response = getattr(client, method)("/address")
    assert response.status_code in [405, 400], "Should not allow non-GET requests"