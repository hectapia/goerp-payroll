# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Schema validation for formula engine calculation rules.

This module provides validation functions for JSON schemas used by the
FormulaEngine to ensure they have the correct structure before execution.
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
import ast
from typing import Any, Type

# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from goerp_payroll.enums import StepType
from goerp_payroll.formula_engine.ast.safe_operators import (
    ALLOWED_AST_TYPES,
    SAFE_FUNCTIONS,
    validate_expression_complexity,
)

__all__ = ["ValidationError", "validate_schema", "validate_schema_deep"]


class ValidationError(Exception):
    """Exception for validation errors in schema or data."""


def validate_schema(schema: dict[str, Any], error_class: Type[Exception] = ValidationError) -> None:
    """Validate the calculation schema structure.

    Args:
        schema: The JSON schema to validate

    Raises:
        ValidationError: If schema is missing required fields or has invalid structure
    """
    if not isinstance(schema, dict):
        raise error_class("Schema must be a dictionary")

    # Check for required sections
    if "steps" not in schema:
        raise error_class("Schema must contain 'steps' section")

    # Validate steps structure
    for i, step in enumerate(schema.get("steps", [])):
        if not isinstance(step, dict):
            raise error_class(f"Step {i} must be a dictionary")
        if "name" not in step:
            raise error_class(f"Step {i} must have a 'name' field")
        if "type" not in step:
            raise error_class(f"Step {i} must have a 'type' field")


def validate_schema_deep(schema: dict[str, Any], error_class: Type[Exception] = ValidationError) -> None:
    """Validate the calculation schema structure including formula safety.

    This performs deeper validation than validate_schema, including checking
    formulas for unsafe operations. Use this for API validation endpoints.

    Args:
        schema: The JSON schema to validate
        error_class: Exception class to raise on error

    Raises:
        ValidationError: If schema is invalid or contains unsafe formulas
    """
    # First do basic validation
    validate_schema(schema, error_class)

    # Get valid step types
    valid_step_types = {step_type.value for step_type in StepType}

    # Then validate step types and formulas for safety
    for i, step in enumerate(schema.get("steps", [])):
        step_type = step.get("type")

        # Validate step type
        if step_type not in valid_step_types:
            raise error_class(
                f"Step {i} has invalid type '{step_type}'. Valid types are: {', '.join(valid_step_types)}"
            )

        # Validate formulas for calculation steps
        if step_type == StepType.CALCULATION:
            formula = step.get("formula", "")
            if formula:
                _validate_formula_safety(formula, error_class)

        # Validate conditional step formulas
        if step_type == StepType.CONDITIONAL:
            if_true = step.get("if_true", "")
            if_false = step.get("if_false", "")
            if if_true:
                _validate_formula_safety(if_true, error_class)
            if if_false:
                _validate_formula_safety(if_false, error_class)


def _validate_formula_safety(formula: str, error_class: Type[Exception] = ValidationError) -> None:
    """Validate that a formula doesn't contain unsafe operations.

    Args:
        formula: Formula string to validate
        error_class: Exception class to raise on error

    Raises:
        ValidationError: If formula contains unsafe operations
    """
    if not formula or not isinstance(formula, str):
        return

    try:
        # Parse the formula into an AST
        tree = ast.parse(formula, mode="eval")

        try:
            validate_expression_complexity(tree, formula)
        except ValueError as e:
            raise error_class(str(e)) from e

        # Check for unsafe operations using whitelist
        for node in ast.walk(tree):
            if not isinstance(node, ALLOWED_AST_TYPES):
                raise error_class(f"Unsafe AST node type '{node.__class__.__name__}' is not allowed in formulas")

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise error_class("Only named functions are allowed in formulas")
                if node.func.id not in SAFE_FUNCTIONS:
                    raise error_class(
                        f"Function '{node.func.id}' is not allowed in formulas. "
                        f"Allowed functions: {', '.join(sorted(SAFE_FUNCTIONS.keys()))}"
                    )
    except SyntaxError as e:
        raise error_class(f"Invalid formula syntax: {e}") from e
