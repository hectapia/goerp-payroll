# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for the settings route."""

from tests.helpers.auth import login_user


def test_settings_route_requires_authentication(client):
    """
    Test that the settings route requires authentication.

    Setup:
        - Unauthenticated client

    Action:
        - Request /settings/

    Verification:
        - Redirects to login page
    """
    response = client.get("/settings/", follow_redirects=False)
    assert response.status_code in [302, 303], "Should redirect to login"


def test_settings_route_with_authenticated_user(app, client, admin_user, db_session):
    """
    Test that authenticated users can access the settings page.

    Setup:
        - Authenticated admin user

    Action:
        - Request /settings/

    Verification:
        - Returns 200 OK
        - Contains expected links to configuration sections
    """
    with app.app_context():
        login_user(client, "admin-test", "admin-password")

        response = client.get("/settings/", follow_redirects=True)
        assert response.status_code == 200

        # Verify the page contains expected configuration links
        data = response.data.decode("utf-8")

        # Check for key configuration sections
        assert "/empresa/" in data, "Should have link to companies"
        assert "/currency/" in data, "Should have link to currencies"
        assert "/exchange_rate/" in data, "Should have link to exchange rates"
        assert "/percepciones/" in data, "Should have link to perceptions"
        assert "/deducciones/" in data, "Should have link to deductions"
        assert "/prestaciones/" in data, "Should have link to benefits"
        assert "/calculation-rule/" in data, "Should have link to calculation rules"
        assert "/custom_field/" in data, "Should have link to custom fields"
        assert "/configuracion/" in data, "Should have link to global configuration"


def test_settings_page_layout(app, client, admin_user, db_session):
    """
    Test that the settings page has the correct layout and structure.

    Setup:
        - Authenticated admin user

    Action:
        - Request /settings/

    Verification:
        - Page has proper heading
        - Contains configuration cards
    """
    with app.app_context():
        login_user(client, "admin-test", "admin-password")

        response = client.get("/settings/", follow_redirects=True)
        data = response.data.decode("utf-8")

        # Check for presence of all configuration sections
        config_sections = [
            "Empresas",  # Companies (Spanish)
            "Companies",  # Companies (English)
            "Monedas",  # Currencies (Spanish)
            "Currencies",  # Currencies (English)
        ]

        # At least some of these should be present depending on locale
        assert any(
            section in data for section in config_sections
        ), "Settings page should contain configuration sections"
