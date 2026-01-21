from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def api_client() -> TestClient:
    from src.main import app

    client = TestClient(app)
    return client
