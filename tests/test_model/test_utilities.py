# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for model utility functions."""

from datetime import datetime, timezone

from goerp_payroll.model import (
    generador_codigo_empleado,
    generador_de_codigos_unicos,
    utc_now,
)


def test_generador_de_codigos_unicos_returns_string():
    """
    Test that ULID generator returns a string.

    Setup:
        - None

    Action:
        - Call generador_de_codigos_unicos()

    Verification:
        - Result is a string
    """
    result = generador_de_codigos_unicos()
    assert isinstance(result, str)


def test_generador_de_codigos_unicos_length():
    """
    Test that ULID has correct length of 26 characters.

    Setup:
        - None

    Action:
        - Call generador_de_codigos_unicos()

    Verification:
        - Result length is 26
    """
    result = generador_de_codigos_unicos()
    assert len(result) == 26


def test_generador_de_codigos_unicos_unique():
    """
    Test that multiple calls produce unique codes.

    Setup:
        - None

    Action:
        - Generate 100 codes

    Verification:
        - All codes are unique
    """
    codes = [generador_de_codigos_unicos() for _ in range(100)]
    assert len(codes) == len(set(codes))


def test_generador_de_codigos_unicos_alphanumeric():
    """
    Test that ULID contains only alphanumeric characters.

    Setup:
        - None

    Action:
        - Call generador_de_codigos_unicos()

    Verification:
        - Result is alphanumeric
    """
    result = generador_de_codigos_unicos()
    assert result.isalnum()


def test_generador_codigo_empleado_returns_string():
    """
    Test that employee code generator returns a string.

    Setup:
        - None

    Action:
        - Call generador_codigo_empleado()

    Verification:
        - Result is a string
    """
    result = generador_codigo_empleado()
    assert isinstance(result, str)


def test_generador_codigo_empleado_has_prefix():
    """
    Test that employee code has EMP- prefix.

    Setup:
        - None

    Action:
        - Call generador_codigo_empleado()

    Verification:
        - Result starts with "EMP-"
    """
    result = generador_codigo_empleado()
    assert result.startswith("EMP-")


def test_generador_codigo_empleado_format():
    """
    Test that employee code has format EMP-XXXXXX.

    Setup:
        - None

    Action:
        - Call generador_codigo_empleado()

    Verification:
        - Format is EMP- followed by 6 characters
    """
    result = generador_codigo_empleado()
    parts = result.split("-")
    assert len(parts) == 2
    assert parts[0] == "EMP"
    assert len(parts[1]) == 6


def test_generador_codigo_empleado_uppercase():
    """
    Test that suffix is uppercase alphanumeric.

    Setup:
        - None

    Action:
        - Call generador_codigo_empleado()

    Verification:
        - Suffix is uppercase and alphanumeric
    """
    result = generador_codigo_empleado()
    suffix = result.split("-")[1]
    assert suffix.isupper()
    assert suffix.isalnum()


def test_generador_codigo_empleado_unique():
    """
    Test that multiple calls produce unique codes.

    Setup:
        - None

    Action:
        - Generate 100 employee codes

    Verification:
        - All codes are unique
    """
    codes = [generador_codigo_empleado() for _ in range(100)]
    assert len(codes) == len(set(codes))


def test_utc_now_returns_datetime():
    """
    Test that utc_now returns a datetime object.

    Setup:
        - None

    Action:
        - Call utc_now()

    Verification:
        - Result is a datetime
    """
    result = utc_now()
    assert isinstance(result, datetime)


def test_utc_now_has_timezone():
    """
    Test that utc_now returns timezone-aware datetime.

    Setup:
        - None

    Action:
        - Call utc_now()

    Verification:
        - Result has timezone info
        - Timezone is UTC
    """
    result = utc_now()
    assert result.tzinfo is not None
    assert result.tzinfo == timezone.utc


def test_utc_now_is_timezone_aware_utc():
    """
    Test that utc_now returns current time in UTC timezone.

    Setup:
        - None

    Action:
        - Call utc_now()

    Verification:
        - Result has UTC timezone
        - Result is a recent datetime (not ancient or future)
    """
    result = utc_now()

    # Should have UTC timezone
    assert result.tzinfo == timezone.utc

    # Should represent a recent time (year 2020 or later)
    # This is a sanity check that the function returns actual current time
    assert result.year >= 2020


def test_generador_codigo_empleado_no_collisions():
    """
    Test that employee codes don't collide in rapid generation.

    Setup:
        - None

    Action:
        - Generate many codes rapidly

    Verification:
        - All codes are unique
    """
    codes = [generador_codigo_empleado() for _ in range(1000)]
    assert len(codes) == len(set(codes))


def test_generador_de_codigos_unicos_alphanumeric_only():
    """
    Test that ULID codes contain only alphanumeric characters.

    Setup:
        - None

    Action:
        - Generate multiple codes

    Verification:
        - All codes are alphanumeric
    """
    codes = [generador_de_codigos_unicos() for _ in range(10)]
    for code in codes:
        assert code.isalnum()
        assert len(code) == 26
