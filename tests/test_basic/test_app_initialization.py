# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for application initialization and basic functionality."""


def test_app_is_created(app):
    """
    Test that the Flask application is created successfully.

    Setup:
        - Use the app fixture

    Action:
        - Verify app exists and is in testing mode

    Verification:
        - App is not None
        - TESTING flag is True
    """
    assert app is not None
    assert app.config["TESTING"] is True


def test_database_is_sqlite_memory(app):
    """
    Test that the database is configured to use SQLite in memory.

    Setup:
        - Use the app fixture

    Action:
        - Check the database URI

    Verification:
        - Database URI uses SQLite in-memory
    """
    assert "sqlite:///:memory:" in app.config["SQLALCHEMY_DATABASE_URI"]


def test_database_tables_exist(app, db_session):
    """
    Test that database tables are created.

    Setup:
        - Use app and db_session fixtures

    Action:
        - Query table names from database

    Verification:
        - Usuario table exists
        - Other essential tables exist
    """
    from goerp_payroll.model import db

    with app.app_context():
        # Get all table names
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        # Verify essential tables exist
        assert "usuario" in tables
        assert "empresa" in tables
        assert "empleado" in tables


def test_csrf_is_disabled_in_testing(app):
    """
    Test that CSRF protection is disabled for testing.

    Setup:
        - Use the app fixture

    Action:
        - Check CSRF configuration

    Verification:
        - WTF_CSRF_ENABLED is False
    """
    assert app.config["WTF_CSRF_ENABLED"] is False


def test_session_isolation(app, db_session):
    """
    Test that each test has isolated database session.

    Setup:
        - Use app and db_session fixtures

    Action:
        - Create a user in the session
        - Don't commit

    Verification:
        - User exists in current session
        - Will be rolled back after test
    """
    from goerp_payroll.auth import proteger_passwd
    from goerp_payroll.model import Usuario

    with app.app_context():
        user = Usuario()
        user.usuario = "test-isolation"
        user.acceso = proteger_passwd("password")
        user.nombre = "Test"
        user.apellido = "Isolation"
        user.tipo = "admin"
        user.activo = True

        db_session.add(user)
        db_session.flush()

        # Verify user exists in current session
        from sqlalchemy import select

        found = db_session.execute(select(Usuario).filter_by(usuario="test-isolation")).scalar_one_or_none()
        assert found is not None
        assert found.usuario == "test-isolation"
