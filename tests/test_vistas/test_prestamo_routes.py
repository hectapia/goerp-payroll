# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for loan (prestamo) routes."""

from tests.helpers.auth import login_user


def test_prestamo_index_requires_authentication(app, client, db_session):
    """Test that loan index requires authentication."""
    with app.app_context():
        response = client.get("/prestamo/", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_prestamo_index_for_admin(app, client, admin_user, db_session):
    """Test that admin can access loan index."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/prestamo/")
        assert response.status_code == 200


def test_prestamo_new_requires_authentication(app, client, db_session):
    """Test that creating a new loan requires authentication."""
    with app.app_context():
        response = client.get("/prestamo/new", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_prestamo_new_requires_write_access(app, client, db_session):
    """Test that creating a new loan requires write access."""
    with app.app_context():
        from goerp_payroll.enums import TipoUsuario
        from tests.factories.user_factory import create_user

        # Create AUDIT user (read-only)
        audit_user = create_user(db_session, "auditor", "password", tipo=TipoUsuario.AUDIT)
        login_user(client, audit_user.usuario, "password")

        response = client.get("/prestamo/new", follow_redirects=False)
        # Should not allow access (403 or redirect)
        assert response.status_code in [302, 403]


def test_prestamo_edit_requires_authentication(app, client, db_session):
    """Test that editing a loan requires authentication."""
    with app.app_context():
        response = client.get("/prestamo/999/edit", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_prestamo_view_requires_authentication(app, client, db_session):
    """Test that viewing loan details requires authentication."""
    with app.app_context():
        response = client.get("/prestamo/999", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_prestamo_approve_requires_authentication(app, client, db_session):
    """Test that approving a loan requires authentication."""
    with app.app_context():
        response = client.post("/prestamo/999/approve", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location
