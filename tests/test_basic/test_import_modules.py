# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for module importability - ensuring all modules can be imported without errors."""

import importlib

import pytest


def test_goerp_payroll_module_is_importable():
    """
    Test that the main goerp_payroll module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll module

    Verification:
        - Module imports without errors
        - Module has expected attributes
    """
    import goerp_payroll

    assert goerp_payroll is not None
    assert hasattr(goerp_payroll, "create_app")


def test_model_module_is_importable():
    """
    Test that the model module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.model module

    Verification:
        - Module imports without errors
        - Module has db instance
    """
    from goerp_payroll import model

    assert model is not None
    assert hasattr(model, "db")
    assert hasattr(model, "Usuario")
    assert hasattr(model, "Empresa")
    assert hasattr(model, "Empleado")


def test_nomina_engine_is_importable():
    """
    Test that the nomina_engine module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.nomina_engine module

    Verification:
        - Module imports without errors
        - Module has NominaEngine class
    """
    from goerp_payroll import nomina_engine

    assert nomina_engine is not None
    assert hasattr(nomina_engine, "NominaEngine")


def test_formula_engine_is_importable():
    """
    Test that the formula_engine module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.formula_engine module

    Verification:
        - Module imports without errors
        - Module has FormulaEngine class
    """
    from goerp_payroll import formula_engine

    assert formula_engine is not None
    assert hasattr(formula_engine, "FormulaEngine")


def test_auth_module_is_importable():
    """
    Test that the auth module can be imported.

    Setup:
        - None

    Action:
        - Import from goerp_payroll.auth module

    Verification:
        - Module imports without errors
        - Module has auth blueprint and proteger_passwd function
    """
    from goerp_payroll.auth import auth, proteger_passwd

    assert auth is not None
    assert proteger_passwd is not None
    assert callable(proteger_passwd)


def test_forms_module_is_importable():
    """
    Test that the forms module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.forms module

    Verification:
        - Module imports without errors
    """
    from goerp_payroll import forms

    assert forms is not None


def test_vacation_service_is_importable():
    """
    Test that the vacation_service module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.vacation_service module

    Verification:
        - Module imports without errors
        - Module has VacationService class
    """
    from goerp_payroll import vacation_service

    assert vacation_service is not None
    assert hasattr(vacation_service, "VacationService")


def test_rbac_module_is_importable():
    """
    Test that the rbac module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.rbac module

    Verification:
        - Module imports without errors
    """
    from goerp_payroll import rbac

    assert rbac is not None


def test_report_engine_is_importable():
    """
    Test that the report_engine module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.report_engine module

    Verification:
        - Module imports without errors
        - Module has required classes and functions
    """
    from goerp_payroll import report_engine

    assert report_engine is not None
    # Check for key classes/functions that exist in the module
    assert hasattr(report_engine, "CustomReportBuilder")
    assert hasattr(report_engine, "ReportExecutionManager")


def test_cli_module_is_importable():
    """
    Test that the CLI module can be imported.

    Setup:
        - None

    Action:
        - Import goerp_payroll.cli module

    Verification:
        - Module imports without errors
    """
    from goerp_payroll import cli

    assert cli is not None
    assert hasattr(cli, "main")


def test_all_vistas_modules_are_importable():
    """
    Test that all vista (view) modules can be imported.

    Setup:
        - None

    Action:
        - Import each vista module

    Verification:
        - All modules import without errors
    """
    vista_modules = [
        "user",
        "currency",
        "exchange_rate",
        "employee",
        "custom_field",
        "calculation_rule",
        "payroll_concepts",  # percepcion, deduccion are in payroll_concepts
        "prestacion",
        "planilla",
        "tipo_planilla",
        "prestamo",
        "empresa",
        "configuracion",
        "carga_inicial_prestacion",
        "vacation",
        "report",
        "settings",
    ]

    for module_name in vista_modules:
        module_path = f"goerp_payroll.vistas.{module_name}"
        try:
            module = importlib.import_module(module_path)
            assert module is not None
        except ImportError as e:
            pytest.fail(f"Failed to import {module_path}: {e}")
