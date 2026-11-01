# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Additional tests for employee routes."""

from tests.helpers.auth import login_user


def test_employee_new_form_displays_for_admin(app, client, admin_user, db_session):
    """Test that admin can see new employee form."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/employee/new")
        assert response.status_code == 200


def test_employee_delete_requires_authentication(app, client, db_session):
    """Test that deleting an employee requires authentication."""
    with app.app_context():
        response = client.post("/employee/delete/999", follow_redirects=False)
        assert response.status_code == 302


def test_employee_delete_requires_write_access(app, client, db_session):
    """Test that deleting an employee requires write access."""
    with app.app_context():
        from goerp_payroll.enums import TipoUsuario
        from tests.factories.user_factory import create_user

        # Create AUDIT user (read-only)
        audit_user = create_user(db_session, "auditor", "password", tipo=TipoUsuario.AUDIT)
        login_user(client, audit_user.usuario, "password")

        response = client.post("/employee/delete/999", follow_redirects=False)
        # Should not allow access (403 or redirect)
        assert response.status_code in [302, 403]
