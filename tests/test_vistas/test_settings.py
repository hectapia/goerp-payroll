# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Comprehensive tests for settings page (goerp_payroll/vistas/settings.py)."""

from tests.helpers.auth import login_user


def test_settings_index_requires_authentication(app, client, db_session):
    """Test that settings page requires authentication."""
    with app.app_context():
        response = client.get("/settings/", follow_redirects=False)
        assert response.status_code == 302


def test_settings_index_requires_write_access(app, client, db_session):
    """Test that settings page requires write access."""
    with app.app_context():
        from goerp_payroll.enums import TipoUsuario
        from tests.factories.user_factory import create_user

        # Create AUDIT user (read-only)
        audit_user = create_user(db_session, "auditor", "password", tipo=TipoUsuario.AUDIT)
        login_user(client, audit_user.usuario, "password")

        response = client.get("/settings/", follow_redirects=False)
        # Should not allow access (403 or redirect)
        assert response.status_code in [302, 403]


def test_settings_index_shows_for_admin(app, client, admin_user, db_session):
    """Test that settings page displays for admin users."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.get("/settings/")
        assert response.status_code == 200
        # Should contain settings-related content
        assert b"settings" in response.data.lower() or b"configuraci" in response.data.lower()


def test_settings_index_shows_for_hhrr(app, client, db_session):
    """Test that settings page displays for HR users."""
    with app.app_context():
        from goerp_payroll.enums import TipoUsuario
        from tests.factories.user_factory import create_user

        # Create HHRR user
        hhrr_user = create_user(db_session, "hr_user", "password", tipo=TipoUsuario.HHRR)
        login_user(client, hhrr_user.usuario, "password")

        response = client.get("/settings/")
        assert response.status_code == 200
