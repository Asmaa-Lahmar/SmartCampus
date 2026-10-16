
import re
from dataclasses import dataclass

MSG_SUCCES = "Connexion réussie"
MSG_CHAMPS_VIDES = "Email et mot de passe obligatoires"
MSG_EMAIL_INVALIDE = "Format d'email invalide"
MSG_ECHEC = "Identifiants incorrects"

EMAIL_REGEX = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


@dataclass(frozen=True)
class LoginResult:
    success: bool
    message: str


class LoginService:
    """Valide les identifiants d'un utilisateur (CA1 à CA3 de SC-11)."""

    def __init__(self, annuaire):
        # annuaire : {email: mot_de_passe}, simule la base des utilisateurs
        self._annuaire = annuaire

    def login(self, email, password):
        if not email or not password:                   # CA2
            return LoginResult(False, MSG_CHAMPS_VIDES)
        if not EMAIL_REGEX.match(email):                # CA2
            return LoginResult(False, MSG_EMAIL_INVALIDE)
        if self._annuaire.get(email) != password:       # CA3
            return LoginResult(False, MSG_ECHEC)
        return LoginResult(True, MSG_SUCCES)         