# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Variable store for formula execution."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from decimal import Decimal
from typing import Any

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #


class VariableStore:
    """Manages variables during formula execution."""

    def __init__(self):
        """Initialize variable store."""
        self.variables: dict[str, Any] = {}  # Changed from Decimal to Any to support dates
        self.results: dict[str, Any] = {}

    def set(self, name: str, value: Any, result: Any | None = None) -> None:
        """Set a variable value.

        Args:
            name: Variable name
            value: Variable value (can be Decimal, date, string, etc.)
            result: Optional raw result for audit purposes
        """
        # Removed the Decimal type check to allow dates and other types
        self.variables[name] = value
        self.results[name] = result if result is not None else value

    def get(self, name: str, default: Any = Decimal("0")) -> Any:
        """Get a variable value.

        Args:
            name: Variable name
            default: Default value if not found

        Returns:
            Variable value
        """
        return self.variables.get(name, default)

    def clear(self) -> None:
        """Clear all variables and results."""
        self.variables.clear()
        self.results.clear()
