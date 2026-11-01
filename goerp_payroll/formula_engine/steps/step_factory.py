# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Factory for creating step instances."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from typing import Any

# <-------------------------------------------------------------------------> #
# Third party packages
# <-------------------------------------------------------------------------> #
from goerp_payroll.enums import StepType

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from ..exceptions import CalculationError
from .assignment_step import AssignmentStep
from .base_step import Step
from .calculation_step import CalculationStep
from .conditional_step import ConditionalStep
from .tax_lookup_step import TaxLookupStep


class StepFactory:
    """Factory for creating step instances."""

    @staticmethod
    def create_step(step_config: dict[str, Any]) -> Step:
        """Create a step instance from configuration.

        Args:
            step_config: Step configuration dictionary

        Returns:
            Step instance

        Raises:
            CalculationError: If step type is unknown
        """
        step_type = step_config.get("type")
        step_name = step_config.get("name", "unnamed_step")

        if step_type == StepType.CALCULATION:
            return CalculationStep(step_name, step_config)
        if step_type == StepType.CONDITIONAL:
            return ConditionalStep(step_name, step_config)
        if step_type == StepType.TAX_LOOKUP:
            return TaxLookupStep(step_name, step_config)
        if step_type == StepType.ASSIGNMENT:
            return AssignmentStep(step_name, step_config)
        raise CalculationError(f"Unknown step type: {step_type}")
