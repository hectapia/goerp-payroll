# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for database URL auto-correction functionality."""

from __future__ import annotations

import importlib

from goerp_payroll import config


def run_correction_logic(url: str, dyno: bool = False) -> str:
    """Helper function that mimics the correction logic in config.py for testing."""
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

    DATABASE_URL_BASE = url
    DATABASE_URL_CORREGIDA = DATABASE_URL_BASE

    prefix = DATABASE_URL_BASE.split(":", 1)[0]

    if dyno and prefix in ("postgres", "postgresql"):
        parsed = urlparse(DATABASE_URL_BASE)
        query = parse_qs(parsed.query)
        query["sslmode"] = ["require"]
        DATABASE_URL_CORREGIDA = urlunparse(parsed._replace(scheme="postgresql", query=urlencode(query, doseq=True)))
    else:
        match prefix:
            case "postgresql" | "postgres":
                parsed = urlparse(DATABASE_URL_BASE)
                query = parse_qs(parsed.query)
                query.pop("sslmode", None)
                new_query = urlencode(query, doseq=True) if query else ""
                cleaned = urlunparse(parsed._replace(query=new_query))
                offset = 10 if prefix == "postgresql" else 8
                DATABASE_URL_CORREGIDA = "postgresql+pg8000" + cleaned[offset:]
            case "mysql":
                DATABASE_URL_CORREGIDA = "mysql+mysqlconnector" + DATABASE_URL_BASE[5:]
            case "mariadb":
                DATABASE_URL_CORREGIDA = "mariadb+mariadbconnector" + DATABASE_URL_BASE[7:]

    return DATABASE_URL_CORREGIDA


def test_sqlite_url_unchanged():
    url = "sqlite:///:memory:"
    assert run_correction_logic(url) == url


def test_postgres_url_correction():
    url = "postgres://coati_user:pass@localhost:5432/coati_db"
    expected = "postgresql+pg8000://coati_user:pass@localhost:5432/coati_db"
    assert run_correction_logic(url) == expected


def test_postgresql_url_correction():
    url = "postgresql://coati_user:pass@localhost:5432/coati_db"
    expected = "postgresql+pg8000://coati_user:pass@localhost:5432/coati_db"
    assert run_correction_logic(url) == expected


def test_mysql_url_correction():
    url = "mysql://coati_user:pass@localhost:3306/coati_db"
    expected = "mysql+mysqlconnector://coati_user:pass@localhost:3306/coati_db"
    assert run_correction_logic(url) == expected


def test_mariadb_url_correction():
    url = "mariadb://coati_user:pass@localhost:3306/coati_db"
    expected = "mariadb+mariadbconnector://coati_user:pass@localhost:3306/coati_db"
    assert run_correction_logic(url) == expected


def test_heroku_postgres_correction():
    url = "postgres://coati_user:pass@localhost:5432/coati_db"
    expected = "postgresql://coati_user:pass@localhost:5432/coati_db?sslmode=require"
    assert run_correction_logic(url, dyno=True) == expected


def test_neon_postgres_url_correction():
    url = "postgresql://neondb_owner:npg_secret@ep-cool-123.us-east-2.aws.neon.tech/neondb?sslmode=require"
    expected = "postgresql+pg8000://neondb_owner:npg_secret@ep-cool-123.us-east-2.aws.neon.tech/neondb"
    assert run_correction_logic(url) == expected


def test_module_reload_mysql_correction(monkeypatch):
    # Test reloading the configuration module with a simulated mysql DATABASE_URL in environment
    monkeypatch.setenv("DATABASE_URL", "mysql://coati_user:pass@localhost:3306/coati_db")

    # Reload the config module to trigger its database correction logic
    importlib.reload(config)

    assert (
        config.CONFIGURACION["SQLALCHEMY_DATABASE_URI"]
        == "mysql+mysqlconnector://coati_user:pass@localhost:3306/coati_db"
    )

    # Clean up by reloading config in default state
    monkeypatch.delenv("DATABASE_URL", raising=False)
    importlib.reload(config)


def test_module_reload_neon_ssl_engine_options(monkeypatch):
    # Test reloading config with a Neon PostgreSQL DATABASE_URL containing sslmode=require
    neon_url = "postgresql://neondb_owner:npg_pass@ep-cool-123.us-east-2.aws.neon.tech/neondb?sslmode=require"
    monkeypatch.setenv("DATABASE_URL", neon_url)

    importlib.reload(config)

    db_uri = config.CONFIGURACION["SQLALCHEMY_DATABASE_URI"]
    if "postgresql+psycopg2" in str(db_uri):
        assert "ep-cool-123" in str(db_uri)
    else:
        assert (
            config.CONFIGURACION["SQLALCHEMY_DATABASE_URI"]
            == "postgresql+pg8000://neondb_owner:npg_pass@ep-cool-123.us-east-2.aws.neon.tech/neondb"
        )
        engine_opts = config.CONFIGURACION.get("SQLALCHEMY_ENGINE_OPTIONS", {})
        assert "connect_args" in engine_opts
        assert "ssl_context" in engine_opts["connect_args"]

    # Clean up
    monkeypatch.delenv("DATABASE_URL", raising=False)
    importlib.reload(config)


