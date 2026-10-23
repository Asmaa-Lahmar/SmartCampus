"""Hachage des mots de passe et jetons JWT (SC-14 : ENF-01, ENF-02)."""

from datetime import UTC, datetime

import jwt
import pytest
from sqlalchemy import select, text

from src.models.user import User
from src.services.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from tests.helpers import PASSWORD


def test_hash_password_never_returns_plain_text():
    hashed = hash_password(PASSWORD)
    assert hashed != PASSWORD
    assert hashed.startswith("$2b$")
    assert verify_password(PASSWORD, hashed)
    assert not verify_password("autre-mot-de-passe", hashed)


def test_verify_password_refuses_too_long_or_invalid_hash():
    hashed = hash_password(PASSWORD)
    assert not verify_password("x" * 100, hashed)
    assert not verify_password(PASSWORD, "empreinte-invalide")


def test_password_is_not_stored_in_plain_text(db, make_user):
    make_user()
    stored = db.scalar(select(User.password_hash))
    assert stored != PASSWORD
    # Aucune colonne de la table ne contient le mot de passe en clair
    rows = db.execute(text("SELECT * FROM users")).all()
    assert all(PASSWORD not in str(value) for row in rows for value in row)


def test_access_token_lasts_30_minutes_and_carries_identity():
    token, expires_at = create_access_token(42, "etudiant")
    payload = decode_access_token(token)
    assert payload["sub"] == "42"
    assert payload["role"] == "etudiant"
    assert payload["jti"]
    minutes = (expires_at - datetime.now(UTC)).total_seconds() / 60
    assert 29 < minutes <= 30


def test_expired_token_is_rejected():
    token, _ = create_access_token(42, "etudiant", minutes=-1)
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_tampered_token_is_rejected():
    token, _ = create_access_token(42, "etudiant")
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token[:-2] + "xx")
