

import math
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from src.config import settings
from src.models.user import User
from src.services import audit_service
from src.services.common import AuthError

ACCOUNT_LOCKED = (
    "Compte bloqué temporairement après {attempts} échecs de connexion. "
    "Réessayez dans {minutes} min."
)


def _now() -> datetime:
    return datetime.now(UTC)


def is_locked(user: User, now: datetime | None = None) -> bool:
    now = now or _now()
    return user.locked_until is not None and user.locked_until > now


def locked_error(user: User, now: datetime | None = None) -> AuthError:
    now = now or _now()
    assert user.locked_until is not None
    minutes = max(1, math.ceil((user.locked_until - now).total_seconds() / 60))
    message = ACCOUNT_LOCKED.format(attempts=settings.max_failed_attempts, minutes=minutes)
    return AuthError(423, message)


def ensure_not_locked(user: User) -> None:
    if is_locked(user):
        raise locked_error(user)


def register_failure(db: Session, user: User, ip: str | None) -> None:
   
    now = _now()
    if user.locked_until is not None and user.locked_until <= now:
        # Le blocage précédent est terminé : on repart de zéro
        user.locked_until = None
        user.failed_attempts = 0

    user.failed_attempts += 1
    audit_service.record(
        db, "LOGIN_FAILED", actor=user, target=f"échec {user.failed_attempts}", ip=ip
    )

    if user.failed_attempts >= settings.max_failed_attempts:
        user.locked_until = now + timedelta(minutes=settings.lock_minutes)
        audit_service.record(
            db, "ACCOUNT_LOCKED", actor=user, target=f"jusqu'à {user.locked_until:%H:%M} UTC", ip=ip
        )
        db.commit()
        raise locked_error(user, now)

    db.commit()


def register_success(db: Session, user: User, ip: str | None) -> None:
    
    user.failed_attempts = 0
    user.locked_until = None
    audit_service.record(db, "LOGIN_SUCCESS", actor=user, ip=ip)
    db.commit()
