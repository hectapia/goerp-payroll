# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Unit tests for ast_visitor.py - AST visitor exception handling.

This test module focuses on exception handling paths in the SafeASTVisitor class
to increase code coverage by testing error scenarios.
"""

import ast
from decimal import Decimal

import pytest

from goerp_payroll.formula_engine.ast.ast_visitor import SafeASTVisitor
from goerp_payroll.formula_engine.exceptions import CalculationError


class TestSafeASTVisitorExceptionHandling:
    """Tests for exception handling in SafeASTVisitor."""

    def test_visit_unsupported_node_type(self):
        """Test that unsupported AST node types raise CalculationError."""
        visitor = SafeASTVisitor({})

        # Create an unsupported node type (ListComp is not allowed)
        unsupported_node = ast.ListComp(elt=ast.Constant(value=1), generators=[])

        with pytest.raises(CalculationError, match="Unsupported AST node type: ListComp"):
            visitor.visit(unsupported_node)

    def test_visit_import_node_rejected(self):
        """Test that Import nodes are rejected."""
        visitor = SafeASTVisitor({})

        # Create an Import node (dangerous - should be rejected)
        import_node = ast.Import(names=[ast.alias(name="os", asname=None)])

        with pytest.raises(CalculationError, match="Unsupported AST node type"):
            visitor.visit(import_node)

    def test_visit_attribute_node_rejected(self):
        """Test that Attribute access nodes are rejected."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        # Create an Attribute node (dangerous - should be rejected)
        attr_node = ast.Attribute(value=ast.Name(id="x", ctx=ast.Load()), attr="__class__", ctx=ast.Load())

        with pytest.raises(CalculationError, match="Unsupported AST node type"):
            visitor.visit(attr_node)

    def test_visit_constant_invalid_type(self):
        """Test that non-numeric constants raise ValidationError (from type_converter)."""
        visitor = SafeASTVisitor({})

        # Create a constant with invalid type (list)
        invalid_constant = ast.Constant(value=[1, 2, 3])

        # The exception is raised by to_decimal in type_converter, which raises ValidationError
        from goerp_payroll.formula_engine.exceptions import ValidationError

        with pytest.raises(ValidationError, match="Cannot convert"):
            visitor.visit_constant(invalid_constant)

    def test_visit_name_undefined_variable(self):
        """Test that undefined variables raise CalculationError with helpful message."""
        visitor = SafeASTVisitor({"a": Decimal("10"), "b": Decimal("20")})

        # Try to access undefined variable
        name_node = ast.Name(id="undefined_var", ctx=ast.Load())

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_name(name_node)

        error_msg = str(exc_info.value)
        assert "Undefined variable: 'undefined_var'" in error_msg
        assert "Available variables:" in error_msg
        assert "a" in error_msg
        assert "b" in error_msg

    def test_visit_binop_unsupported_operator(self):
        """Test that unsupported binary operators raise CalculationError."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        # Create a BinOp node with unsupported operator (BitAnd is not allowed)
        binop_node = ast.BinOp(left=ast.Constant(value=5), op=ast.BitAnd(), right=ast.Constant(value=3))

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_binop(binop_node)

        error_msg = str(exc_info.value)
        assert "BitAnd" in error_msg or "not allowed" in error_msg
        assert "Allowed operators:" in error_msg

    def test_visit_binop_arithmetic_overflow(self):
        """Test that arithmetic overflow raises CalculationError."""
        visitor = SafeASTVisitor({})

        # Create a power operation that will cause OverflowError before it gets to to_decimal
        # This is tricky because Decimal can handle very large numbers
        # Let's use a different approach - create invalid operands
        binop_node = ast.BinOp(
            left=ast.Constant(value=2), op=ast.Pow(), right=ast.Constant(value=10000)  # This should overflow
        )

        # This should raise CalculationError from the exception handler
        with pytest.raises(CalculationError):
            visitor.visit_binop(binop_node)

    def test_visit_binop_division_by_zero_returns_zero(self):
        """Test that division by zero returns 0 safely in non-strict mode."""
        visitor = SafeASTVisitor({}, strict_mode=False)

        # Division by zero
        binop_node = ast.BinOp(left=ast.Constant(value=100), op=ast.Div(), right=ast.Constant(value=0))

        result = visitor.visit_binop(binop_node)
        assert result == Decimal("0")

    def test_visit_binop_floor_division_by_zero_returns_zero(self):
        """Test that floor division by zero returns 0 safely in non-strict mode."""
        visitor = SafeASTVisitor({}, strict_mode=False)

        # Floor division by zero
        binop_node = ast.BinOp(left=ast.Constant(value=100), op=ast.FloorDiv(), right=ast.Constant(value=0))

        result = visitor.visit_binop(binop_node)
        assert result == Decimal("0")

    def test_visit_binop_modulo_by_zero_returns_zero(self):
        """Test that modulo by zero returns 0 safely in non-strict mode."""
        visitor = SafeASTVisitor({}, strict_mode=False)

        # Modulo by zero
        binop_node = ast.BinOp(left=ast.Constant(value=100), op=ast.Mod(), right=ast.Constant(value=0))

        result = visitor.visit_binop(binop_node)
        assert result == Decimal("0")

    def test_visit_binop_division_by_zero_raises_in_strict_mode(self):
        """Test that division by zero raises CalculationError in strict mode."""
        visitor = SafeASTVisitor({}, strict_mode=True)

        # Division by zero
        binop_node = ast.BinOp(left=ast.Constant(value=100), op=ast.Div(), right=ast.Constant(value=0))

        with pytest.raises(CalculationError, match="Division by zero detected"):
            visitor.visit_binop(binop_node)

    def test_visit_binop_floor_division_by_zero_raises_in_strict_mode(self):
        """Test that floor division by zero raises CalculationError in strict mode."""
        visitor = SafeASTVisitor({}, strict_mode=True)

        # Floor division by zero
        binop_node = ast.BinOp(left=ast.Constant(value=100), op=ast.FloorDiv(), right=ast.Constant(value=0))

        with pytest.raises(CalculationError, match="Division by zero detected"):
            visitor.visit_binop(binop_node)

    def test_visit_binop_modulo_by_zero_raises_in_strict_mode(self):
        """Test that modulo by zero raises CalculationError in strict mode."""
        visitor = SafeASTVisitor({}, strict_mode=True)

        # Modulo by zero
        binop_node = ast.BinOp(left=ast.Constant(value=100), op=ast.Mod(), right=ast.Constant(value=0))

        with pytest.raises(CalculationError, match="Division by zero detected"):
            visitor.visit_binop(binop_node)

    def test_visit_unaryop_unsupported_operator(self):
        """Test that unsupported unary operators raise CalculationError."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        # Create a UnaryOp node with unsupported operator (Not is not allowed)
        unaryop_node = ast.UnaryOp(op=ast.Not(), operand=ast.Name(id="x", ctx=ast.Load()))

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_unaryop(unaryop_node)

        error_msg = str(exc_info.value)
        assert "Not" in error_msg or "not allowed" in error_msg
        assert "Only unary + and -" in error_msg

    def test_visit_unaryop_invert_not_allowed(self):
        """Test that bitwise invert operator is not allowed."""
        visitor = SafeASTVisitor({})

        # Create a UnaryOp node with Invert operator
        unaryop_node = ast.UnaryOp(op=ast.Invert(), operand=ast.Constant(value=5))

        with pytest.raises(CalculationError, match="not allowed"):
            visitor.visit_unaryop(unaryop_node)

    def test_visit_call_non_name_function(self):
        """Test that non-Name function calls raise CalculationError."""
        visitor = SafeASTVisitor({})

        # Create a Call node with attribute access (dangerous)
        call_node = ast.Call(
            func=ast.Attribute(value=ast.Name(id="obj", ctx=ast.Load()), attr="method", ctx=ast.Load()),
            args=[],
            keywords=[],
        )

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_call(call_node)

        error_msg = str(exc_info.value)
        assert "Only direct named function calls are allowed" in error_msg
        assert "Attribute access" in error_msg

    def test_visit_call_lambda_not_allowed(self):
        """Test that lambda functions are not allowed."""
        visitor = SafeASTVisitor({})

        # Create a Call node with Lambda function (dangerous)
        call_node = ast.Call(
            func=ast.Lambda(
                args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                body=ast.Constant(value=1),
            ),
            args=[],
            keywords=[],
        )

        with pytest.raises(CalculationError, match="Only direct named function calls"):
            visitor.visit_call(call_node)

    def test_visit_call_non_whitelisted_function(self):
        """Test that non-whitelisted functions raise CalculationError."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        # Create a Call node with non-whitelisted function
        call_node = ast.Call(func=ast.Name(id="eval", ctx=ast.Load()), args=[ast.Constant(value="1+1")], keywords=[])

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_call(call_node)

        error_msg = str(exc_info.value)
        assert "eval" in error_msg
        assert "not in the whitelist" in error_msg
        assert "Allowed functions:" in error_msg

    def test_visit_call_with_keyword_arguments(self):
        """Test that keyword arguments raise CalculationError."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        # Create a Call node with keyword arguments (not allowed)
        call_node = ast.Call(
            func=ast.Name(id="max", ctx=ast.Load()),
            args=[ast.Name(id="x", ctx=ast.Load())],
            keywords=[ast.keyword(arg="default", value=ast.Constant(value=0))],
        )

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_call(call_node)

        error_msg = str(exc_info.value)
        assert "Keyword arguments are not allowed" in error_msg
        assert "max" in error_msg

    def test_visit_call_invalid_number_of_arguments(self):
        """Test that invalid number of arguments raises CalculationError."""
        visitor = SafeASTVisitor({})

        # Create a Call node for max() with no arguments (invalid)
        call_node = ast.Call(func=ast.Name(id="max", ctx=ast.Load()), args=[], keywords=[])

        with pytest.raises(CalculationError, match="Invalid arguments"):
            visitor.visit_call(call_node)

    def test_visit_call_round_precision_too_low(self):
        """Test that round() with negative precision raises CalculationError."""
        visitor = SafeASTVisitor({"x": Decimal("123.456")})

        # Create a Call node for round() with negative precision
        call_node = ast.Call(
            func=ast.Name(id="round", ctx=ast.Load()),
            args=[ast.Name(id="x", ctx=ast.Load()), ast.Constant(value=-1)],
            keywords=[],
        )

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_call(call_node)

        error_msg = str(exc_info.value)
        assert "precision must be between 0 and 10" in error_msg

    def test_visit_call_round_precision_too_high(self):
        """Test that round() with precision > 10 raises CalculationError."""
        visitor = SafeASTVisitor({"x": Decimal("123.456")})

        # Create a Call node for round() with precision > 10
        call_node = ast.Call(
            func=ast.Name(id="round", ctx=ast.Load()),
            args=[ast.Name(id="x", ctx=ast.Load()), ast.Constant(value=15)],
            keywords=[],
        )

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_call(call_node)

        error_msg = str(exc_info.value)
        assert "precision must be between 0 and 10" in error_msg

    def test_visit_call_round_precision_non_integer(self):
        """Test that round() with non-integer precision raises CalculationError."""
        visitor = SafeASTVisitor({"x": Decimal("123.456")})

        # Create a Call node for round() with non-integer precision (2.9)
        call_node = ast.Call(
            func=ast.Name(id="round", ctx=ast.Load()),
            args=[ast.Name(id="x", ctx=ast.Load()), ast.Constant(value=2.9)],
            keywords=[],
        )

        with pytest.raises(CalculationError) as exc_info:
            visitor.visit_call(call_node)

        error_msg = str(exc_info.value)
        assert "precision must be an integer" in error_msg
        assert "2.9" in error_msg

    def test_visit_call_invalid_value_error(self):
        """Test that ValueError in function call raises CalculationError."""
        visitor = SafeASTVisitor({})

        # Create a Call node that will cause ValueError (abs with multiple args)
        call_node = ast.Call(
            func=ast.Name(id="abs", ctx=ast.Load()), args=[ast.Constant(value=10), ast.Constant(value=20)], keywords=[]
        )

        with pytest.raises(CalculationError):
            visitor.visit_call(call_node)

    def test_visit_with_nested_undefined_variable(self):
        """Test nested operations with undefined variable."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        # Create a nested operation: x + undefined_var
        binop_node = ast.BinOp(
            left=ast.Name(id="x", ctx=ast.Load()), op=ast.Add(), right=ast.Name(id="undefined_var", ctx=ast.Load())
        )

        with pytest.raises(CalculationError, match="Undefined variable"):
            visitor.visit_binop(binop_node)

    def test_visit_unaryop_with_undefined_variable(self):
        """Test unary operation with undefined variable."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        # Create a unary operation: -undefined_var
        unaryop_node = ast.UnaryOp(op=ast.USub(), operand=ast.Name(id="undefined_var", ctx=ast.Load()))

        with pytest.raises(CalculationError, match="Undefined variable"):
            visitor.visit_unaryop(unaryop_node)


class TestSafeASTVisitorSuccessCases:
    """Tests for successful operations to ensure error handling doesn't break normal flow."""

    def test_visit_constant_valid_number(self):
        """Test that valid numeric constants work correctly."""
        visitor = SafeASTVisitor({})

        constant_node = ast.Constant(value=42)
        result = visitor.visit_constant(constant_node)

        assert result == Decimal("42")

    def test_visit_name_defined_variable(self):
        """Test that defined variables are accessed correctly."""
        visitor = SafeASTVisitor({"salary": Decimal("5000")})

        name_node = ast.Name(id="salary", ctx=ast.Load())
        result = visitor.visit_name(name_node)

        assert result == Decimal("5000")

    def test_visit_binop_normal_operation(self):
        """Test that normal binary operations work correctly."""
        visitor = SafeASTVisitor({})

        # 10 + 20
        binop_node = ast.BinOp(left=ast.Constant(value=10), op=ast.Add(), right=ast.Constant(value=20))

        result = visitor.visit_binop(binop_node)
        assert result == Decimal("30")

    def test_visit_unaryop_positive(self):
        """Test that unary plus works correctly."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        unaryop_node = ast.UnaryOp(op=ast.UAdd(), operand=ast.Name(id="x", ctx=ast.Load()))

        result = visitor.visit_unaryop(unaryop_node)
        assert result == Decimal("10")

    def test_visit_unaryop_negative(self):
        """Test that unary minus works correctly."""
        visitor = SafeASTVisitor({"x": Decimal("10")})

        unaryop_node = ast.UnaryOp(op=ast.USub(), operand=ast.Name(id="x", ctx=ast.Load()))

        result = visitor.visit_unaryop(unaryop_node)
        assert result == Decimal("-10")

    def test_visit_call_max_function(self):
        """Test that max() function works correctly."""
        visitor = SafeASTVisitor({"a": Decimal("10"), "b": Decimal("20")})

        call_node = ast.Call(
            func=ast.Name(id="max", ctx=ast.Load()),
            args=[ast.Name(id="a", ctx=ast.Load()), ast.Name(id="b", ctx=ast.Load())],
            keywords=[],
        )

        result = visitor.visit_call(call_node)
        assert result == Decimal("20")

    def test_visit_call_round_valid_precision(self):
        """Test that round() with valid precision works correctly."""
        visitor = SafeASTVisitor({"x": Decimal("123.456")})

        call_node = ast.Call(
            func=ast.Name(id="round", ctx=ast.Load()),
            args=[ast.Name(id="x", ctx=ast.Load()), ast.Constant(value=2)],
            keywords=[],
        )

        result = visitor.visit_call(call_node)
        assert result == Decimal("123.46")
