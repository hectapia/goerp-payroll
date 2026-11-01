# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Additional tests for exchange rate routes."""

from tests.helpers.auth import login_user


def test_exchange_rate_index_requires_authentication(app, client, db_session):
    """Test that exchange rate index requires authentication."""
    with app.app_context():
        response = client.get("/exchange_rate/", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_exchange_rate_index_for_admin(app, client, admin_user, db_session):
    """Test that admin can access exchange rate index."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/exchange_rate/")
        assert response.status_code == 200


def test_exchange_rate_new_requires_authentication(app, client, db_session):
    """Test that creating a new exchange rate requires authentication."""
    with app.app_context():
        response = client.get("/exchange_rate/new", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_exchange_rate_new_requires_write_access(app, client, db_session):
    """Test that creating a new exchange rate requires write access."""
    with app.app_context():
        from goerp_payroll.enums import TipoUsuario
        from tests.factories.user_factory import create_user

        # Create AUDIT user (read-only)
        audit_user = create_user(db_session, "auditor", "password", tipo=TipoUsuario.AUDIT)
        login_user(client, audit_user.usuario, "password")

        response = client.get("/exchange_rate/new", follow_redirects=False)
        # Should not allow access (403 or redirect)
        assert response.status_code in [302, 403]


def test_exchange_rate_edit_requires_authentication(app, client, db_session):
    """Test that editing an exchange rate requires authentication."""
    with app.app_context():
        response = client.get("/exchange_rate/edit/999", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_exchange_rate_delete_requires_authentication(app, client, db_session):
    """Test that deleting an exchange rate requires authentication."""
    with app.app_context():
        response = client.post("/exchange_rate/delete/999", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_exchange_rate_import_requires_authentication(app, client, db_session):
    """Test that importing exchange rates requires authentication."""
    with app.app_context():
        response = client.get("/exchange_rate/import", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location
