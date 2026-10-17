import re
from dataclasses import dataclass

import bcrypt

MSG_SUCCES = "Connexion réussie"
MSG_CHAMPS_VIDES = "Email et mot de passe obligatoires"
MSG_EMAIL_INVALIDE = "Format d'email invalide"
MSG_ECHEC = "Identifiants incorrects"

EMAIL_REGEX = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


@dataclass(frozen=True)
class LoginResult:
    success: bool
    message: str


def _est_vide(valeur):
    return not isinstance(valeur, str) or not valeur.strip()


def hacher_mot_de_passe(password):
    
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class LoginService:
    def __init__(self, annuaire):
       
        self._annuaire = annuaire

    def login(self, email, password):
        if _est_vide(email) or _est_vide(password):     
            return LoginResult(False, MSG_CHAMPS_VIDES)
        email = email.strip()
        if not EMAIL_REGEX.match(email):                
            return LoginResult(False, MSG_EMAIL_INVALIDE)
        hache = self._annuaire.get(email)
        if hache is None or not bcrypt.checkpw(password.encode("utf-8"), hache):  
            return LoginResult(False, MSG_ECHEC)
        return LoginResult(True, MSG_SUCCES)
