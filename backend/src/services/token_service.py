"""Révocation des jetons à la déconnexion (SC-15).

Un JWT ne s'annule pas seul : son identifiant (jti) est inscrit dans revoked_tokens
et chaque requête authentifiée vérifie qu'il n'y figure pas.
"""

from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.models.revoked_token import RevokedToken


def revoke(db: Session, jti: str, user_id: int, expires_at: datetime) -> None:
    if db.get(RevokedToken, jti) is None:
        db.add(RevokedToken(jti=jti, user_id=user_id, expires_at=expires_at))
    purge_expired(db)


def is_revoked(db: Session, jti: str) -> bool:
    return db.scalar(select(RevokedToken.jti).where(RevokedToken.jti == jti)) is not None


def purge_expired(db: Session) -> None:
    """Supprime les jetons déjà expirés : ils sont refusés par leur date de toute façon."""
    db.execute(delete(RevokedToken).where(RevokedToken.expires_at < datetime.now(UTC)))
