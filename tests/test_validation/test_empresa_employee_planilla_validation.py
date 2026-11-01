# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for empresa-employee-planilla validation logic.

CRITICAL CONTROL: Employees and planillas must belong to the same company.
This is a fundamental internal control requirement for payroll systems.

These tests validate:
1. Payroll engine rejects employees from different companies
2. Employees cannot be added to planillas from different companies
3. Forms enforce empresa_id requirements
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from goerp_payroll.model import (
    Empleado,
    Empresa,
    Moneda,
    Planilla,
    PlanillaEmpleado,
    TipoPlanilla,
)
from tests.helpers.auth import login_user


class TestNominaEngineEmpresaValidation:
    """Test that NominaEngine validates empresa matching between employee and planilla."""

    def test_employee_without_empresa_fails_validation(self, app, db_session):
        """Employee without empresa_id should fail payroll validation."""
        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)
            db_session.commit()

            empresa = Empresa(
                codigo="EMP001",
                razon_social="Test Company",
                ruc="J-12345678-9",
                activo=True,
            )
            db_session.add(empresa)
            db_session.commit()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                activo=True,
            )
            db_session.add(tipo_planilla)
            db_session.commit()

            planilla = Planilla(
                nombre="Test Planilla",
                tipo_planilla_id=tipo_planilla.id,
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.commit()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010101-0001A",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=None,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            db_session.add(empleado)
            db_session.commit()

            from goerp_payroll.nomina_engine.validators.employee_validator import EmployeeValidator

            validator = EmployeeValidator()
            validation_result = validator.validate_employee(
                empleado, planilla.empresa_id, date(2024, 1, 1), date(2024, 1, 31)
            )
            is_valid = validation_result.is_valid
            errors = validation_result.errors  # errors is already a list of strings

            assert is_valid is False
            assert any("no está asignado a ninguna empresa" in error for error in errors)

    def test_employee_different_empresa_fails_validation(self, app, db_session):
        """Employee from different empresa should fail payroll validation."""
        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)
            db_session.commit()

            empresa1 = Empresa(
                codigo="EMP001",
                razon_social="Company One",
                ruc="J-12345678-1",
                activo=True,
            )
            empresa2 = Empresa(
                codigo="EMP002",
                razon_social="Company Two",
                ruc="J-12345678-2",
                activo=True,
            )
            db_session.add_all([empresa1, empresa2])
            db_session.commit()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                activo=True,
            )
            db_session.add(tipo_planilla)
            db_session.commit()

            planilla = Planilla(
                nombre="Planilla Company One",
                tipo_planilla_id=tipo_planilla.id,
                moneda_id=moneda.id,
                empresa_id=empresa1.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.commit()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010101-0001A",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa2.id,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            db_session.add(empleado)
            db_session.commit()

            from goerp_payroll.nomina_engine.validators.employee_validator import EmployeeValidator

            validator = EmployeeValidator()
            validation_result = validator.validate_employee(
                empleado, planilla.empresa_id, date(2024, 1, 1), date(2024, 1, 31)
            )
            is_valid = validation_result.is_valid
            errors = validation_result.errors  # errors is already a list of strings

            assert is_valid is False
            assert any("pertenece a empresa diferente" in error for error in errors)

    def test_employee_same_empresa_passes_validation(self, app, db_session):
        """Employee from same empresa should pass empresa validation."""
        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)
            db_session.commit()

            empresa = Empresa(
                codigo="EMP001",
                razon_social="Test Company",
                ruc="J-12345678-9",
                activo=True,
            )
            db_session.add(empresa)
            db_session.commit()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                activo=True,
            )
            db_session.add(tipo_planilla)
            db_session.commit()

            planilla = Planilla(
                nombre="Test Planilla",
                tipo_planilla_id=tipo_planilla.id,
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.commit()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010101-0001A",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            db_session.add(empleado)
            db_session.commit()

            from goerp_payroll.nomina_engine.validators.employee_validator import EmployeeValidator

            validator = EmployeeValidator()
            validation_result = validator.validate_employee(
                empleado, planilla.empresa_id, date(2024, 1, 1), date(2024, 1, 31)
            )
            is_valid = validation_result.is_valid
            errors = validation_result.errors  # errors is already a list of strings

            assert is_valid is True
            assert not any("empresa" in error.lower() for error in errors)


class TestPlanillaEmpleadoAssociationValidation:
    """Test validation when adding employees to planillas via UI."""

    def test_add_employee_different_empresa_rejected(self, app, client, admin_user, db_session):
        """Adding employee from different empresa should be rejected."""
        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)
            db_session.commit()

            empresa1 = Empresa(
                codigo="EMP001",
                razon_social="Company One",
                ruc="J-12345678-1",
                activo=True,
            )
            empresa2 = Empresa(
                codigo="EMP002",
                razon_social="Company Two",
                ruc="J-12345678-2",
                activo=True,
            )
            db_session.add_all([empresa1, empresa2])
            db_session.commit()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                activo=True,
            )
            db_session.add(tipo_planilla)
            db_session.commit()

            planilla = Planilla(
                nombre="Planilla Company One",
                tipo_planilla_id=tipo_planilla.id,
                moneda_id=moneda.id,
                empresa_id=empresa1.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.commit()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010101-0001A",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa2.id,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            db_session.add(empleado)
            db_session.commit()

            login_user(client, admin_user.usuario, "admin-password")

            response = client.post(
                f"/planilla/{planilla.id}/empleado/add",
                data={"empleado_id": empleado.id},
                follow_redirects=True,
            )

            assert response.status_code == 200
            assert b"misma empresa" in response.data or b"same company" in response.data

            association = db_session.execute(
                select(PlanillaEmpleado).filter_by(planilla_id=planilla.id, empleado_id=empleado.id)
            ).scalar_one_or_none()
            assert association is None

    def test_add_employee_without_empresa_rejected(self, app, client, admin_user, db_session):
        """Adding employee without empresa should be rejected."""
        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)
            db_session.commit()

            empresa = Empresa(
                codigo="EMP001",
                razon_social="Test Company",
                ruc="J-12345678-9",
                activo=True,
            )
            db_session.add(empresa)
            db_session.commit()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                activo=True,
            )
            db_session.add(tipo_planilla)
            db_session.commit()

            planilla = Planilla(
                nombre="Test Planilla",
                tipo_planilla_id=tipo_planilla.id,
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.commit()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010101-0001A",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=None,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            db_session.add(empleado)
            db_session.commit()

            login_user(client, admin_user.usuario, "admin-password")

            response = client.post(
                f"/planilla/{planilla.id}/empleado/add",
                data={"empleado_id": empleado.id},
                follow_redirects=True,
            )

            assert response.status_code == 200
            assert b"empresa asignada" in response.data or b"assigned" in response.data

            association = db_session.execute(
                select(PlanillaEmpleado).filter_by(planilla_id=planilla.id, empleado_id=empleado.id)
            ).scalar_one_or_none()
            assert association is None

    def test_add_employee_same_empresa_succeeds(self, app, client, admin_user, db_session):
        """Adding employee from same empresa should succeed."""
        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)
            db_session.commit()

            empresa = Empresa(
                codigo="EMP001",
                razon_social="Test Company",
                ruc="J-12345678-9",
                activo=True,
            )
            db_session.add(empresa)
            db_session.commit()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                activo=True,
            )
            db_session.add(tipo_planilla)
            db_session.commit()

            planilla = Planilla(
                nombre="Test Planilla",
                tipo_planilla_id=tipo_planilla.id,
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.commit()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010101-0001A",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            db_session.add(empleado)
            db_session.commit()

            login_user(client, admin_user.usuario, "admin-password")

            response = client.post(
                f"/planilla/{planilla.id}/empleado/add",
                data={"empleado_id": empleado.id},
                follow_redirects=True,
            )

            assert response.status_code == 200

            association = db_session.execute(
                select(PlanillaEmpleado).filter_by(planilla_id=planilla.id, empleado_id=empleado.id)
            ).scalar_one_or_none()
            assert association is not None


class TestConfigEmpleadosFiltering:
    """Test that config_empleados only shows employees from same empresa."""

    def test_config_empleados_filters_by_empresa(self, app, client, admin_user, db_session):
        """Config empleados should only show employees from same empresa."""
        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)
            db_session.commit()

            empresa1 = Empresa(
                codigo="EMP001",
                razon_social="Company One",
                ruc="J-12345678-1",
                activo=True,
            )
            empresa2 = Empresa(
                codigo="EMP002",
                razon_social="Company Two",
                ruc="J-12345678-2",
                activo=True,
            )
            db_session.add_all([empresa1, empresa2])
            db_session.commit()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                activo=True,
            )
            db_session.add(tipo_planilla)
            db_session.commit()

            planilla = Planilla(
                nombre="Planilla Company One",
                tipo_planilla_id=tipo_planilla.id,
                moneda_id=moneda.id,
                empresa_id=empresa1.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.commit()

            emp1_company1 = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="CompanyOne",
                identificacion_personal="001-010101-0001A",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa1.id,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            emp2_company2 = Empleado(
                codigo_empleado="EMP002",
                primer_nombre="Maria",
                primer_apellido="CompanyTwo",
                identificacion_personal="001-010101-0002B",
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa2.id,
                fecha_alta=date(2024, 1, 1),
                activo=True,
            )
            db_session.add_all([emp1_company1, emp2_company2])
            db_session.commit()

            login_user(client, admin_user.usuario, "admin-password")

            response = client.get(f"/planilla/{planilla.id}/config/empleados")

            assert response.status_code == 200
            assert b"CompanyOne" in response.data
            assert b"CompanyTwo" not in response.data
