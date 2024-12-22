from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_llm_by_price():
    response = client.get("/llm_by_price?price=100")
    assert response.status_code == 200
    assert len(response.json()) > 0
