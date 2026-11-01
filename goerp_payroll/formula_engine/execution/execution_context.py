# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Execution context for formula engine."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from dataclasses import dataclass, field
from typing import Any, Callable, cast

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..ast.safe_operators import SAFE_FUNCTIONS, SAFE_OPERATORS


@dataclass
class ExecutionContext:
    """Context for formula execution."""

    variables: dict[str, Any]  # Changed from dict[str, Decimal] to support dates and other types
    tax_tables: dict[str, Any]
    strict_mode: bool = False
    trace_callback: Callable[[str], None] | None = None
    safe_operators: dict[type, Any] = field(default_factory=lambda: cast(dict[type, Any], SAFE_OPERATORS))
    safe_functions: dict[str, Any] = field(default_factory=lambda: SAFE_FUNCTIONS)

    def with_variable(self, name: str, value: Any) -> "ExecutionContext":  # Changed from Decimal to Any
        """Create a new context with an additional variable.

        Args:
            name: Variable name
            value: Variable value

        Returns:
            New context with updated variables
        """
        new_vars = {**self.variables, name: value}
        return ExecutionContext(
            variables=new_vars,
            tax_tables=self.tax_tables,
            strict_mode=self.strict_mode,
            trace_callback=self.trace_callback,
            safe_operators=self.safe_operators,
            safe_functions=self.safe_functions,
        )
