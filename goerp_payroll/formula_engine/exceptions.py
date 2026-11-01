# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Exceptions for formula engine."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from goerp_payroll.schema_validator import ValidationError as _BaseValidationError


class FormulaEngineError(Exception):
    """Base exception for formula engine errors.

    Python 3.11+ enhancement: Supports exception notes via add_note() method.
    """


# Alias for backward compatibility
TaxEngineError = FormulaEngineError


class ValidationError(_BaseValidationError, FormulaEngineError):
    """Exception for validation errors in schema or data.

    Inherits from both the base ValidationError (for schema_validator) and
    FormulaEngineError (for backward compatibility with existing error handling).

    Python 3.11+ enhancement: Can use add_note() to append contextual information.
    """


class CalculationError(FormulaEngineError):
    """Exception for calculation errors during execution.

    Python 3.11+ enhancement: Supports add_note() for additional context.
    """
