# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from tests.helpers.auth import login_user


from goerp_payroll.model import db


@pytest.fixture
def empresa(app, db_session):
    with app.app_context():
        from goerp_payroll.model import Empresa

        e = Empresa(codigo="EMP", razon_social="Empresa", ruc="RUC", activo=True)
        db_session.add(e)
        db_session.commit()
        db_session.refresh(e)
        return e


@pytest.fixture
def moneda(app, db_session):
    with app.app_context():
        from goerp_payroll.model import Moneda

        m = Moneda(codigo="USD", nombre="Dollar", simbolo="$", activo=True)
        db_session.add(m)
        db_session.commit()
        db_session.refresh(m)
        return m


@pytest.fixture
def tipo_planilla(app, db_session):
    with app.app_context():
        from goerp_payroll.model import TipoPlanilla

        t = TipoPlanilla(codigo="MONTHLY", descripcion="Mensual", periodicidad="monthly", dias=30, activo=True)
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)
        return t


@pytest.fixture
def planilla(app, db_session, empresa, moneda, tipo_planilla, admin_user):
    with app.app_context():
        from goerp_payroll.model import Planilla

        p = Planilla(
            nombre="Planilla E2E",
            descripcion="",
            tipo_planilla_id=tipo_planilla.id,
            moneda_id=moneda.id,
            empresa_id=empresa.id,
            activo=True,
            creado_por=admin_user.usuario,
        )
        db_session.add(p)
        db_session.commit()
        db_session.refresh(p)
        return p


@pytest.fixture
def empleado(app, db_session, empresa):
    with app.app_context():
        from goerp_payroll.model import Empleado

        emp = Empleado(
            empresa_id=empresa.id,
            codigo_empleado="E2E1",
            primer_nombre="Juan",
            primer_apellido="Perez",
            identificacion_personal="ID-E2E1",
            fecha_alta=date(2025, 1, 1),
            salario_base=Decimal("300.00"),
            activo=True,
        )
        db_session.add(emp)
        db_session.commit()
        db_session.refresh(emp)
        return emp


@pytest.fixture
def concepto(app, db_session):
    with app.app_context():
        from goerp_payroll.model import LiquidacionConcepto

        c = LiquidacionConcepto(codigo="RENUNCIA", nombre="Renuncia", descripcion="", activo=True)
        db_session.add(c)
        db_session.commit()
        db_session.refresh(c)
        return c


def test_liquidaciones_requires_login(client):
    resp = client.get("/liquidaciones/", follow_redirects=False)
    assert resp.status_code in (302, 303)


def test_crear_y_ver_liquidacion(client, app, db_session, admin_user, empleado, concepto):
    login_user(client, "admin-test", "admin-password")

    resp = client.post(
        "/liquidaciones/nueva",
        data={
            "empleado_id": empleado.id,
            "concepto_id": concepto.id,
            "fecha_calculo": "2025-01-01",
        },
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)

    with app.app_context():
        from goerp_payroll.model import Liquidacion

        liq = db_session.execute(db.select(Liquidacion).where(Liquidacion.empleado_id == empleado.id)).scalars().one()
        assert liq.estado == "draft"

        # detail page
        resp2 = client.get(f"/liquidaciones/{liq.id}")
        assert resp2.status_code == 200


def test_recalcular_liquidacion(client, app, db_session, admin_user, empleado, concepto):
    login_user(client, "admin-test", "admin-password")

    # Create
    client.post(
        "/liquidaciones/nueva",
        data={
            "empleado_id": empleado.id,
            "concepto_id": concepto.id,
            "fecha_calculo": "2025-01-01",
        },
        follow_redirects=False,
    )

    with app.app_context():
        from goerp_payroll.model import Liquidacion

        liq = db_session.execute(db.select(Liquidacion).where(Liquidacion.empleado_id == empleado.id)).scalars().one()

    resp = client.post(f"/liquidaciones/{liq.id}/recalcular", follow_redirects=False)
    assert resp.status_code in (302, 303)

    with app.app_context():
        from goerp_payroll.model import Liquidacion

        liq2 = db_session.get(Liquidacion, liq.id)
        assert liq2 is not None
        assert liq2.estado == "draft"


def test_aplicar_inactiva_empleado_y_desvincula_planillas(
    client, app, db_session, admin_user, empleado, concepto, planilla
):
    login_user(client, "admin-test", "admin-password")

    with app.app_context():
        from goerp_payroll.model import PlanillaEmpleado

        pe = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
        db_session.add(pe)
        db_session.commit()

    client.post(
        "/liquidaciones/nueva",
        data={
            "empleado_id": empleado.id,
            "concepto_id": concepto.id,
            "fecha_calculo": "2025-01-01",
        },
        follow_redirects=False,
    )

    with app.app_context():
        from goerp_payroll.model import Liquidacion

        liq = db_session.execute(db.select(Liquidacion).where(Liquidacion.empleado_id == empleado.id)).scalars().one()

    resp = client.post(f"/liquidaciones/{liq.id}/aplicar", follow_redirects=False)
    assert resp.status_code in (302, 303)

    with app.app_context():
        from goerp_payroll.model import Empleado, PlanillaEmpleado, Liquidacion

        emp = db_session.get(Empleado, empleado.id)
        assert emp is not None
        assert emp.activo is False
        assert emp.fecha_baja == date(2025, 1, 1)

        pe2 = (
            db_session.execute(db.select(PlanillaEmpleado).where(PlanillaEmpleado.empleado_id == empleado.id))
            .scalars()
            .one()
        )
        assert pe2.activo is False
        assert pe2.fecha_fin == date(2025, 1, 1)

        liq2 = db_session.get(Liquidacion, liq.id)
        assert liq2.estado == "applied"


def test_pagar_liquidacion(client, app, db_session, admin_user, empleado, concepto, planilla):
    login_user(client, "admin-test", "admin-password")

    with app.app_context():
        from goerp_payroll.model import PlanillaEmpleado

        pe = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
        db_session.add(pe)
        db_session.commit()

    client.post(
        "/liquidaciones/nueva",
        data={
            "empleado_id": empleado.id,
            "concepto_id": concepto.id,
            "fecha_calculo": "2025-01-01",
        },
        follow_redirects=False,
    )

    with app.app_context():
        from goerp_payroll.model import Liquidacion

        liq = db_session.execute(db.select(Liquidacion).where(Liquidacion.empleado_id == empleado.id)).scalars().one()

    client.post(f"/liquidaciones/{liq.id}/aplicar", follow_redirects=False)

    resp = client.post(f"/liquidaciones/{liq.id}/pagar", follow_redirects=False)
    assert resp.status_code in (302, 303)

    with app.app_context():
        from goerp_payroll.model import Liquidacion

        liq2 = db_session.get(Liquidacion, liq.id)
        assert liq2.estado == "paid"
