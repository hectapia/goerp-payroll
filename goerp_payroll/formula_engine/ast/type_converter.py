# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Type conversion utilities for formula engine.

This module provides safe type conversion functions that maintain financial
precision and prevent common security issues:

1. Decimal Precision: All numeric values are converted to Decimal to avoid
   floating-point precision errors in financial calculations.

2. Input Validation: Values are validated to prevent:
   - Infinity and NaN values
   - Extremely large numbers that could cause DoS
   - Invalid type conversions

3. Safe Division: Division by zero is handled gracefully by returning 0
   instead of raising an exception.

Security Considerations:
- All conversions are deterministic and side-effect free
- No dynamic type inspection or attribute access
- Bounded numeric ranges prevent resource exhaustion
- Explicit error messages aid in debugging and auditing
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
import math
from decimal import Decimal, InvalidOperation
from typing import Any

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..exceptions import ValidationError

# <-------------------- Constantes Locales --------------------> #
MAX_DECIMAL_DIGITS = 28
MAX_DECIMAL_VALUE = Decimal("9" * MAX_DECIMAL_DIGITS)
MIN_DECIMAL_VALUE = -MAX_DECIMAL_VALUE


def to_decimal(value: Any) -> Decimal:
    """Safely convert a value to Decimal with validation.

    This function converts various Python types to Decimal while enforcing
    security constraints:
    - Rejects infinity and NaN values
    - Validates numeric ranges to prevent DoS
    - Maintains financial precision
    - Provides clear error messages

    Args:
        value: Value to convert. Supported types:
              - None: converts to 0
              - Decimal: returned as-is (after validation)
              - bool: True -> 1, False -> 0
              - int, float, str: converted to Decimal

    Returns:
        Decimal representation of the value

    Raises:
        ValidationError: If value cannot be safely converted to Decimal

    Examples:
        >>> to_decimal(42)
        Decimal('42')
        >>> to_decimal('123.45')
        Decimal('123.45')
        >>> to_decimal(True)
        Decimal('1')
        >>> to_decimal(None)
        Decimal('0')
    """
    if value is None:
        return Decimal("0")

    if isinstance(value, Decimal):
        _validate_decimal_range(value)
        return value

    if isinstance(value, bool):
        return Decimal("1") if value else Decimal("0")

    if isinstance(value, float):
        if math.isnan(value):
            raise ValidationError(
                "Cannot convert NaN (Not a Number) to Decimal. "
                "This may indicate a calculation error in the input data."
            )
        if math.isinf(value):
            raise ValidationError(
                "Cannot convert infinity to Decimal. Check for division by zero or overflow in input calculations."
            )

    try:
        result = Decimal(str(value))
        _validate_decimal_range(result)
        return result
    except (InvalidOperation, ValueError) as e:
        raise ValidationError(
            f"Cannot convert value '{value}' (type: {type(value).__name__}) to Decimal: {e}. "
            "Ensure the value is a valid number."
        ) from e
    except Exception as e:
        raise ValidationError(f"Unexpected error converting '{value}' to Decimal: {e}") from e


def _validate_decimal_range(value: Decimal) -> None:
    """Validate that a Decimal value is within acceptable range.

    This prevents denial-of-service attacks via extremely large numbers
    that could consume excessive memory or CPU during calculations.

    Args:
        value: Decimal value to validate

    Raises:
        ValidationError: If value is outside acceptable range
    """
    if value.is_nan():
        raise ValidationError("Decimal value is NaN (Not a Number). This indicates an invalid calculation result.")

    if value.is_infinite():
        raise ValidationError("Decimal value is infinite. This indicates an overflow or division by zero.")

    if value > MAX_DECIMAL_VALUE or value < MIN_DECIMAL_VALUE:
        raise ValidationError(
            f"Decimal value {value} is outside acceptable range "
            f"[{MIN_DECIMAL_VALUE}, {MAX_DECIMAL_VALUE}]. "
            f"This limit ({MAX_DECIMAL_DIGITS} digits) prevents resource exhaustion attacks."
        )


def safe_divide(numerator: Decimal, denominator: Decimal) -> Decimal:
    """Safely divide two decimals, handling division by zero.

    This function provides safe division for payroll calculations where
    division by zero should return 0 rather than raising an exception.
    This is common in formulas like: bonus = sales / days_worked
    where days_worked might be 0 for new employees.

    Args:
        numerator: The dividend (value to be divided)
        denominator: The divisor (value to divide by)

    Returns:
        Result of division, or Decimal('0') if denominator is 0

    Examples:
        >>> safe_divide(Decimal('100'), Decimal('5'))
        Decimal('20')
        >>> safe_divide(Decimal('100'), Decimal('0'))
        Decimal('0')
    """
    if denominator == 0:
        return Decimal("0")

    try:
        result = numerator / denominator
        _validate_decimal_range(result)
        return result
    except (InvalidOperation, ValueError) as e:
        raise ValidationError(f"Error in division {numerator} / {denominator}: {e}") from e
