"""Route de connexion POST /api/auth/login (SC-12, SC-11)."""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import Role
from src.services.auth_service import authenticate

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255, examples=["etudiant@usms.ac.ma"])
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: Role


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserOut


@router.post("/login", response_model=LoginResponse)
def login(
    body: LoginRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> LoginResponse:
    """Renvoie un jeton valable 30 min ; 401 si l'e-mail ou le mot de passe est faux."""
    ip = request.client.host if request.client else None
    result = authenticate(db, body.email, body.password, ip)
    return LoginResponse(
        access_token=result.access_token,
        expires_at=result.expires_at,
        user=UserOut.model_validate(result.user),
    )
