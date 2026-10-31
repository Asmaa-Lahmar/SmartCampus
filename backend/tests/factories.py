from collections.abc import Callable

from fastapi.testclient import TestClient

from src.models.user import Role, User
from tests.helpers import auth_header, login


def headers_for(
    client: TestClient, make_user: Callable[..., User], role: Role = Role.ETUDIANT
) -> dict[str, str]:
    """Crée un compte du rôle demandé, le connecte et renvoie l'en-tête Authorization (SC-17)."""
    email = f"{role.value}@usms.ac.ma"
    make_user(email=email, role=role)
    token = login(client, email=email).json()["access_token"]
    return auth_header(token)
