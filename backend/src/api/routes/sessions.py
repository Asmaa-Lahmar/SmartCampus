"""Routes de session. SC-15 (Se déconnecter) remplace ce fichier par sa version complète."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["sessions"])
