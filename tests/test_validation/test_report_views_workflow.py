# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.

from __future__ import annotations

from decimal import Decimal

import pytest

from goerp_payroll.enums import ReportStatus, ReportType, TipoUsuario
from goerp_payroll.model import Empleado, Empresa, Moneda, Report, ReportExecution, ReportRole
from tests.factories.user_factory import create_user
from tests.helpers.auth import login_user


def _create_company_currency_employee(db_session):
    empresa = Empresa(codigo="RPT001", razon_social="Report Co", ruc="J-123", activo=True)
    db_session.add(empresa)
    db_session.flush()

    moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
    db_session.add(moneda)
    db_session.flush()

    emp = Empleado(
        empresa_id=empresa.id,
        codigo_empleado="EMP-RPT-001",
        primer_nombre="Juan",
        primer_apellido="Pérez",
        identificacion_personal="001-010101-0001A",
        salario_base=Decimal("1000.00"),
        moneda_id=moneda.id,
        activo=True,
    )
    db_session.add(emp)
    db_session.flush()

    return empresa, moneda, emp


def _create_minimal_custom_report(db_session, *, name: str = "Employees Report") -> Report:
    report = Report(
        name=name,
        description="Test custom report",
        type=ReportType.CUSTOM,
        status=ReportStatus.ENABLED,
        base_entity="Employee",
        category="employee",
        definition={
            "columns": [
                {"type": "field", "entity": "Employee", "field": "codigo_empleado", "label": "codigo_empleado"},
                {"type": "field", "entity": "Employee", "field": "primer_nombre", "label": "primer_nombre"},
            ],
            "filters": [],
            "sorting": [{"field": "codigo_empleado", "direction": "asc"}],
        },
    )
    db_session.add(report)
    db_session.flush()

    # For non-admins, the list is filtered by permissions.
    perm = ReportRole(report_id=report.id, role=TipoUsuario.HHRR, can_view=True, can_execute=True, can_export=False)
    db_session.add(perm)
    db_session.commit()

    return report


@pytest.mark.validation
def test_report_index_get_as_admin(app, client, admin_user, db_session):
    with app.app_context():
        _create_company_currency_employee(db_session)
        _create_minimal_custom_report(db_session)

        login_user(client, admin_user.usuario, "admin-password")
        resp = client.get("/report/")
        assert resp.status_code == 200


@pytest.mark.validation
def test_report_admin_index_requires_admin(app, client, db_session):
    with app.app_context():
        hhrr_user = create_user(db_session, "hr-reports", "password", tipo=TipoUsuario.HHRR)
        login_user(client, hhrr_user.usuario, "password")

        resp = client.get("/report/admin", follow_redirects=False)
        assert resp.status_code in [302, 403]


@pytest.mark.validation
def test_report_execute_run_and_toggle_status_as_admin(app, client, admin_user, db_session):
    with app.app_context():
        _create_company_currency_employee(db_session)
        report = _create_minimal_custom_report(db_session, name="Employees Report 2")

        login_user(client, admin_user.usuario, "admin-password")

        # Execution form
        resp = client.get(f"/report/{report.id}/execute")
        assert resp.status_code == 200

        # Run report (JSON API)
        resp = client.post(f"/report/{report.id}/run", json={"page": 1, "per_page": 10})
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload is not None
        assert payload.get("success") is True
        assert "execution_id" in payload

        execution = db_session.get(ReportExecution, payload["execution_id"])
        assert execution is not None
        assert execution.report_id == report.id

        # Toggle enabled/disabled
        resp = client.post(f"/report/{report.id}/toggle-status", follow_redirects=False)
        assert resp.status_code == 302

        db_session.refresh(report)
        assert report.status in [ReportStatus.ENABLED, ReportStatus.DISABLED]


@pytest.mark.validation
def test_report_permissions_update_as_admin(app, client, admin_user, db_session):
    with app.app_context():
        _create_company_currency_employee(db_session)
        report = _create_minimal_custom_report(db_session, name="Employees Report 3")

        login_user(client, admin_user.usuario, "admin-password")

        resp = client.get(f"/report/{report.id}/permissions")
        assert resp.status_code == 200

        resp = client.post(
            f"/report/{report.id}/permissions",
            data={
                f"{TipoUsuario.ADMIN}_can_view": "on",
                f"{TipoUsuario.ADMIN}_can_execute": "on",
                f"{TipoUsuario.ADMIN}_can_export": "on",
                f"{TipoUsuario.HHRR}_can_view": "on",
                f"{TipoUsuario.HHRR}_can_execute": "on",
                # HHRR export intentionally off
                f"{TipoUsuario.AUDIT}_can_view": "on",
                # Audit execute/export intentionally off
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302


@pytest.mark.validation
def test_report_run_denied_for_user_without_permission(app, client, db_session):
    with app.app_context():
        _create_company_currency_employee(db_session)
        report = _create_minimal_custom_report(db_session, name="Employees Report 4")

        # Explicitly deny execute for audit
        audit_perm = ReportRole(
            report_id=report.id, role=TipoUsuario.AUDIT, can_view=True, can_execute=False, can_export=False
        )
        db_session.add(audit_perm)
        db_session.commit()

        audit_user = create_user(db_session, "audit-reports", "password", tipo=TipoUsuario.AUDIT)
        login_user(client, audit_user.usuario, "password")

        resp = client.post(f"/report/{report.id}/run", json={})
        assert resp.status_code == 403
        payload = resp.get_json()
        assert payload is not None
        assert "error" in payload
