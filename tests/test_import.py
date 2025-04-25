from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_import_gmail_emails():
    response = client.post("/sources/import/gmail")
    assert response.status_code == 200
    assert "emails imported" in response.json()["message"]