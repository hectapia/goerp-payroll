# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Bracket tax calculation."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..ast.type_converter import to_decimal


class BracketCalculator:
    """Calculates tax for a specific bracket."""

    @staticmethod
    def calculate(bracket: dict[str, Any], input_value: Decimal) -> dict[str, Decimal]:
        """Calculate tax for a specific bracket.

        Args:
            bracket: Tax bracket definition
            input_value: Value being taxed

        Returns:
            Dictionary with calculated tax components
        """
        rate = to_decimal(bracket.get("rate", 0))
        fixed = to_decimal(bracket.get("fixed", 0))
        over = to_decimal(bracket.get("over", 0))

        # Calculate tax: fixed + (input_value - over) * rate
        excess = max(input_value - over, Decimal("0"))
        tax = fixed + (excess * rate)

        return {
            "tax": tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "rate": rate,
            "fixed": fixed,
            "over": over,
        }
