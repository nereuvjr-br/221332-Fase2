from fastapi.testclient import TestClient

import api

client = TestClient(api.app)


def test_status_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "online"
    assert payload["docs"] == "/docs"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analisar_requires_api_key():
    response = client.post("/analisar", json={"texto": "Great movie"})
    assert response.status_code == 401


def test_analisar_success(monkeypatch):
    monkeypatch.setattr(
        api,
        "process_pipeline",
        lambda text: {"texto_original": text, "sentimento": {"classificacao": "Positivo"}},
    )
    response = client.post(
        "/analisar",
        json={"texto": "Great movie"},
        headers={"X-API-Key": "dev-api-key"},
    )
    assert response.status_code == 200
    assert response.json()["texto_original"] == "Great movie"
