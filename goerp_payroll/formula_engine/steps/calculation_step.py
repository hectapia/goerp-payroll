# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Calculation step implementation."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from typing import TYPE_CHECKING, Any

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..ast.expression_evaluator import ExpressionEvaluator
from .base_step import Step

if TYPE_CHECKING:
    from ..execution.execution_context import ExecutionContext


class CalculationStep(Step):
    """Step for executing mathematical calculations."""

    def execute(self, context: "ExecutionContext") -> Any:  # Changed from Decimal to Any
        """Execute calculation step.

        Args:
            context: Execution context

        Returns:
            Calculated result (Decimal for numbers, date for dates, etc.)
        """
        formula = self.config.get("formula", "")
        evaluator = ExpressionEvaluator(
            variables=context.variables,
            trace_callback=context.trace_callback,
            strict_mode=context.strict_mode,
        )
        return evaluator.evaluate(formula)
