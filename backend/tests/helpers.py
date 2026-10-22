"""Outils communs aux tests de l'API (SC-14)."""

from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User

PASSWORD = "MotDePasse-2026"
EMAIL = "etudiant@usms.ac.ma"
IP = "testclient"  # adresse que TestClient transmet à l'API


def login(client: TestClient, email: str = EMAIL, password: str = PASSWORD) -> Response:
    return client.post("/api/auth/login", json={"email": email, "password": password})


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def reload_user(db: Session, email: str = EMAIL) -> User:
    """Relit le compte en base : l'API l'a modifié dans une autre session."""
    db.expire_all()
    user = db.scalar(select(User).where(User.email == email))
    assert user is not None
    return user
