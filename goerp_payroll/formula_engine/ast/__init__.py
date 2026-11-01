# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
# Copyright 2025 - 2026 BMO Soluciones, S.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""AST parsing and evaluation modules.

This package provides secure, enterprise-grade evaluation of mathematical
expressions for payroll formulas. It implements a whitelist-based security
model that prevents arbitrary code execution while maintaining financial precision.

Security Architecture:

1. **Whitelist-Based Validation**: Only explicitly approved AST node types
   and functions are allowed. Any attempt to use unapproved operations is
   rejected with a clear security violation message.

2. **No Dynamic Code Execution**: The system does NOT use eval(), exec(),
   compile(), or any dynamic method resolution (getattr). All code paths
   are explicit and auditable.

3. **DoS Prevention**: Expression length and AST depth are bounded to prevent
   denial-of-service attacks via extremely long or deeply nested expressions.

4. **Financial Precision**: All calculations use Python's Decimal type to
   maintain precision required for payroll calculations.

5. **Immutable Context**: Variable contexts are read-only during evaluation,
   preventing side effects and ensuring deterministic results.

Allowed Operations:
- Arithmetic: +, -, *, /, //, %, **
- Functions: min, max, abs, round
- Variables: Pre-defined in execution context
- Constants: Numeric literals only

Prohibited Operations:
- File I/O, network access, system calls
- Import statements, attribute access
- Lambda functions, list comprehensions
- Any Python builtin not explicitly whitelisted

Usage Example:
    ```python
    from goerp_payroll.formula_engine.ast import ExpressionEvaluator
    from decimal import Decimal

    variables = {
        'salario_base': Decimal('5000'),
        'bono': Decimal('1000')
    }

    evaluator = ExpressionEvaluator(variables)
    result = evaluator.evaluate('salario_base * 1.15 + bono')
    # result = Decimal('6750')
    ```

Security Notes:
- This module is designed for use with untrusted input (JSON rules)
- All security validations are fail-safe (reject by default)
- Adding new functions or operators requires security review
- Regular security audits are recommended
"""

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #


# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #


# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from .ast_visitor import ASTVisitor, SafeASTVisitor
from .expression_evaluator import ExpressionEvaluator
from .safe_operators import (
    SAFE_OPERATORS,
    COMPARISON_OPERATORS,
    SAFE_FUNCTIONS,
    ALLOWED_AST_TYPES,
    MAX_EXPRESSION_LENGTH,
    MAX_AST_DEPTH,
    MAX_FUNCTION_ARGS,
    validate_safe_function_call,
)
from .type_converter import (
    to_decimal,
    safe_divide,
    MAX_DECIMAL_DIGITS,
    MAX_DECIMAL_VALUE,
    MIN_DECIMAL_VALUE,
)

# <==================[ Expose all varaibles and constants ]===================>
__all__ = [
    "ASTVisitor",
    "SafeASTVisitor",
    "ExpressionEvaluator",
    "SAFE_OPERATORS",
    "COMPARISON_OPERATORS",
    "SAFE_FUNCTIONS",
    "ALLOWED_AST_TYPES",
    "MAX_EXPRESSION_LENGTH",
    "MAX_AST_DEPTH",
    "MAX_FUNCTION_ARGS",
    "validate_safe_function_call",
    "to_decimal",
    "safe_divide",
    "MAX_DECIMAL_DIGITS",
    "MAX_DECIMAL_VALUE",
    "MIN_DECIMAL_VALUE",
]
