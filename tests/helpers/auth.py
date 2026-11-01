# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Authentication helpers for tests."""


def login_user(client, username, password):
    """
    Log in a user via the login form.

    Args:
        client: Flask test client
        username: Username to log in with
        password: Password to log in with

    Returns:
        Response: Response from the login POST request
    """
    return client.post(
        "/auth/login",
        data={
            "email": username,
            "password": password,
        },
        follow_redirects=False,
    )


def logout_user(client):
    """
    Log out the current user.

    Args:
        client: Flask test client

    Returns:
        Response: Response from the logout request
    """
    return client.post("/auth/logout", follow_redirects=False)
