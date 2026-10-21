"""Table users : comptes et état de connexion (SC-12)."""

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, func, true
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Role(enum.StrEnum):
    ETUDIANT = "etudiant"
    ENSEIGNANT = "enseignant"
    GESTIONNAIRE = "gestionnaire"
    SCOLARITE = "scolarite"
    ADMINISTRATEUR = "administrateur"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150))
    role: Mapped[Role] = mapped_column(
        Enum(
            Role,
            name="user_role",
            native_enum=False,
            length=20,
            values_callable=lambda roles: [r.value for r in roles],
        )
    )
    # Statut du compte : un compte désactivé ne peut plus se connecter (SC-11)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=true())
    # Empreinte bcrypt, jamais le mot de passe en clair (ENF-01)
    password_hash: Mapped[str] = mapped_column(String(255))
    # Compteur d'échecs consécutifs et fin du blocage (RG-02, SC-16)
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
