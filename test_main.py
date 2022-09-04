from fastapi.testclient import TestClient
import sys

from main import app

client = TestClient(app)

# Test Application Status
# Making sure it runs properly without crashing


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

    print(response.json())
    assert response.json() == {"status": True,
                               "python": sys.version, "env": 'test'}
