# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tax table and bracket calculation modules."""

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from .tax_table import TaxTable
from .bracket_calculator import BracketCalculator
from .table_lookup import TableLookup

# <==================[ Expose all varaibles and constants ]===================>
__all__ = [
    "TaxTable",
    "BracketCalculator",
    "TableLookup",
]
