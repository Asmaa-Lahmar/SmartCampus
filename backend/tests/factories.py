"""Outils de test partagés des tickets du Sprint 2."""

from collections.abc import Callable

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.room import Room, RoomStatus, RoomType
from src.models.user import Role, User
from tests.helpers import auth_header, login


def headers_for(
    client: TestClient, make_user: Callable[..., User], role: Role = Role.ETUDIANT
) -> dict[str, str]:
    """Crée un compte du rôle demandé, le connecte et renvoie l'en-tête Authorization (SC-17)."""
    email = f"{role.value}@usms.ac.ma"
    make_user(email=email, role=role)
    token = login(client, email=email).json()["access_token"]
    return auth_header(token)


def make_room(
    db: Session,
    code: str = "A-101",
    building: str = "Bâtiment A",
    room_type: RoomType = RoomType.SALLE_COURS,
    capacity: int = 30,
    status: RoomStatus = RoomStatus.ACTIVE,
    description: str | None = None,
) -> Room:
    """Salle enregistrée directement en base (SC-20)."""
    room = Room(
        code=code,
        building=building,
        room_type=room_type,
        capacity=capacity,
        status=status,
        description=description,
    )
    db.add(room)
    db.commit()
    return room
