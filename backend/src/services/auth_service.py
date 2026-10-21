"""Service d'authentification : vérifie les identifiants et émet le jeton.

Version SC-11 : domaine de l'établissement (RG-11) et compte désactivé.
SC-16 ajoute le blocage après 3 échecs.
"""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.models.user import User
from src.services.common import INVALID_CREDENTIALS, AuthError
from src.services.security import create_access_token, verify_password

DOMAIN_REFUSED = "Utilisez votre adresse e-mail institutionnelle (@{domain})."
ACCOUNT_DISABLED = "Votre compte est désactivé. Contactez l'administration de l'établissement."


@dataclass
class LoginResult:
    access_token: str
    expires_at: datetime
    user: User


def normalize_email(email: str) -> str:
    return email.strip().lower()


def is_institutional_email(email: str) -> bool:
    return normalize_email(email).endswith("@" + settings.allowed_email_domain.lower())


def find_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == normalize_email(email)))


def authenticate(db: Session, email: str, password: str, ip: str | None = None) -> LoginResult:
    if not is_institutional_email(email):
        raise AuthError(400, DOMAIN_REFUSED.format(domain=settings.allowed_email_domain))

    user = find_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise AuthError(401, INVALID_CREDENTIALS)

    # Vérifié après le mot de passe : on ne révèle rien à qui ignore le mot de passe
    if not user.is_active:
        raise AuthError(403, ACCOUNT_DISABLED)

    token, expires_at = create_access_token(user.id, user.role.value)
    return LoginResult(access_token=token, expires_at=expires_at, user=user)
