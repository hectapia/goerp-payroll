# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tax table data structure."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from typing import Any

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #


class TaxTable:
    """Represents a tax table with brackets."""

    def __init__(self, name: str, brackets: list[dict[str, Any]]):
        """Initialize tax table.

        Args:
            name: Table name
            brackets: List of bracket dictionaries
        """
        self.name = name
        self.brackets = brackets
