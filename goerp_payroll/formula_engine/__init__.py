# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Formula engine package.

This package contains the refactored formula engine with modular architecture:
- AST parsing and evaluation using Visitor pattern
- Step execution using Strategy pattern
- Validation, tables, execution, and results modules
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
# Import from formula_engine_examples
# EXAMPLE_PROGRESSIVE_TAX_SCHEMA is the new generic name
# EXAMPLE_IR_NICARAGUA_SCHEMA is kept for backward compatibility (deprecated)
from goerp_payroll.formula_engine_examples import (
    EXAMPLE_PROGRESSIVE_TAX_SCHEMA,
    EXAMPLE_IR_NICARAGUA_SCHEMA,
)

# Import main engine and functions
from .engine import FormulaEngine, calculate_with_rule, get_available_sources_for_ui

# Import exceptions
from .exceptions import CalculationError, FormulaEngineError, TaxEngineError, ValidationError

# Import utilities for backward compatibility
from .ast.type_converter import safe_divide, to_decimal

# Import submodules
from .ast import (
    ALLOWED_AST_TYPES,
    ASTVisitor,
    COMPARISON_OPERATORS,
    ExpressionEvaluator,
    SAFE_FUNCTIONS,
    SAFE_OPERATORS,
    SafeASTVisitor,
)
from .data_sources import AVAILABLE_DATA_SOURCES
from .novelty_codes import NOVELTY_CODES

# <==================[ Expose all varaibles and constants ]===================>
__all__ = [
    # Main engine
    "FormulaEngine",
    "calculate_with_rule",
    "get_available_sources_for_ui",
    # Exceptions
    "FormulaEngineError",
    "TaxEngineError",
    "ValidationError",
    "CalculationError",
    # Examples
    "EXAMPLE_PROGRESSIVE_TAX_SCHEMA",
    "EXAMPLE_IR_NICARAGUA_SCHEMA",  # Deprecated alias for backward compatibility
    # Utilities
    "to_decimal",
    "safe_divide",
    # AST modules
    "ASTVisitor",
    "SafeASTVisitor",
    "ExpressionEvaluator",
    "SAFE_OPERATORS",
    "COMPARISON_OPERATORS",
    "SAFE_FUNCTIONS",
    "ALLOWED_AST_TYPES",
    # Data sources
    "AVAILABLE_DATA_SOURCES",
    "NOVELTY_CODES",
]
