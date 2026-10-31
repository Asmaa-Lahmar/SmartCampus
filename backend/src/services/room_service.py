"""Consultation des salles (SC-20, SC-21 : EF-ROOM-01)."""

from dataclasses import dataclass

from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session

from src.models.room import Room, RoomStatus, RoomType
from src.services.common import ServiceError

ROOM_NOT_FOUND = "Salle introuvable."


@dataclass
class RoomFilters:
    """Critères de la liste des salles (SC-21)."""

    query: str | None = None  # code ou bâtiment, sans tenir compte des majuscules
    building: str | None = None
    room_type: RoomType | None = None
    min_capacity: int | None = None  # nombre de participants (RG-08)


def apply_filters(statement: Select[tuple[Room]], filters: RoomFilters) -> Select[tuple[Room]]:
    if filters.query and filters.query.strip():
        pattern = f"%{filters.query.strip()}%"
        statement = statement.where(or_(Room.code.ilike(pattern), Room.building.ilike(pattern)))
    if filters.building:
        statement = statement.where(Room.building == filters.building)
    if filters.room_type:
        statement = statement.where(Room.room_type == filters.room_type)
    if filters.min_capacity:
        statement = statement.where(Room.capacity >= filters.min_capacity)
    return statement


def list_rooms(db: Session, include_archived: bool = False, filters: RoomFilters | None = None) -> list[Room]:
    """Salles triées par bâtiment puis code ; les archivées seulement sur demande."""
    statement = select(Room)
    if not include_archived:
        statement = statement.where(Room.status != RoomStatus.ARCHIVEE)
    if filters is not None:
        statement = apply_filters(statement, filters)
    return list(db.scalars(statement.order_by(Room.building, Room.code)))


def get_room(db: Session, room_id: int, include_archived: bool = False) -> Room:
    """Une salle ; 404 si elle n'existe pas, ou si elle est archivée et que ce n'est pas demandé."""
    room = db.get(Room, room_id)
    if room is None or (room.status == RoomStatus.ARCHIVEE and not include_archived):
        raise ServiceError(404, ROOM_NOT_FOUND)
    return room
