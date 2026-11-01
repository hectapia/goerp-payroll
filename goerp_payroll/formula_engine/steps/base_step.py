# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Base step interface for Strategy pattern."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from typing import Any, TYPE_CHECKING

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #

if TYPE_CHECKING:
    from ..execution.execution_context import ExecutionContext


class Step(ABC):
    """Base interface for all step types."""

    def __init__(self, name: str, config: dict[str, Any]):
        """Initialize step.

        Args:
            name: Step name
            config: Step configuration dictionary
        """
        self.name = name
        self.config = config

    @abstractmethod
    def execute(self, context: "ExecutionContext") -> Any:
        """Execute the step and return result.

        Args:
            context: Execution context with variables and tax tables

        Returns:
            Step execution result
        """

    def get_variable_value(self, result: Any) -> Any:  # Changed from Decimal to Any
        """Return the value to store for this step.

        For numeric results, ensures it's a Decimal.
        For date/string results, returns as-is.
        """
        from ..ast.type_converter import to_decimal

        # If it's already a Decimal, return it
        if isinstance(result, Decimal):
            return result

        # If it's a date or string (from date functions), return as-is
        if isinstance(result, (str, date)):
            return result

        # For other numeric types, try to convert to Decimal
        try:
            return to_decimal(result)
        except Exception:
            # If conversion fails, it might be a valid non-numeric type
            return result
