# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Validator for payroll period."""

from __future__ import annotations


from ..domain.payroll_context import PayrollContext
from ..results.validation_result import ValidationResult
from ..validators.base_validator import BaseValidator


class PeriodValidator(BaseValidator):
    """Validates payroll period."""

    def validate(self, context: PayrollContext) -> ValidationResult:
        """Validate period."""
        result = ValidationResult()

        if context.periodo_inicio > context.periodo_fin:
            result.add_error(
                f"Período inválido: inicio ({context.periodo_inicio}) posterior a fin ({context.periodo_fin})"
            )

        dias_periodo = (context.periodo_fin - context.periodo_inicio).days + 1
        if dias_periodo <= 0:
            result.add_error("El período debe tener al menos un día.")
        elif dias_periodo > 366:
            result.add_error(
                f"Período excesivamente largo: {dias_periodo} días. Los períodos no deben exceder 366 días."
            )

        return result
