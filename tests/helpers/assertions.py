# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Assertion helpers for tests."""

from sqlalchemy import select

from goerp_payroll.model import Usuario


def assert_user_exists(db_session, usuario):
    """
    Assert that a user exists in the database.

    Args:
        db_session: SQLAlchemy session
        usuario: Username to check

    Raises:
        AssertionError: If user does not exist
    """
    user = db_session.execute(select(Usuario).filter_by(usuario=usuario)).scalar_one_or_none()
    assert user is not None, f"User '{usuario}' should exist in database"
    return user


def assert_redirected_to(response, expected_location):
    """
    Assert that response is a redirect to the expected location.

    Args:
        response: Flask response object
        expected_location: Expected redirect location (can be partial match)

    Raises:
        AssertionError: If not a redirect or wrong location
    """
    assert response.status_code in (301, 302, 303, 307, 308), f"Expected redirect but got status {response.status_code}"

    location = response.headers.get("Location", "")
    assert expected_location in location, f"Expected redirect to contain '{expected_location}' but got '{location}'"
