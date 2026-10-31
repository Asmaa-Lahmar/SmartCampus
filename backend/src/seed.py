"""Données de démonstration : un compte par rôle (SC-12) et les salles du campus (SC-20).

Usage, depuis le dossier backend :  python -m src.seed
Le script peut être relancé : il ne recrée pas ce qui existe déjà.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.database import SessionLocal
from src.models.room import Room, RoomStatus, RoomType
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

# (code, bâtiment, type, capacité, statut, description)
DEMO_ROOMS = [
    ("AMPHI-A", "Bâtiment A", RoomType.AMPHITHEATRE, 200, RoomStatus.ACTIVE,
     "Grand amphithéâtre, accès par le hall principal."),
    ("A-101", "Bâtiment A", RoomType.SALLE_COURS, 40, RoomStatus.ACTIVE, None),
    ("A-102", "Bâtiment A", RoomType.SALLE_TD, 30, RoomStatus.ACTIVE, None),
    ("A-103", "Bâtiment A", RoomType.SALLE_TD, 30, RoomStatus.HORS_SERVICE, "Vidéoprojecteur en réparation."),
    ("B-201", "Bâtiment B", RoomType.SALLE_TP, 24, RoomStatus.ACTIVE, "Laboratoire informatique, 24 postes."),
    ("B-202", "Bâtiment B", RoomType.SALLE_TP, 20, RoomStatus.ACTIVE, "Laboratoire réseaux."),
    ("C-001", "Bâtiment C", RoomType.SALLE_TRAVAIL, 8, RoomStatus.ACTIVE,
     "Salle de travail en groupe, rez-de-chaussée de la bibliothèque."),
    ("C-002", "Bâtiment C", RoomType.SALLE_TRAVAIL, 6, RoomStatus.ACTIVE, None),
    ("D-001", "Bâtiment D", RoomType.SALLE_COURS, 35, RoomStatus.ARCHIVEE, "Ancienne salle, remplacée par A-101."),
]


def seed_accounts(db: Session) -> None:
    domain = settings.allowed_email_domain.lower()
    for local_part, full_name, role, is_active in DEMO_ACCOUNTS:
        email = f"{local_part}@{domain}"
        if db.scalar(select(User).where(User.email == email)) is not None:
            print(f"déjà présent  : {email}")
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
        print(f"créé          : {email} ({role.value})")
    db.flush()


def seed_rooms(db: Session) -> None:
    for code, building, room_type, capacity, status, description in DEMO_ROOMS:
        if db.scalar(select(Room).where(Room.code == code)) is not None:
            print(f"déjà présente : salle {code}")
            continue
        db.add(
            Room(
                code=code,
                building=building,
                room_type=room_type,
                capacity=capacity,
                status=status,
                description=description,
            )
        )
        print(f"créée         : salle {code}")
    db.flush()


def main() -> None:
    with SessionLocal() as db:
        seed_accounts(db)
        seed_rooms(db)
        db.commit()
    print("Mot de passe des comptes : valeur SEED_PASSWORD de backend/.env")


if __name__ == "__main__":
    main()
