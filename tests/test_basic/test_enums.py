# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for enums module to ensure type safety."""


def test_formula_type_enum_values():
    """
    Test FormulaType enum has expected values.

    Setup:
        - None

    Action:
        - Import and check enum values

    Verification:
        - All expected values are present
    """
    from goerp_payroll.enums import FormulaType

    assert FormulaType.FIJO == "fixed"
    assert FormulaType.PORCENTAJE == "percentage"
    assert FormulaType.PORCENTAJE_SALARIO == "salary_percentage"
    assert FormulaType.PORCENTAJE_BRUTO == "gross_percentage"
    assert FormulaType.FORMULA == "formula"
    assert FormulaType.HORAS == "hours"
    assert FormulaType.DIAS == "days"


def test_tipo_usuario_enum_values():
    """
    Test TipoUsuario enum has expected values.

    Setup:
        - None

    Action:
        - Import and check enum values

    Verification:
        - All expected values are present
    """
    from goerp_payroll.enums import TipoUsuario

    assert TipoUsuario.ADMIN == "admin"
    assert TipoUsuario.HHRR == "hr"
    assert TipoUsuario.AUDIT == "audit"


def test_nomina_estado_enum_values():
    """
    Test NominaEstado enum has expected values.

    Setup:
        - None

    Action:
        - Import and check enum values

    Verification:
        - All expected values are present
    """
    from goerp_payroll.enums import NominaEstado

    assert NominaEstado.CALCULANDO == "calculating"
    assert NominaEstado.GENERADO == "generated"
    assert NominaEstado.GENERADO_CON_ERRORES == "generated_with_errors"
    assert NominaEstado.APROBADO == "approved"
    assert NominaEstado.APLICADO == "applied"
    assert NominaEstado.ERROR == "error"


def test_metodo_amortizacion_enum_values():
    """
    Test MetodoAmortizacion enum has expected values.

    Setup:
        - None

    Action:
        - Import and check enum values

    Verification:
        - All expected values are present
    """
    from goerp_payroll.enums import MetodoAmortizacion

    assert MetodoAmortizacion.FRANCES == "french"
    assert MetodoAmortizacion.ALEMAN == "german"


def test_tipo_interes_enum_values():
    """
    Test TipoInteres enum has expected values.

    Setup:
        - None

    Action:
        - Import and check enum values

    Verification:
        - All expected values are present
    """
    from goerp_payroll.enums import TipoInteres

    assert TipoInteres.SIMPLE == "simple"
    assert TipoInteres.COMPUESTO == "compound"


def test_enums_are_strings():
    """
    Test that enum values are strings.

    Setup:
        - None

    Action:
        - Import enums and check type

    Verification:
        - All enum values are strings
    """
    from goerp_payroll.enums import FormulaType, TipoUsuario

    assert isinstance(FormulaType.FIJO, str)
    assert isinstance(TipoUsuario.ADMIN, str)


def test_enum_comparison():
    """
    Test that enum values can be compared with strings.

    Setup:
        - None

    Action:
        - Compare enum with string

    Verification:
        - Comparison works correctly
    """
    from goerp_payroll.enums import TipoUsuario

    user_type = "admin"
    assert user_type == TipoUsuario.ADMIN


def test_enum_in_list():
    """
    Test that enum values can be used in lists.

    Setup:
        - None

    Action:
        - Check membership in list

    Verification:
        - Membership check works
    """
    from goerp_payroll.enums import TipoUsuario

    allowed_types = [TipoUsuario.ADMIN, TipoUsuario.HHRR]
    assert TipoUsuario.ADMIN in allowed_types
    assert TipoUsuario.AUDIT not in allowed_types


def test_step_type_enum():
    """
    Test StepType enum used in formula engine.

    Setup:
        - None

    Action:
        - Import and check enum values

    Verification:
        - Expected values are present
    """
    from goerp_payroll.enums import StepType

    assert StepType.CALCULATION == "calculation"
    # StepType should have more values, test at least one exists
    assert isinstance(StepType.CALCULATION, str)
