"""Service d'authentification : vérifie les identifiants et émet le jeton.

Version SC-12 : contrôle de l'e-mail et du mot de passe.
SC-11 ajoute le domaine et le compte désactivé ; SC-16 ajoute le blocage.
"""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User
from src.services.common import INVALID_CREDENTIALS, AuthError
from src.services.security import create_access_token, verify_password


@dataclass
class LoginResult:
    access_token: str
    expires_at: datetime
    user: User


def normalize_email(email: str) -> str:
    return email.strip().lower()


def find_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == normalize_email(email)))


def authenticate(db: Session, email: str, password: str, ip: str | None = None) -> LoginResult:
    user = find_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise AuthError(401, INVALID_CREDENTIALS)

    token, expires_at = create_access_token(user.id, user.role.value)
    return LoginResult(access_token=token, expires_at=expires_at, user=user)
