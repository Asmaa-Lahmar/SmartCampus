"""Consultation des salles (SC-20)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.room import Room, RoomStatus
from src.services.common import ServiceError

ROOM_NOT_FOUND = "Salle introuvable."


def list_rooms(db: Session, include_archived: bool = False) -> list[Room]:
    """Salles triées par bâtiment puis code ; les archivées seulement sur demande."""
    statement = select(Room)
    if not include_archived:
        statement = statement.where(Room.status != RoomStatus.ARCHIVEE)
    return list(db.scalars(statement.order_by(Room.building, Room.code)))


def get_room(db: Session, room_id: int, include_archived: bool = False) -> Room:
    """Une salle ; 404 si elle n'existe pas, ou si elle est archivée et que ce n'est pas demandé."""
    room = db.get(Room, room_id)
    if room is None or (room.status == RoomStatus.ARCHIVEE and not include_archived):
        raise ServiceError(404, ROOM_NOT_FOUND)
    return room
