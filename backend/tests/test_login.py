"""Connexion POST /api/auth/login (SC-14 pour SC-11 et SC-12 : EF-AUTH-01, EF-AUTH-03, RG-11)."""

from datetime import UTC, datetime

from src.models.user import Role
from src.services.common import INVALID_CREDENTIALS
from tests.helpers import EMAIL, PASSWORD, login


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_valid_login_returns_30_minute_token(client, make_user):
    make_user()
    response = login(client)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"] == {
        "id": body["user"]["id"],
        "email": EMAIL,
        "full_name": "Étudiant Test",
        "role": "etudiant",
    }
    expires_at = datetime.fromisoformat(body["expires_at"])
    minutes = (expires_at - datetime.now(UTC)).total_seconds() / 60
    assert 29 < minutes <= 30


def test_email_is_case_and_space_insensitive(client, make_user):
    make_user()
    assert login(client, email="  Etudiant@USMS.ac.ma ").status_code == 200


def test_wrong_password_gives_generic_message(client, make_user):
    make_user()
    response = login(client, password="faux")
    assert response.status_code == 403
    assert response.json() == {"detail": INVALID_CREDENTIALS}


def test_unknown_email_gives_same_generic_message(client, make_user):
    make_user()
    response = login(client, email="inconnu@usms.ac.ma")
    assert response.status_code == 401
    assert response.json() == {"detail": INVALID_CREDENTIALS}


def test_email_outside_domain_is_refused(client, make_user):
    make_user(email="etudiant@gmail.com")
    response = login(client, email="etudiant@gmail.com")
    assert response.status_code == 400
    assert "@usms.ac.ma" in response.json()["detail"]


def test_disabled_account_is_refused_with_admin_message(client, make_user):
    make_user(is_active=False)
    response = login(client)
    assert response.status_code == 403
    assert "administration" in response.json()["detail"]


def test_disabled_account_with_wrong_password_reveals_nothing(client, make_user):
    make_user(is_active=False)
    response = login(client, password="faux")
    assert response.status_code == 401
    assert response.json() == {"detail": INVALID_CREDENTIALS}


def test_each_role_can_log_in(client, make_user):
    for role in Role:
        email = f"{role.value}@usms.ac.ma"
        make_user(email=email, role=role)
        response = login(client, email=email, password=PASSWORD)
        assert response.status_code == 200
        assert response.json()["user"]["role"] == role.value


def test_missing_fields_are_rejected(client):
    assert client.post("/api/auth/login", json={"email": EMAIL}).status_code == 422
