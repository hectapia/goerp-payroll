# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Schema validation for formula engine."""

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
from goerp_payroll.schema_validator import validate_schema
from ..exceptions import ValidationError


class SchemaValidator:
    """Validates formula engine schemas."""

    def validate(self, schema: dict[str, Any]) -> None:
        """Validate a calculation schema.

        Args:
            schema: JSON schema to validate

        Raises:
            ValidationError: If schema is invalid
        """
        validate_schema(schema, error_class=ValidationError)
