# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Assignment step implementation."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from decimal import Decimal
from typing import TYPE_CHECKING, Any

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..ast.type_converter import to_decimal
from .base_step import Step

if TYPE_CHECKING:
    from ..execution.execution_context import ExecutionContext


class AssignmentStep(Step):
    """Step for assigning values to variables."""

    def execute(self, context: "ExecutionContext") -> Decimal:
        """Execute assignment step.

        Args:
            context: Execution context

        Returns:
            Assigned value as Decimal
        """
        value = self.config.get("value")
        result = self._resolve_value(value, context)
        return result

    def _resolve_value(self, value: Any, context: "ExecutionContext") -> Decimal:
        """Resolve a value that might be a variable reference.

        Args:
            value: Value or variable name to resolve
            context: Execution context

        Returns:
            Decimal value
        """
        if isinstance(value, str) and value in context.variables:
            resolved = context.variables[value]
            if context.trace_callback:
                from goerp_payroll.i18n import _

                context.trace_callback(
                    _("Resolviendo variable '%(name)s' => %(value)s") % {"name": value, "value": resolved}
                )
            return resolved

        resolved_literal = to_decimal(value)
        if context.trace_callback:
            from goerp_payroll.i18n import _

            context.trace_callback(
                _("Resolviendo valor literal '%(raw)s' => %(value)s") % {"raw": value, "value": resolved_literal}
            )
        return resolved_literal
