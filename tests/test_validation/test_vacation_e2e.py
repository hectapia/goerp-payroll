# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""End-to-end tests for vacation management using Flask test client."""

from datetime import date, timedelta
from decimal import Decimal

from goerp_payroll.model import (
    VacationPolicy,
    VacationAccount,
    VacationNovelty,
    Empleado,
    Moneda,
    Empresa,
    Planilla,
    TipoPlanilla,
)
from tests.helpers.auth import login_user
import pytest


@pytest.mark.validation
def test_vacation_policy_index_list_all_policies(app, client, admin_user, db_session):
    """Test that user can view all vacation policies."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/vacation/policies")
        assert response.status_code == 200


@pytest.mark.validation
def test_vacation_policy_new_get_form(app, client, admin_user, db_session):
    """Test that user can access vacation policy creation form."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/vacation/policies/new")
        assert response.status_code == 200


@pytest.mark.validation
def test_vacation_account_index_list_all_accounts(app, client, admin_user, db_session):
    """Test that user can view all vacation accounts."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/vacation/accounts")
        assert response.status_code == 200


@pytest.mark.validation
def test_vacation_account_new_get_form(app, client, admin_user, db_session):
    """Test that user can access vacation account creation form."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/vacation/accounts/new")
        assert response.status_code == 200


@pytest.mark.validation
def test_vacation_leave_request_index_list_requests(app, client, admin_user, db_session):
    """Test that user can view all vacation leave requests."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/vacation/leave-requests")
        assert response.status_code == 200


@pytest.mark.validation
def test_vacation_leave_request_new_get_form(app, client, admin_user, db_session):
    """Test that user can access vacation leave request creation form."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/vacation/leave-requests/new")
        assert response.status_code == 200


@pytest.mark.validation
def test_vacation_register_taken_get_form(app, client, admin_user, db_session):
    """Test that user can access vacation taken registration form."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        response = client.get("/vacation/register-taken")
        assert response.status_code == 200


@pytest.mark.validation
def test_vacation_leave_request_approve_with_balance(app, client, admin_user, db_session):
    """Test: User approves a pending vacation leave request."""
    with app.app_context():
        empresa = Empresa(codigo="TEST001", razon_social="Test Company", ruc="J-123", activo=True)
        db_session.add(empresa)
        db_session.commit()

        moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
        db_session.add(moneda)
        db_session.commit()

        tipo_planilla = TipoPlanilla(
            codigo="MENSUAL",
            descripcion="Planilla Mensual",
            dias=30,
            periodicidad="monthly",
            activo=True,
        )
        db_session.add(tipo_planilla)
        db_session.commit()

        planilla = Planilla(
            nombre="Planilla Test",
            tipo_planilla_id=tipo_planilla.id,
            empresa_id=empresa.id,
            moneda_id=moneda.id,
            activo=True,
        )
        db_session.add(planilla)
        db_session.commit()

        empleado = Empleado(
            empresa_id=empresa.id,
            codigo_empleado="EMP001",
            primer_nombre="Juan",
            primer_apellido="Pérez",
            identificacion_personal="001-010101-0001A",
            salario_base=Decimal("10000.00"),
            moneda_id=moneda.id,
            activo=True,
        )
        db_session.add(empleado)
        db_session.commit()

        policy = VacationPolicy(
            codigo="POL001",
            nombre="Test Policy",
            empresa_id=empresa.id,
            planilla_id=planilla.id,
            accrual_rate=Decimal("15.0000"),
        )
        db_session.add(policy)
        db_session.commit()

        account = VacationAccount(
            empleado_id=empleado.id,
            policy_id=policy.id,
            current_balance=Decimal("10.0000"),
        )
        db_session.add(account)
        db_session.commit()

        start_date = date.today() + timedelta(days=10)
        end_date = start_date + timedelta(days=4)

        leave_request = VacationNovelty(
            empleado_id=empleado.id,
            account_id=account.id,
            start_date=start_date,
            end_date=end_date,
            units=Decimal("5"),
            estado="pending",
        )
        db_session.add(leave_request)
        db_session.commit()

        request_id = leave_request.id
        db_session.expunge_all()

        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(f"/vacation/leave-requests/{request_id}/approve", follow_redirects=False)

        assert response.status_code == 302
        assert f"/vacation/leave-requests/{request_id}" in response.location

        leave_request_updated = db_session.get(VacationNovelty, request_id)
        assert leave_request_updated.estado == "approved"


@pytest.mark.validation
def test_vacation_leave_request_reject(app, client, admin_user, db_session):
    """Test: User rejects a pending vacation leave request."""
    with app.app_context():
        empresa = Empresa(codigo="TEST001", razon_social="Test Company", ruc="J-123", activo=True)
        db_session.add(empresa)
        db_session.commit()

        moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
        db_session.add(moneda)
        db_session.commit()

        tipo_planilla = TipoPlanilla(
            codigo="MENSUAL",
            descripcion="Planilla Mensual",
            dias=30,
            periodicidad="monthly",
            activo=True,
        )
        db_session.add(tipo_planilla)
        db_session.commit()

        planilla = Planilla(
            nombre="Planilla Test",
            tipo_planilla_id=tipo_planilla.id,
            empresa_id=empresa.id,
            moneda_id=moneda.id,
            activo=True,
        )
        db_session.add(planilla)
        db_session.commit()

        empleado = Empleado(
            empresa_id=empresa.id,
            codigo_empleado="EMP001",
            primer_nombre="Juan",
            primer_apellido="Pérez",
            identificacion_personal="001-010101-0001A",
            salario_base=Decimal("10000.00"),
            moneda_id=moneda.id,
            activo=True,
        )
        db_session.add(empleado)
        db_session.commit()

        policy = VacationPolicy(
            codigo="POL001",
            nombre="Test Policy",
            empresa_id=empresa.id,
            planilla_id=planilla.id,
            accrual_rate=Decimal("15.0000"),
        )
        db_session.add(policy)
        db_session.commit()

        account = VacationAccount(
            empleado_id=empleado.id,
            policy_id=policy.id,
            current_balance=Decimal("10.0000"),
        )
        db_session.add(account)
        db_session.commit()

        start_date = date.today() + timedelta(days=10)
        end_date = start_date + timedelta(days=4)

        leave_request = VacationNovelty(
            empleado_id=empleado.id,
            account_id=account.id,
            start_date=start_date,
            end_date=end_date,
            units=Decimal("5"),
            estado="pending",
        )
        db_session.add(leave_request)
        db_session.commit()

        request_id = leave_request.id
        db_session.expunge_all()

        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            f"/vacation/leave-requests/{request_id}/reject",
            data={"motivo_rechazo": "Período no disponible"},
            follow_redirects=False,
        )

        assert response.status_code == 302

        leave_request_updated = db_session.get(VacationNovelty, request_id)
        assert leave_request_updated.estado == "rejected"
