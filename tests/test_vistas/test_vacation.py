# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Comprehensive tests for vacation management (goerp_payroll/vistas/vacation.py)."""

from tests.helpers.auth import login_user


def test_vacation_policies_requires_authentication(app, client, db_session):
    """Test that vacation policies requires authentication."""
    with app.app_context():
        response = client.get("/vacation/policies", follow_redirects=False)
        assert response.status_code == 302


def test_vacation_policies_accessible_to_authenticated_users(app, client, admin_user, db_session):
    """Test that authenticated users can access vacation policies."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.get("/vacation/policies")
        assert response.status_code == 200


def test_vacation_accounts_requires_authentication(app, client, db_session):
    """Test that vacation accounts requires authentication."""
    with app.app_context():
        response = client.get("/vacation/accounts", follow_redirects=False)
        assert response.status_code == 302


def test_vacation_accounts_accessible_to_authenticated_users(app, client, admin_user, db_session):
    """Test that authenticated users can access vacation accounts."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.get("/vacation/accounts")
        assert response.status_code == 200


def test_vacation_leave_requests_requires_authentication(app, client, db_session):
    """Test that leave requests requires authentication."""
    with app.app_context():
        response = client.get("/vacation/leave-requests", follow_redirects=False)
        assert response.status_code == 302


def test_vacation_leave_requests_accessible_to_authenticated_users(app, client, admin_user, db_session):
    """Test that authenticated users can access leave requests."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.get("/vacation/leave-requests")
        assert response.status_code == 200


def test_vacation_policy_new_requires_write_access(app, client, db_session):
    """Test that creating vacation policies requires write access."""
    with app.app_context():
        response = client.get("/vacation/policies/new", follow_redirects=False)
        assert response.status_code == 302


def test_vacation_account_new_requires_write_access(app, client, db_session):
    """Test that creating vacation accounts requires write access."""
    with app.app_context():
        response = client.get("/vacation/accounts/new", follow_redirects=False)
        assert response.status_code == 302


def test_vacation_leave_request_new_requires_write_access(app, client, db_session):
    """Test that creating leave requests requires write access."""
    with app.app_context():
        response = client.get("/vacation/leave-requests/new", follow_redirects=False)
        assert response.status_code == 302


def test_vacation_workflow_view_all_sections(app, client, admin_user, db_session):
    """End-to-end test: View all vacation management sections."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        # Step 1: View vacation policies
        response = client.get("/vacation/policies")
        assert response.status_code == 200

        # Step 2: View vacation accounts
        response = client.get("/vacation/accounts")
        assert response.status_code == 200

        # Step 3: View leave requests
        response = client.get("/vacation/leave-requests")
        assert response.status_code == 200
