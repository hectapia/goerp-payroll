# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for instance creation - ensuring main classes can be instantiated correctly."""


def test_usuario_can_be_instantiated():
    """
    Test that Usuario instances can be created.

    Setup:
        - Import Usuario model

    Action:
        - Create a Usuario instance

    Verification:
        - Instance is created successfully
        - Instance is of correct type
    """
    from goerp_payroll.model import Usuario

    user = Usuario()
    assert user is not None
    assert isinstance(user, Usuario)


def test_usuario_has_required_attributes():
    """
    Test that Usuario has required attributes.

    Setup:
        - Import Usuario model

    Action:
        - Create a Usuario instance and check attributes

    Verification:
        - Has usuario, acceso, nombre, apellido, tipo attributes
    """
    from goerp_payroll.model import Usuario

    user = Usuario()
    assert hasattr(user, "usuario")
    assert hasattr(user, "acceso")
    assert hasattr(user, "nombre")
    assert hasattr(user, "apellido")
    assert hasattr(user, "tipo")
    assert hasattr(user, "activo")


def test_empresa_can_be_instantiated():
    """
    Test that Empresa instances can be created.

    Setup:
        - Import Empresa model

    Action:
        - Create an Empresa instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Empresa

    empresa = Empresa()
    assert empresa is not None
    assert isinstance(empresa, Empresa)


def test_empleado_can_be_instantiated():
    """
    Test that Empleado instances can be created.

    Setup:
        - Import Empleado model

    Action:
        - Create an Empleado instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Empleado

    empleado = Empleado()
    assert empleado is not None
    assert isinstance(empleado, Empleado)


def test_nomina_can_be_instantiated():
    """
    Test that Nomina instances can be created.

    Setup:
        - Import Nomina model

    Action:
        - Create a Nomina instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Nomina

    nomina = Nomina()
    assert nomina is not None
    assert isinstance(nomina, Nomina)


def test_planilla_can_be_instantiated():
    """
    Test that Planilla instances can be created.

    Setup:
        - Import Planilla model

    Action:
        - Create a Planilla instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Planilla

    planilla = Planilla()
    assert planilla is not None
    assert isinstance(planilla, Planilla)


def test_percepcion_can_be_instantiated():
    """
    Test that Percepcion instances can be created.

    Setup:
        - Import Percepcion model

    Action:
        - Create a Percepcion instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Percepcion

    percepcion = Percepcion()
    assert percepcion is not None
    assert isinstance(percepcion, Percepcion)


def test_deduccion_can_be_instantiated():
    """
    Test that Deduccion instances can be created.

    Setup:
        - Import Deduccion model

    Action:
        - Create a Deduccion instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Deduccion

    deduccion = Deduccion()
    assert deduccion is not None
    assert isinstance(deduccion, Deduccion)


def test_prestacion_can_be_instantiated():
    """
    Test that Prestacion instances can be created.

    Setup:
        - Import Prestacion model

    Action:
        - Create a Prestacion instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Prestacion

    prestacion = Prestacion()
    assert prestacion is not None
    assert isinstance(prestacion, Prestacion)


def test_moneda_can_be_instantiated():
    """
    Test that Moneda instances can be created.

    Setup:
        - Import Moneda model

    Action:
        - Create a Moneda instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.model import Moneda

    moneda = Moneda()
    assert moneda is not None
    assert isinstance(moneda, Moneda)


def test_nomina_engine_class_exists():
    """
    Test that NominaEngine class exists and can be imported.

    Setup:
        - Import NominaEngine class

    Action:
        - Verify class exists

    Verification:
        - NominaEngine class is importable
        - NominaEngine is a class
    """
    from goerp_payroll.nomina_engine import NominaEngine

    assert NominaEngine is not None
    assert callable(NominaEngine)  # Can be called as a constructor


def test_formula_engine_can_be_instantiated():
    """
    Test that FormulaEngine instances can be created.

    Setup:
        - Import FormulaEngine class

    Action:
        - Create a FormulaEngine instance

    Verification:
        - Instance is created successfully
    """
    from goerp_payroll.formula_engine import FormulaEngine

    # FormulaEngine requires a schema
    schema = {"steps": []}
    engine = FormulaEngine(schema)
    assert engine is not None
    assert isinstance(engine, FormulaEngine)


def test_vacation_service_class_exists():
    """
    Test that VacationService class exists and can be imported.

    Setup:
        - Import VacationService class

    Action:
        - Verify class exists

    Verification:
        - VacationService class is importable
        - VacationService is a class
    """
    from goerp_payroll.vacation_service import VacationService

    assert VacationService is not None
    assert callable(VacationService)  # Can be called as a constructor


def test_report_engine_classes_exist():
    """
    Test that report_engine module has required classes.

    Setup:
        - Import report_engine module

    Action:
        - Verify classes exist

    Verification:
        - CustomReportBuilder and ReportExecutionManager classes exist
    """
    from goerp_payroll import report_engine

    assert hasattr(report_engine, "CustomReportBuilder")
    assert hasattr(report_engine, "ReportExecutionManager")
    assert callable(report_engine.CustomReportBuilder)
    assert callable(report_engine.ReportExecutionManager)


def test_generador_de_codigos_unicos_returns_string():
    """
    Test that generador_de_codigos_unicos returns a string.

    Setup:
        - Import function from model

    Action:
        - Call function

    Verification:
        - Returns a non-empty string
    """
    from goerp_payroll.model import generador_de_codigos_unicos

    codigo = generador_de_codigos_unicos()
    assert isinstance(codigo, str)
    assert len(codigo) > 0


def test_generador_codigo_empleado_returns_correct_format():
    """
    Test that generador_codigo_empleado returns correct format.

    Setup:
        - Import function from model

    Action:
        - Call function

    Verification:
        - Returns string starting with EMP-
    """
    from goerp_payroll.model import generador_codigo_empleado

    codigo = generador_codigo_empleado()
    assert isinstance(codigo, str)
    assert codigo.startswith("EMP-")
    # Format is EMP- (4 chars) + 6 alphanumeric characters
    expected_length = len("EMP-") + 6
    assert len(codigo) == expected_length


def test_db_instance_exists():
    """
    Test that db instance exists and is configured.

    Setup:
        - Import db from model

    Action:
        - Check db instance

    Verification:
        - db is not None
        - db has expected methods
    """
    from goerp_payroll.model import db

    assert db is not None
    assert hasattr(db, "Model")
    assert hasattr(db, "Column")
    assert hasattr(db, "session")
