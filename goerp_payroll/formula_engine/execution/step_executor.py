# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Step executor for formula engine."""

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
from goerp_payroll.i18n import _
from ..exceptions import CalculationError
from .execution_context import ExecutionContext

if TYPE_CHECKING:
    from ..steps.base_step import Step


class StepExecutor:
    """Executes steps in sequence."""

    def execute(self, step: "Step", context: ExecutionContext) -> Any:
        """Execute a step and update context.

        Args:
            step: Step to execute
            context: Execution context

        Returns:
            Step execution result
        """
        if context.trace_callback:
            context.trace_callback(
                _("Ejecutando paso '%(name)s' tipo=%(type)s variables_disponibles=%(vars)s")
                % {
                    "name": step.name,
                    "type": step.config.get("type"),
                    "vars": list(context.variables.keys()),
                }
            )

        try:
            result = step.execute(context)
            return result
        except Exception as e:
            step_name = step.name
            step_type = step.config.get("type", "unknown")
            error = CalculationError(f"Error in step '{step_name}': {e}")
            if hasattr(error, "add_note"):
                error.add_note(f"Step type: {step_type}")
                error.add_note(f"Available variables: {list(context.variables.keys())}")
            raise error from e
