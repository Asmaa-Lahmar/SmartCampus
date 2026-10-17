from fastapi.testclient import TestClient

from src.login_service import MSG_CHAMPS_VIDES, MSG_ECHEC, MSG_SUCCES
from src.main import app

client = TestClient(app)


def test_connexion_api_ok():  # CA1
    r = client.post("/api/auth/login", json={"email": "etudiant@ensa.ma", "password": "Secret123"})
    assert r.status_code == 200
    assert r.json()["message"] == MSG_SUCCES


def test_connexion_api_champs_vides():  # CA2
    r = client.post("/api/auth/login", json={})
    assert r.status_code == 400
    assert r.json()["detail"] == MSG_CHAMPS_VIDES


def test_connexion_api_echec():  # CA3
    r = client.post("/api/auth/login", json={"email": "etudiant@ensa.ma", "password": "Faux"})
    assert r.status_code == 401
    assert r.json()["detail"] == MSG_ECHEC


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
