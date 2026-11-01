# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for logout functionality."""

from tests.helpers.assertions import assert_redirected_to
from tests.helpers.auth import login_user, logout_user


def test_logout_redirects_to_login(client, app, admin_user):
    """
    Test that logout redirects to login page.

    Setup:
        - Create and login admin user

    Action:
        - Access logout endpoint

    Verification:
        - Response redirects to login
    """
    # Login first
    login_user(client, "admin-test", "admin-password")

    # Then logout
    response = logout_user(client)

    assert response.status_code in (302, 303)
    assert_redirected_to(response, "/auth/login")


def test_logout_clears_session(client, app, admin_user):
    """
    Test that logout clears the user session.

    Setup:
        - Create and login admin user

    Action:
        - Logout user
        - Try to access protected page

    Verification:
        - User is redirected to login (not authenticated)
    """
    # Login first
    login_user(client, "admin-test", "admin-password")

    # Verify we can access protected page
    response = client.get("/")
    assert response.status_code == 200

    # Logout
    logout_user(client)

    # Try to access protected page again
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (302, 303)
    assert_redirected_to(response, "/auth/login")


def test_logout_without_login(client):
    """
    Test logout when not logged in.

    Setup:
        - No user logged in

    Action:
        - Access logout endpoint

    Verification:
        - Still redirects to login (no error)
    """
    response = logout_user(client)

    assert response.status_code in (302, 303)
    assert_redirected_to(response, "/auth/login")
