"""Hachage des mots de passe (bcrypt) et jetons d'accès (PyJWT) - ENF-01, ENF-02."""

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from src.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=settings.bcrypt_rounds)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # Mot de passe de plus de 72 octets ou empreinte illisible : refus simple
        return False


def create_access_token(
    user_id: int, role: str, minutes: int | None = None
) -> tuple[str, datetime]:
    """Renvoie le jeton signé et sa date d'expiration (30 min par défaut)."""
    now = datetime.now(UTC)
    duration = settings.access_token_minutes if minutes is None else minutes
    expires_at = now + timedelta(minutes=duration)
    payload = {
        "sub": str(user_id),
        "role": role,
        "jti": uuid.uuid4().hex,  # identifiant unique, utile pour révoquer le jeton
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, expires_at


def decode_access_token(token: str) -> dict[str, Any]:
    """Lève jwt.ExpiredSignatureError ou jwt.InvalidTokenError si le jeton est refusé."""
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["exp", "sub", "jti"]},
    )
