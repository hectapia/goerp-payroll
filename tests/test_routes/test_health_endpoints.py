# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for health and readiness endpoints."""

import json


def test_health_endpoint_returns_ok(client):
    """
    Test that /health endpoint returns 200 OK.

    The health endpoint should always return 200 OK if the application is running,
    without requiring authentication or database access.

    Setup:
        - Client without authentication

    Action:
        - GET /health

    Verification:
        - Status code is 200
        - Response contains {"status": "ok"}
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"


def test_health_endpoint_no_authentication_required(client):
    """
    Test that /health endpoint does not require authentication.

    This is critical for container orchestration tools to check
    if the application is running.

    Setup:
        - Client without authentication

    Action:
        - GET /health

    Verification:
        - Status code is 200 (not 302 redirect)
        - No redirect to login page
    """
    response = client.get("/health", follow_redirects=False)

    assert response.status_code == 200
    assert "login" not in response.location if response.location else True


def test_ready_endpoint_returns_ok_when_db_available(app, client):
    """
    Test that /ready endpoint returns 200 OK when database is available.

    The readiness endpoint should check database connectivity and return
    200 OK if the application is ready to serve traffic.

    Setup:
        - App with database initialized
        - Client without authentication

    Action:
        - GET /ready

    Verification:
        - Status code is 200
        - Response contains {"status": "ok"}
    """
    response = client.get("/ready")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"


def test_ready_endpoint_no_authentication_required(client):
    """
    Test that /ready endpoint does not require authentication.

    This is critical for container orchestration tools to check
    if the application is ready to serve traffic.

    Setup:
        - Client without authentication

    Action:
        - GET /ready

    Verification:
        - Status code is 200 or 503 (not 302 redirect)
        - No redirect to login page
    """
    response = client.get("/ready", follow_redirects=False)

    # Should return either 200 (ready) or 503 (not ready), but not redirect
    assert response.status_code in [200, 503]
    assert "login" not in response.location if response.location else True


def test_ready_endpoint_json_response_format(client):
    """
    Test that /ready endpoint returns proper JSON response.

    Setup:
        - Client without authentication

    Action:
        - GET /ready

    Verification:
        - Response is valid JSON
        - Response contains "status" field
    """
    response = client.get("/ready")

    # Should be valid JSON
    data = json.loads(response.data)
    assert "status" in data
    assert data["status"] in ["ok", "unavailable"]


def test_health_endpoint_json_response_format(client):
    """
    Test that /health endpoint returns proper JSON response.

    Setup:
        - Client without authentication

    Action:
        - GET /health

    Verification:
        - Response is valid JSON
        - Response contains "status" field with value "ok"
    """
    response = client.get("/health")

    # Should be valid JSON
    data = json.loads(response.data)
    assert "status" in data
    assert data["status"] == "ok"
