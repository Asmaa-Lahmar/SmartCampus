
INVALID_CREDENTIALS = "E-mail ou mot de passe incorrect"


class AuthError(Exception):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
