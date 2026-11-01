# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for class inheritance - ensuring model classes inherit from correct base classes."""

from flask_login import UserMixin


def test_usuario_inherits_from_usermixin():
    """
    Test that Usuario class inherits from UserMixin for Flask-Login integration.

    Setup:
        - Import Usuario model

    Action:
        - Check class inheritance

    Verification:
        - Usuario inherits from UserMixin
    """
    from goerp_payroll.model import Usuario

    assert issubclass(Usuario, UserMixin), "Usuario should inherit from UserMixin"


def test_usuario_inherits_from_base_tabla():
    """
    Test that Usuario class inherits from BaseTabla.

    Setup:
        - Import Usuario and BaseTabla

    Action:
        - Check class inheritance

    Verification:
        - Usuario inherits from BaseTabla
    """
    from goerp_payroll.model import Usuario

    # Check if Usuario has attributes from BaseTabla
    assert hasattr(Usuario, "id"), "Usuario should have 'id' from BaseTabla"
    assert hasattr(Usuario, "timestamp"), "Usuario should have 'timestamp' from BaseTabla"
    assert hasattr(Usuario, "creado"), "Usuario should have 'creado' from BaseTabla"


def test_empleado_has_base_tabla_attributes():
    """
    Test that Empleado class has BaseTabla attributes.

    Setup:
        - Import Empleado model

    Action:
        - Check for BaseTabla attributes

    Verification:
        - Empleado has id, timestamp, creado attributes
    """
    from goerp_payroll.model import Empleado

    assert hasattr(Empleado, "id"), "Empleado should have 'id' from BaseTabla"
    assert hasattr(Empleado, "timestamp"), "Empleado should have 'timestamp' from BaseTabla"
    assert hasattr(Empleado, "creado"), "Empleado should have 'creado' from BaseTabla"


def test_empresa_has_base_tabla_attributes():
    """
    Test that Empresa class has BaseTabla attributes.

    Setup:
        - Import Empresa model

    Action:
        - Check for BaseTabla attributes

    Verification:
        - Empresa has id, timestamp, creado attributes
    """
    from goerp_payroll.model import Empresa

    assert hasattr(Empresa, "id"), "Empresa should have 'id' from BaseTabla"
    assert hasattr(Empresa, "timestamp"), "Empresa should have 'timestamp' from BaseTabla"
    assert hasattr(Empresa, "creado"), "Empresa should have 'creado' from BaseTabla"


def test_nomina_has_base_tabla_attributes():
    """
    Test that Nomina class has BaseTabla attributes.

    Setup:
        - Import Nomina model

    Action:
        - Check for BaseTabla attributes

    Verification:
        - Nomina has id, timestamp, creado attributes
    """
    from goerp_payroll.model import Nomina

    assert hasattr(Nomina, "id"), "Nomina should have 'id' from BaseTabla"
    assert hasattr(Nomina, "timestamp"), "Nomina should have 'timestamp' from BaseTabla"
    assert hasattr(Nomina, "creado"), "Nomina should have 'creado' from BaseTabla"


def test_planilla_has_base_tabla_attributes():
    """
    Test that Planilla class has BaseTabla attributes.

    Setup:
        - Import Planilla model

    Action:
        - Check for BaseTabla attributes

    Verification:
        - Planilla has id, timestamp, creado attributes
    """
    from goerp_payroll.model import Planilla

    assert hasattr(Planilla, "id"), "Planilla should have 'id' from BaseTabla"
    assert hasattr(Planilla, "timestamp"), "Planilla should have 'timestamp' from BaseTabla"
    assert hasattr(Planilla, "creado"), "Planilla should have 'creado' from BaseTabla"


def test_percepcion_has_base_tabla_attributes():
    """
    Test that Percepcion class has BaseTabla attributes.

    Setup:
        - Import Percepcion model

    Action:
        - Check for BaseTabla attributes

    Verification:
        - Percepcion has id, timestamp, creado attributes
    """
    from goerp_payroll.model import Percepcion

    assert hasattr(Percepcion, "id"), "Percepcion should have 'id' from BaseTabla"
    assert hasattr(Percepcion, "timestamp"), "Percepcion should have 'timestamp' from BaseTabla"
    assert hasattr(Percepcion, "creado"), "Percepcion should have 'creado' from BaseTabla"


def test_deduccion_has_base_tabla_attributes():
    """
    Test that Deduccion class has BaseTabla attributes.

    Setup:
        - Import Deduccion model

    Action:
        - Check for BaseTabla attributes

    Verification:
        - Deduccion has id, timestamp, creado attributes
    """
    from goerp_payroll.model import Deduccion

    assert hasattr(Deduccion, "id"), "Deduccion should have 'id' from BaseTabla"
    assert hasattr(Deduccion, "timestamp"), "Deduccion should have 'timestamp' from BaseTabla"
    assert hasattr(Deduccion, "creado"), "Deduccion should have 'creado' from BaseTabla"


def test_prestacion_has_base_tabla_attributes():
    """
    Test that Prestacion class has BaseTabla attributes.

    Setup:
        - Import Prestacion model

    Action:
        - Check for BaseTabla attributes

    Verification:
        - Prestacion has id, timestamp, creado attributes
    """
    from goerp_payroll.model import Prestacion

    assert hasattr(Prestacion, "id"), "Prestacion should have 'id' from BaseTabla"
    assert hasattr(Prestacion, "timestamp"), "Prestacion should have 'timestamp' from BaseTabla"
    assert hasattr(Prestacion, "creado"), "Prestacion should have 'creado' from BaseTabla"


def test_all_model_classes_are_db_models():
    """
    Test that all main model classes are SQLAlchemy models.

    Setup:
        - Import all main model classes

    Action:
        - Check if each class has __tablename__

    Verification:
        - All classes have __tablename__ attribute
    """
    from goerp_payroll.model import (
        Deduccion,
        Empleado,
        Empresa,
        Moneda,
        Nomina,
        Percepcion,
        Planilla,
        Prestacion,
        Usuario,
    )

    models = [Usuario, Empresa, Empleado, Nomina, Planilla, Percepcion, Deduccion, Prestacion, Moneda]

    for model in models:
        assert hasattr(model, "__tablename__"), f"{model.__name__} should have __tablename__ attribute"


def test_nomina_engine_error_inherits_from_exception():
    """
    Test that NominaEngineError inherits from Exception.

    Setup:
        - Import NominaEngineError

    Action:
        - Check class inheritance

    Verification:
        - NominaEngineError inherits from Exception
    """
    from goerp_payroll.nomina_engine import NominaEngineError

    assert issubclass(NominaEngineError, Exception), "NominaEngineError should inherit from Exception"


def test_formula_engine_error_inherits_from_exception():
    """
    Test that FormulaEngineError inherits from Exception.

    Setup:
        - Import FormulaEngineError

    Action:
        - Check class inheritance

    Verification:
        - FormulaEngineError inherits from Exception
    """
    from goerp_payroll.formula_engine import FormulaEngineError

    assert issubclass(FormulaEngineError, Exception), "FormulaEngineError should inherit from Exception"


def test_validation_error_inherits_from_formula_engine_error():
    """
    Test that ValidationError inherits from FormulaEngineError.

    Setup:
        - Import ValidationError and FormulaEngineError

    Action:
        - Check class inheritance

    Verification:
        - ValidationError inherits from FormulaEngineError
    """
    from goerp_payroll.formula_engine import FormulaEngineError, ValidationError

    assert issubclass(ValidationError, FormulaEngineError), "ValidationError should inherit from FormulaEngineError"


def test_calculation_error_inherits_from_formula_engine_error():
    """
    Test that CalculationError inherits from FormulaEngineError.

    Setup:
        - Import CalculationError and FormulaEngineError

    Action:
        - Check class inheritance

    Verification:
        - CalculationError inherits from FormulaEngineError
    """
    from goerp_payroll.formula_engine import CalculationError, FormulaEngineError

    assert issubclass(CalculationError, FormulaEngineError), "CalculationError should inherit from FormulaEngineError"
