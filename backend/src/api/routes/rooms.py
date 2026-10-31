"""Salles : liste pour tous, création, modification et archivage par le gestionnaire
(SC-20 : EF-ROOM-04, ENF-03)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from src.api.deps import FORBIDDEN, get_current_user, require_roles
from src.database import get_db
from src.models.room import Room, RoomStatus, RoomType
from src.models.user import Role, User
from src.services import room_admin_service, room_service
from src.services.common import ServiceError
from src.services.room_admin_service import RoomChanges

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

CurrentUser = Annotated[User, Depends(get_current_user)]
Manager = Annotated[User, Depends(require_roles(Role.GESTIONNAIRE))]
Db = Annotated[Session, Depends(get_db)]

# Lettres, chiffres et tirets : A-101, AMPHI-A
CODE_PATTERN = r"^\s*[A-Za-z0-9][A-Za-z0-9-]*\s*$"


class RoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    building: str
    room_type: RoomType
    capacity: int
    status: RoomStatus
    description: str | None


class RoomCreate(BaseModel):
    code: str = Field(min_length=1, max_length=20, pattern=CODE_PATTERN, examples=["A-104"])
    building: str = Field(min_length=2, max_length=80, examples=["Bâtiment A"])
    room_type: RoomType
    capacity: int = Field(ge=1, le=500)
    description: str | None = Field(default=None, max_length=500)


class RoomUpdate(BaseModel):
    """Seuls les champs envoyés sont modifiés."""

    code: str | None = Field(default=None, min_length=1, max_length=20, pattern=CODE_PATTERN)
    building: str | None = Field(default=None, min_length=2, max_length=80)
    room_type: RoomType | None = None
    capacity: int | None = Field(default=None, ge=1, le=500)
    description: str | None = Field(default=None, max_length=500)


def client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("", response_model=list[RoomOut])
def list_rooms(user: CurrentUser, db: Db, include_archived: bool = False) -> list[Room]:
    """Salles non archivées ; le gestionnaire peut aussi voir les archivées."""
    if include_archived and user.role != Role.GESTIONNAIRE:
        raise ServiceError(403, FORBIDDEN)
    return room_service.list_rooms(db, include_archived)


@router.post("", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(body: RoomCreate, request: Request, manager: Manager, db: Db) -> Room:
    """Crée une salle « active » ; 409 si le code existe déjà, 422 si la capacité est nulle."""
    return room_admin_service.create_room(
        db, body.code, body.building, body.room_type, body.capacity, body.description,
        manager, client_ip(request),
    )


@router.patch("/{room_id}", response_model=RoomOut)
def update_room(room_id: int, body: RoomUpdate, request: Request, manager: Manager, db: Db) -> Room:
    changes = RoomChanges(**body.model_dump(exclude_unset=True))
    return room_admin_service.update_room(db, room_id, changes, manager, client_ip(request))


@router.post("/{room_id}/archive", response_model=RoomOut)
def archive_room(room_id: int, request: Request, manager: Manager, db: Db) -> Room:
    """Archive la salle : elle disparaît de la liste et de la recherche, jamais supprimée."""
    return room_admin_service.archive_room(db, room_id, manager, client_ip(request))
