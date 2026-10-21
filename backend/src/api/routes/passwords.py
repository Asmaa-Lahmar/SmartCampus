"""Routes des mots de passe.

Aucune route au Sprint 1 : la réinitialisation par e-mail arrive au Sprint 2 (SC-18).
Le routeur existe déjà parce que main.py l'inclut.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/auth/password", tags=["passwords"])
