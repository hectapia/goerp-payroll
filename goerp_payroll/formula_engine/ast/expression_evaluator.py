# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Expression evaluator using AST visitor pattern.

This module provides secure evaluation of mathematical expressions from JSON rules.
It implements multiple layers of security:

1. Expression Length Validation: Prevents DoS attacks via extremely long expressions
2. AST Depth Validation: Prevents stack overflow from deeply nested expressions
3. Whitelist-based AST Validation: Only approved node types are allowed
4. Safe Visitor Pattern: No dynamic code execution or attribute access
5. Decimal Precision: All calculations maintain financial precision

Security Model:
- Input expressions are parsed into Abstract Syntax Trees (AST)
- AST is validated against a whitelist of allowed node types
- AST depth is checked to prevent stack overflow
- Evaluation uses explicit visitor pattern (no eval/exec/compile)
- All operations are deterministic and side-effect free

Example Safe Expression:
    'salario_base * 1.15 + max(bono, 1000)'

Example Unsafe Expression (rejected):
    '__import__("os").system("rm -rf /")'
    'open("/etc/passwd").read()'
    '[x for x in range(1000000)]'
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
import ast
from decimal import Decimal
from typing import Any, Callable

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from goerp_payroll.i18n import _
from goerp_payroll.log import TRACE_LEVEL_NUM, is_trace_enabled, log
from ..exceptions import CalculationError, ValidationError
from .ast_visitor import SafeASTVisitor
from .safe_operators import ALLOWED_AST_TYPES, validate_expression_complexity
from .type_converter import to_decimal


class ExpressionEvaluator:
    """Evaluates mathematical expressions safely using AST.

    This class provides enterprise-grade secure expression evaluation for
    payroll formulas. It prevents code injection, DoS attacks, and ensures
    all calculations are deterministic and auditable.

    Security Features:
    - Expression length limits (prevents DoS)
    - AST depth limits (prevents stack overflow)
    - Whitelist-based validation (prevents code injection)
    - No dynamic code execution (no eval/exec/compile)
    - Immutable variable context (prevents side effects)
    - Comprehensive error messages for debugging

    Thread Safety:
    This class is thread-safe as long as the variables dictionary is not
    modified during evaluation. Each evaluation creates a new visitor instance.
    """

    def __init__(
        self,
        variables: dict[str, Decimal],
        trace_callback: Callable[[str], None] | None = None,
        strict_mode: bool = False,
    ):
        """Initialize expression evaluator.

        Args:
            variables: Dictionary of variable names to Decimal values.
                      This dictionary is not modified during evaluation.
            trace_callback: Optional callback for trace logging.
                          Should be thread-safe if used in concurrent contexts.
        """
        self.variables = variables
        self.trace_callback = trace_callback or self._default_trace
        self.strict_mode = strict_mode

    def _default_trace(self, message: str) -> None:
        """Default trace callback."""
        if is_trace_enabled():
            try:
                log.log(TRACE_LEVEL_NUM, message)
            except Exception:
                pass

    def evaluate(self, expression: str) -> Any:  # Changed from Decimal to Any
        """Safely evaluate a mathematical expression using AST.

        This method implements multiple layers of security validation:
        1. Input validation (type, length)
        2. Syntax validation (AST parsing)
        3. Security validation (whitelist checking)
        4. Depth validation (stack overflow prevention)
        5. Safe evaluation (visitor pattern)

        Args:
            expression: Mathematical expression string (e.g., 'a + b * 2')

        Returns:
            Result of the expression (Decimal for numbers, date for dates, etc.)

        Raises:
            CalculationError: If expression is invalid, unsafe, or evaluation fails

        Examples:
            >>> evaluator = ExpressionEvaluator({'x': Decimal('10'), 'y': Decimal('5')})
            >>> evaluator.evaluate('x + y')
            Decimal('15')
            >>> evaluator.evaluate('max(x, y) * 2')
            Decimal('20')
        """
        if not expression or not isinstance(expression, str):
            return Decimal("0")

        expression = expression.strip()
        if not expression:
            return Decimal("0")

        self.trace_callback(_("Evaluando expresión: '%(expr)s'") % {"expr": expression})

        try:
            tree = ast.parse(expression, mode="eval")

            self._validate_ast_security(tree.body)
            try:
                validate_expression_complexity(tree, expression)
            except ValueError as e:
                raise CalculationError(str(e)) from e

            visitor = SafeASTVisitor(self.variables, strict_mode=self.strict_mode)
            result = visitor.visit(tree.body)

            # Try to convert to Decimal only if it's a numeric result
            # Date functions and other special types return as-is
            try:
                if isinstance(result, (int, float, str)):
                    # If it looks like a number, convert to Decimal
                    final_result = to_decimal(result)
                else:
                    # Otherwise keep the original type (date, etc.)
                    final_result = result
            except (ValidationError, ValueError):
                # If conversion fails, keep original result
                final_result = result

            self.trace_callback(
                _("Resultado expresión '%(expr)s' => %(res)s") % {"expr": expression, "res": final_result}
            )
            return final_result
        except SyntaxError as e:
            raise CalculationError(
                f"Invalid expression syntax in '{expression}': {e}. "
                "Check for unmatched parentheses, invalid operators, or typos."
            ) from e
        except ZeroDivisionError as e:
            if self.strict_mode:
                raise CalculationError("Division by zero detected while evaluating expression.") from e
            return Decimal("0")
        except CalculationError as e:
            raise CalculationError(f"Error evaluating expression '{expression}': {e}") from e
        except Exception as e:
            raise CalculationError(f"Unexpected error evaluating expression '{expression}': {e}") from e

    def _validate_ast_security(self, node: ast.AST) -> None:
        """Validate that an AST node only contains safe operations.

        This method implements a whitelist-based security model. It walks the
        entire AST and verifies that every node is in the allowed list. This
        prevents code injection attacks like:
        - Import statements: __import__('os').system('rm -rf /')
        - Attribute access: obj.__class__.__bases__[0].__subclasses__()
        - List comprehensions: [x for x in range(999999999)]
        - Lambda functions: (lambda: exec('malicious code'))()

        Args:
            node: AST node to validate (typically the root of the expression tree)

        Raises:
            CalculationError: If any unsafe operation is detected
        """
        for child in ast.walk(node):
            if not isinstance(child, ALLOWED_AST_TYPES):
                raise CalculationError(
                    f"Security violation: AST node type '{child.__class__.__name__}' is not allowed. "
                    "Only basic arithmetic operations and whitelisted functions are permitted. "
                    "This restriction prevents code injection and arbitrary code execution."
                )

            if isinstance(child, ast.Call):
                if not isinstance(child.func, ast.Name):
                    raise CalculationError(
                        "Security violation: Only direct named function calls are allowed. "
                        "Attribute access (e.g., obj.method()) and lambda functions are prohibited."
                    )
                from .safe_operators import SAFE_FUNCTIONS

                if child.func.id not in SAFE_FUNCTIONS:
                    raise CalculationError(
                        f"Security violation: Function '{child.func.id}' is not in the whitelist. "
                        f"Allowed functions: {', '.join(sorted(SAFE_FUNCTIONS.keys()))}. "
                        "This restriction prevents execution of arbitrary Python functions."
                    )
