# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Validators for planilla business logic."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from goerp_payroll.vistas.planilla.validators.planilla_validators import PlanillaValidator


def __getattr__(name: str) -> Any:
    """Lazy-load validator symbols to avoid import cycles at module import time."""
    if name == "PlanillaValidator":
        module = import_module("goerp_payroll.vistas.planilla.validators.planilla_validators")
        return getattr(module, "PlanillaValidator")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["PlanillaValidator"]
