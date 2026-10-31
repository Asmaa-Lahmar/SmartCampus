"""Données de démonstration : le script se relance sans doublon (SC-20)."""

from sqlalchemy import func, select

from src import seed
from src.models.room import Room, RoomStatus, RoomType
from src.models.user import User


def run_seed(db) -> None:
    seed.seed_accounts(db)
    seed.seed_rooms(db)
    db.commit()


def count(db, model) -> int:
    return db.scalar(select(func.count()).select_from(model))


def test_seed_creates_accounts_and_rooms(db):
    run_seed(db)
    assert count(db, User) == len(seed.DEMO_ACCOUNTS)
    assert count(db, Room) == len(seed.DEMO_ROOMS)
    types = set(db.scalars(select(Room.room_type)))
    # Les types utilisés par RG-09 sont présents
    assert {RoomType.SALLE_TD, RoomType.SALLE_TRAVAIL, RoomType.AMPHITHEATRE} <= types
    assert db.scalar(select(Room.status).where(Room.code == "D-001")) == RoomStatus.ARCHIVEE


def test_seed_can_run_twice_without_duplicates(db):
    run_seed(db)
    run_seed(db)
    assert count(db, User) == len(seed.DEMO_ACCOUNTS)
    assert count(db, Room) == len(seed.DEMO_ROOMS)
