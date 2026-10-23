"""Table revoked_tokens : jetons invalidés par la déconnexion (SC-15)."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    # Identifiant unique du jeton (champ « jti » du JWT)
    jti: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    # Après cette date le jeton est expiré de toute façon : la ligne peut être purgée
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
