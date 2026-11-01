# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Security validation for AST nodes."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
import ast

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..ast.safe_operators import ALLOWED_AST_TYPES, SAFE_FUNCTIONS, validate_expression_complexity
from ..exceptions import CalculationError


class SecurityValidator:
    """Validates AST security for expression evaluation."""

    @staticmethod
    def validate_ast_security(node: ast.AST) -> None:
        """Validate that an AST node only contains safe operations.

        Args:
            node: AST node to validate

        Raises:
            CalculationError: If unsafe operations are detected
        """
        try:
            validate_expression_complexity(node)
        except ValueError as e:
            raise CalculationError(str(e)) from e

        # Validate all nodes in the tree in a single pass
        for child in ast.walk(node):
            if not isinstance(child, ALLOWED_AST_TYPES):
                raise CalculationError(
                    f"Unsafe operation detected: {child.__class__.__name__}. "
                    "Only basic arithmetic and safe functions are allowed."
                )
            # Validate function calls
            if isinstance(child, ast.Call):
                if not isinstance(child.func, ast.Name):
                    raise CalculationError("Only named functions are allowed")
                if child.func.id not in SAFE_FUNCTIONS:
                    raise CalculationError(
                        f"Function '{child.func.id}' is not allowed. "
                        f"Allowed functions: {', '.join(SAFE_FUNCTIONS.keys())}"
                    )
