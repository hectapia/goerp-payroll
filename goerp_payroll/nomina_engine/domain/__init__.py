# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Domain models for payroll processing."""

from .payroll_context import PayrollContext
from .employee_calculation import EmployeeCalculation, EmpleadoCalculo
from .calculation_items import DeduccionItem, PercepcionItem, PrestacionItem

__all__ = [
    "PayrollContext",
    "EmployeeCalculation",
    "EmpleadoCalculo",
    "DeduccionItem",
    "PercepcionItem",
    "PrestacionItem",
]
