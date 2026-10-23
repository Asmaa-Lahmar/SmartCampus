from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from src.api.deps import CurrentSession, get_current_session, get_current_user
from src.api.routes.login import UserOut
from src.database import get_db
from src.models.user import User
from src.services import audit_service, token_service

router = APIRouter(prefix="/api/auth", tags=["sessions"])


@router.get("/me", response_model=UserOut)
def me(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    session: Annotated[CurrentSession, Depends(get_current_session)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    token_service.revoke(db, session.jti, session.user.id, session.expires_at)
    ip = request.client.host if request.client else None
    audit_service.record(db, "LOGOUT", actor=session.user, ip=ip)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
