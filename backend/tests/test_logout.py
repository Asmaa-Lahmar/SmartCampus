"""Jetons et déconnexion (SC-14 pour SC-15 : EF-AUTH-02, ENF-02)."""

from sqlalchemy import select

from src.models.audit_log import AuditLog
from src.services.security import create_access_token
from tests.helpers import EMAIL, auth_header, login, reload_user


def token_for(client, make_user) -> str:
    make_user()
    return login(client).json()["access_token"]


def test_me_requires_a_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_me_returns_the_connected_user(client, make_user):
    token = token_for(client, make_user)
    response = client.get("/api/auth/me", headers=auth_header(token))
    assert response.status_code == 200
    assert response.json()["email"] == EMAIL


def test_logout_invalidates_the_token(client, db, make_user):
    token = token_for(client, make_user)
    assert client.post("/api/auth/logout", headers=auth_header(token)).status_code == 204
    # Le même jeton est désormais refusé partout
    assert client.get("/api/auth/me", headers=auth_header(token)).status_code == 401
    assert client.post("/api/auth/logout", headers=auth_header(token)).status_code == 401
    assert db.scalar(select(AuditLog.action).order_by(AuditLog.id.desc())) == "LOGOUT"


def test_logout_does_not_affect_another_session(client, make_user):
    token_a = token_for(client, make_user)
    token_b = login(client).json()["access_token"]
    client.post("/api/auth/logout", headers=auth_header(token_a))
    assert client.get("/api/auth/me", headers=auth_header(token_b)).status_code == 200


def test_expired_token_is_refused(client, db, make_user):
    make_user()
    user = reload_user(db)
    token, _ = create_access_token(user.id, user.role.value, minutes=-1)
    response = client.get("/api/auth/me", headers=auth_header(token))
    assert response.status_code == 401
    assert "expirée" in response.json()["detail"]


def test_invalid_token_is_refused(client):
    response = client.get("/api/auth/me", headers=auth_header("pas-un-jeton"))
    assert response.status_code == 401


def test_token_of_disabled_account_is_refused(client, db, make_user):
    token = token_for(client, make_user)
    user = reload_user(db)
    user.is_active = False
    db.commit()
    assert client.get("/api/auth/me", headers=auth_header(token)).status_code == 401
