"""Blocage après 3 échecs consécutifs (SC-14 pour SC-16 et SC-13 : EF-AUTH-04, RG-02)."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from src.models.audit_log import AuditLog
from src.services.common import INVALID_CREDENTIALS
from tests.helpers import EMAIL, IP, login, reload_user


def fail(client, times: int):
    return [login(client, password="faux") for _ in range(times)]


def test_three_consecutive_failures_lock_the_account_for_15_minutes(client, db, make_user):
    make_user()
    first, second, third = fail(client, 3)
    assert first.status_code == second.status_code == 401
    assert third.status_code == 423
    assert "Réessayez dans 15 min" in third.json()["detail"]

    user = reload_user(db)
    assert user.locked_until is not None
    remaining = (user.locked_until - datetime.now(UTC)).total_seconds() / 60
    assert 14 < remaining <= 15


def test_lock_is_logged_with_date_email_and_ip(client, db, make_user):
    make_user()
    fail(client, 3)
    db.expire_all()
    actions = db.scalars(select(AuditLog.action).order_by(AuditLog.id)).all()
    assert actions == ["LOGIN_FAILED", "LOGIN_FAILED", "LOGIN_FAILED", "ACCOUNT_LOCKED"]
    locked = db.scalar(select(AuditLog).where(AuditLog.action == "ACCOUNT_LOCKED"))
    assert locked.actor_email == EMAIL
    assert locked.ip_address == IP
    assert locked.created_at is not None


def test_locked_account_refuses_the_right_password(client, make_user):
    make_user()
    fail(client, 3)
    response = login(client)
    assert response.status_code == 423
    assert "Compte bloqué" in response.json()["detail"]


def test_sc13_fourth_attempt_shows_lock_message_not_generic_message(client, make_user):
    """SC-13 : après trois échecs, la 4e tentative annonce le blocage et le délai."""
    make_user()
    fail(client, 3)
    response = login(client, password="faux")
    assert response.status_code == 423
    assert response.json()["detail"] != INVALID_CREDENTIALS
    assert "Réessayez dans" in response.json()["detail"]


def test_two_failures_then_success_reset_the_counter(client, db, make_user):
    make_user()
    fail(client, 2)
    assert login(client).status_code == 200
    user = reload_user(db)
    assert user.failed_attempts == 0
    # Le compteur repart de zéro : deux nouveaux échecs ne bloquent pas
    assert [r.status_code for r in fail(client, 2)] == [401, 401]


def test_account_unlocks_after_15_minutes(client, db, make_user):
    make_user()
    fail(client, 3)
    user = reload_user(db)
    user.locked_until = datetime.now(UTC) - timedelta(seconds=1)
    db.commit()
    assert login(client).status_code == 200


def test_expired_lock_restarts_the_count(client, db, make_user):
    make_user()
    fail(client, 3)
    user = reload_user(db)
    user.locked_until = datetime.now(UTC) - timedelta(seconds=1)
    db.commit()
    assert login(client, password="faux").status_code == 401


def test_unknown_email_failures_are_logged(client, db):
    login(client, email="inconnu@usms.ac.ma")
    entry = db.scalar(select(AuditLog))
    assert entry.action == "LOGIN_FAILED"
    assert entry.actor_id is None
    assert entry.actor_email == "inconnu@usms.ac.ma"


def test_successful_login_is_logged(client, db, make_user):
    make_user()
    login(client)
    assert db.scalar(select(AuditLog.action)) == "LOGIN_SUCCESS"
