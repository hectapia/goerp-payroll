# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for carga inicial prestacion routes."""

from tests.helpers.auth import login_user


def test_carga_inicial_index_requires_authentication(app, client, db_session):
    """Test that carga inicial index requires authentication."""
    with app.app_context():
        response = client.get("/carga-inicial-prestaciones/", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_carga_inicial_index_for_admin(app, client, admin_user, db_session):
    """Test that admin can access carga inicial index."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/carga-inicial-prestaciones/")
        assert response.status_code == 200


def test_carga_inicial_new_requires_authentication(app, client, db_session):
    """Test that creating a new carga inicial requires authentication."""
    with app.app_context():
        response = client.get("/carga-inicial-prestaciones/nueva", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_carga_inicial_new_requires_write_access(app, client, db_session):
    """Test that creating a new carga inicial requires write access."""
    with app.app_context():
        from goerp_payroll.enums import TipoUsuario
        from tests.factories.user_factory import create_user

        # Create AUDIT user (read-only)
        audit_user = create_user(db_session, "auditor", "password", tipo=TipoUsuario.AUDIT)
        login_user(client, audit_user.usuario, "password")

        response = client.get("/carga-inicial-prestaciones/nueva", follow_redirects=False)
        # Should not allow access (403 or redirect)
        assert response.status_code in [302, 403]


def test_carga_inicial_edit_requires_authentication(app, client, db_session):
    """Test that editing a carga inicial requires authentication."""
    with app.app_context():
        response = client.get("/carga-inicial-prestaciones/999/editar", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location


def test_carga_inicial_delete_requires_authentication(app, client, db_session):
    """Test that deleting a carga inicial requires authentication."""
    with app.app_context():
        response = client.post("/carga-inicial-prestaciones/999/eliminar", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.location
