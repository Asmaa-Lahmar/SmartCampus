"""Crée un compte de démonstration par rôle, plus un compte désactivé (SC-12).

Usage, depuis le dossier backend :  python -m src.seed
Le script peut être relancé : il ne recrée pas un compte qui existe déjà.
"""

from sqlalchemy import select

from src.config import settings
from src.database import SessionLocal
from src.models.user import Role, User
from src.services.security import hash_password

DEMO_ACCOUNTS = [
    ("etudiant", "Étudiant Démo", Role.ETUDIANT, True),
    ("enseignant", "Enseignant Démo", Role.ENSEIGNANT, True),
    ("gestionnaire", "Gestionnaire Démo", Role.GESTIONNAIRE, True),
    ("scolarite", "Agent Scolarité Démo", Role.SCOLARITE, True),
    ("admin", "Administrateur Démo", Role.ADMINISTRATEUR, True),
    ("desactive", "Compte Désactivé Démo", Role.ETUDIANT, False),
]


def main() -> None:
    domain = settings.allowed_email_domain.lower()
    with SessionLocal() as db:
        for local_part, full_name, role, is_active in DEMO_ACCOUNTS:
            email = f"{local_part}@{domain}"
            if db.scalar(select(User).where(User.email == email)) is not None:
                print(f"déjà présent : {email}")
                continue
            db.add(
                User(
                    email=email,
                    full_name=full_name,
                    role=role,
                    is_active=is_active,
                    password_hash=hash_password(settings.seed_password),
                )
            )
            print(f"créé         : {email} ({role.value})")
        db.commit()
    print("Mot de passe de ces comptes : valeur SEED_PASSWORD de backend/.env")


if __name__ == "__main__":
    main()
