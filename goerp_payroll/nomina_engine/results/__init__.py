# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Result DTOs for payroll processing."""

from .validation_result import ValidationResult
from .error_result import ErrorResult
from .payroll_result import PayrollResult

__all__ = [
    "ValidationResult",
    "ErrorResult",
    "PayrollResult",
]
