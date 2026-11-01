# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tax lookup step implementation."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from decimal import Decimal
from typing import TYPE_CHECKING

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..exceptions import CalculationError
from ..tables.table_lookup import TableLookup
from .base_step import Step

if TYPE_CHECKING:
    from ..execution.execution_context import ExecutionContext


class TaxLookupStep(Step):
    """Step for looking up values in tax tables."""

    def execute(self, context: "ExecutionContext") -> dict[str, Decimal]:
        """Execute tax lookup step.

        Args:
            context: Execution context

        Returns:
            Dictionary with tax calculation results
        """
        table_name = self.config.get("table", "")
        input_var = self.config.get("input", "")
        if input_var in context.variables:
            input_value = context.variables[input_var]
        else:
            if context.strict_mode:
                raise CalculationError(
                    f"Missing required input variable '{input_var}' for tax lookup in table '{table_name}'"
                )
            input_value = Decimal("0")

        table_lookup = TableLookup(context.tax_tables, context.trace_callback, strict_mode=context.strict_mode)
        return table_lookup.lookup(table_name, input_value)

    def get_variable_value(self, result: dict[str, Decimal]) -> Decimal:
        """Return the Decimal tax value for variable storage."""
        if not isinstance(result, dict):
            raise CalculationError(f"Tax lookup step '{self.name}' must return dict, got {type(result).__name__}")
        tax_value = result.get("tax")
        if not isinstance(tax_value, Decimal):
            raise CalculationError(
                f"Tax lookup step '{self.name}' must include Decimal 'tax', got {type(tax_value).__name__}"
            )
        return tax_value
