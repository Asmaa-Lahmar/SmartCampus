from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.login_service import MSG_ECHEC, LoginService, hacher_mot_de_passe

app = FastAPI(title="SmartCampus API")

# Compte de démonstration : sera remplacé par la table User (PostgreSQL)
service = LoginService({"etudiant@ensa.ma": hacher_mot_de_passe("Secret123")})


class LoginRequest(BaseModel):
    # Champs libres : la validation (CA2) reste dans LoginService
    email: str | None = None
    password: str | None = None


@app.post("/api/auth/login")
def login(req: LoginRequest):
    result = service.login(req.email, req.password)
    if not result.success:
        code = 401 if result.message == MSG_ECHEC else 400
        raise HTTPException(status_code=code, detail=result.message)
    return {"message": result.message}


@app.get("/health")
def health():
    return {"status": "ok"}
