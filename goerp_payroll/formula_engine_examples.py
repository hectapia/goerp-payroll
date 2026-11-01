# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Formula calculation engine examples for payroll processing.

IMPORTANT: EXAMPLE DATA ONLY - NOT PART OF THE ENGINE
=========================================================
The examples in this module are provided SOLELY for demonstration and testing
purposes. They do NOT represent legal rules, tax rates, or compliance requirements
for any specific jurisdiction.

Per the project's Social Contract:
- The engine is jurisdiction-agnostic and does not incorporate hardcoded legal rules.
- These examples use fictional/placeholder values that may not reflect any real legislation.
- Implementers must define their own rules based on their specific legal requirements.
- The project makes no guarantees about the correctness of these examples for any use case.

These examples demonstrate the STRUCTURE and CAPABILITIES of the formula engine,
not actual legal calculations.
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #


# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #


# ===========================================================================
# EXAMPLE: Progressive Income Tax Calculation Schema
# ===========================================================================
# This is a DEMONSTRATION of how to structure a progressive tax calculation.
# The values, rates, and brackets shown are FICTIONAL and for illustration only.
# Implementers must create their own schemas based on applicable laws.
# ===========================================================================
EXAMPLE_PROGRESSIVE_TAX_SCHEMA = {
    "meta": {
        "name": "Example Progressive Income Tax",
        "jurisdiction": "Example Jurisdiction",
        "reference_currency": "XXX",
        "version": "1.0.0",
        "description": "EXAMPLE ONLY: Demonstrates progressive income tax calculation. "
        "Values are fictional. Implementers must define their own rules.",
    },
    "inputs": [
        {
            "name": "salario_mensual",
            "type": "decimal",
            "source": "empleado.salario_base",
            "description": "Salario mensual bruto",
        },
        {
            "name": "social_security_deduction",
            "type": "decimal",
            "source": "calculated",
            "description": "Pre-tax social security deduction (example)",
        },
        {
            "name": "meses_restantes",
            "type": "integer",
            "default": 12,
            "description": "Meses restantes en el año fiscal",
        },
        {
            "name": "salario_acumulado",
            "type": "decimal",
            "default": 0,
            "description": "Salario bruto acumulado del año",
        },
        {
            "name": "ir_retenido_acumulado",
            "type": "decimal",
            "default": 0,
            "description": "IR ya retenido en el año",
        },
    ],
    "steps": [
        {
            "name": "salario_neto_mensual",
            "type": "calculation",
            "formula": "salario_mensual - social_security_deduction",
            "description": "Net salary after pre-tax deductions",
        },
        {
            "name": "expectativa_anual",
            "type": "calculation",
            "formula": "salario_neto_mensual * meses_restantes",
            "description": "Proyección de salario restante del año",
        },
        {
            "name": "base_imponible_anual",
            "type": "calculation",
            "formula": "salario_acumulado + expectativa_anual",
            "description": "Base imponible anual total",
        },
        {
            "name": "annual_tax",
            "type": "tax_lookup",
            "table": "example_tax_brackets",
            "input": "base_imponible_anual",
            "description": "Annual tax calculation using example brackets",
        },
        {
            "name": "pending_tax",
            "type": "calculation",
            "formula": "annual_tax - ir_retenido_acumulado",
            "description": "Pending tax to withhold",
        },
        {
            "name": "monthly_tax",
            "type": "calculation",
            "formula": "pending_tax / meses_restantes",
            "description": "Tax to withhold this month",
        },
    ],
    # EXAMPLE TAX BRACKETS - FICTIONAL VALUES FOR DEMONSTRATION ONLY
    # These do NOT represent any real tax legislation.
    # Implementers must define their own brackets based on applicable laws.
    "tax_tables": {
        "example_tax_brackets": [
            {"min": 0, "max": 100000, "rate": 0, "fixed": 0, "over": 0},
            {"min": 100000.01, "max": 200000, "rate": 0.10, "fixed": 0, "over": 100000},
            {"min": 200000.01, "max": 350000, "rate": 0.15, "fixed": 10000, "over": 200000},
            {"min": 350000.01, "max": 500000, "rate": 0.20, "fixed": 32500, "over": 350000},
            {"min": 500000.01, "max": None, "rate": 0.25, "fixed": 62500, "over": 500000},
        ]
    },
    "output": "monthly_tax",
}

# Backward compatibility alias - DEPRECATED, will be removed in future versions
# This alias exists only to prevent breaking existing code that references the old name.
# New code should use EXAMPLE_PROGRESSIVE_TAX_SCHEMA instead.
EXAMPLE_IR_NICARAGUA_SCHEMA = EXAMPLE_PROGRESSIVE_TAX_SCHEMA
