from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_topic_validation():
    response = client.post(
        "/api/guides",
        data={"topic": "a"},
        files={"file": ("test.pdf", b"%PDF-1.4", "application/pdf")},
    )
    assert response.status_code == 422

def test_rejects_non_pdf():
    response = client.post(
        "/api/guides",
        data={"topic": "photosynthesis"},
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415
