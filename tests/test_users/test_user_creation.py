# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for user creation and management."""

from sqlalchemy import func, select
from goerp_payroll.model import Usuario
from tests.factories.user_factory import create_user
from tests.helpers.assertions import assert_user_exists


def test_create_user_with_factory(app, db_session):
    """
    Test creating a user using the factory function.

    Setup:
        - Clean database

    Action:
        - Create user with factory

    Verification:
        - User exists in database
        - User has correct attributes
    """
    with app.app_context():
        user = create_user(
            db_session,
            usuario="testuser",
            password="testpass",
            nombre="John",
            apellido="Doe",
            correo_electronico="john@example.com",
            tipo="admin",
        )

        # Verify user was created
        assert user.id is not None
        assert user.usuario == "testuser"
        assert user.nombre == "John"
        assert user.apellido == "Doe"
        assert user.correo_electronico == "john@example.com"
        assert user.tipo == "admin"
        assert user.activo is True


def test_user_persists_in_database(app, db_session):
    """
    Test that created user persists in database.

    Setup:
        - Create user with factory

    Action:
        - Query database for user

    Verification:
        - User can be retrieved from database
        - All attributes match
    """
    with app.app_context():
        # Create user
        created_user = create_user(
            db_session,
            usuario="persistuser",
            password="pass123",
            nombre="Jane",
            apellido="Smith",
        )

        # Query database directly
        found_user = assert_user_exists(db_session, "persistuser")

        # Verify attributes
        assert found_user.id == created_user.id
        assert found_user.nombre == "Jane"
        assert found_user.apellido == "Smith"


def test_multiple_users_can_be_created(app, db_session):
    """
    Test creating multiple users in the same test.

    Setup:
        - Clean database

    Action:
        - Create multiple users

    Verification:
        - All users exist in database
        - Users have unique IDs
    """
    with app.app_context():
        user1 = create_user(db_session, "user1", "pass1", nombre="User", apellido="One")
        user2 = create_user(db_session, "user2", "pass2", nombre="User", apellido="Two")
        user3 = create_user(db_session, "user3", "pass3", nombre="User", apellido="Three")

        # Verify all exist
        assert_user_exists(db_session, "user1")
        assert_user_exists(db_session, "user2")
        assert_user_exists(db_session, "user3")

        # Verify unique IDs
        assert user1.id != user2.id
        assert user2.id != user3.id
        assert user1.id != user3.id


def test_admin_user_can_be_created(app, db_session):
    """
    Test creating an admin user.

    Setup:
        - Clean database

    Action:
        - Create admin user

    Verification:
        - User type is 'admin'
        - User exists in database
    """
    with app.app_context():
        admin = create_user(
            db_session,
            usuario="admin123",
            password="adminpass",
            tipo="admin",
        )

        assert admin.tipo == "admin"

        # Verify in database
        found = assert_user_exists(db_session, "admin123")
        assert found.tipo == "admin"


def test_user_with_minimal_data(app, db_session):
    """
    Test creating user with only required fields.

    Setup:
        - Clean database

    Action:
        - Create user with minimal data

    Verification:
        - User is created successfully
        - Optional fields have default values
    """
    with app.app_context():
        user = create_user(
            db_session,
            usuario="minimaluser",
            password="password",
        )

        assert user.id is not None
        assert user.usuario == "minimaluser"
        assert user.nombre == "Test"  # Default
        assert user.apellido == "User"  # Default
        assert user.tipo == "admin"  # Default
        assert user.activo is True  # Default


def test_users_in_parallel_tests_are_isolated(app, db_session):
    """
    Test that users created in this test don't affect other tests.

    This test demonstrates the isolation principle - each test
    starts with a clean database and its changes are rolled back.

    Setup:
        - Clean database

    Action:
        - Create users
        - Verify they exist

    Verification:
        - Users exist in current test
        - Will be rolled back and won't affect other tests
    """
    with app.app_context():
        # Create users in this test
        create_user(db_session, "isolated1", "pass1")
        create_user(db_session, "isolated2", "pass2")

        # Verify they exist in current session
        assert_user_exists(db_session, "isolated1")
        assert_user_exists(db_session, "isolated2")

        # Count total users
        total = db_session.execute(select(func.count(Usuario.id))).scalar() or 0
        assert total == 2

        # These users will be rolled back after this test completes
