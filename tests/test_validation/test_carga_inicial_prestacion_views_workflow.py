# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.

from __future__ import annotations

from decimal import Decimal

import pytest

from goerp_payroll.model import CargaInicialPrestacion, Empleado, Empresa, Moneda, Prestacion, PrestacionAcumulada
from tests.helpers.auth import login_user


def _seed_minimal_entities(db_session):
    empresa = Empresa(codigo="BEN001", razon_social="Benefits Co", ruc="J-BEN", activo=True)
    moneda = Moneda(codigo="USD", nombre="Dólar", simbolo="$", activo=True)
    prestacion = Prestacion(codigo="VAC", nombre="Vacaciones", tipo_acumulacion="monthly", activo=True)

    db_session.add_all([empresa, moneda, prestacion])
    db_session.flush()

    empleado = Empleado(
        empresa_id=empresa.id,
        codigo_empleado="EMP-BEN-001",
        primer_nombre="Juan",
        primer_apellido="Perez",
        identificacion_personal="001-010101-0001A",
        salario_base=Decimal("1000.00"),
        moneda_id=moneda.id,
        activo=True,
    )
    db_session.add(empleado)
    db_session.commit()

    return empresa, moneda, prestacion, empleado


@pytest.mark.validation
def test_carga_inicial_prestacion_index_and_reporte_get(app, client, admin_user, db_session):
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        resp = client.get("/carga-inicial-prestaciones/")
        assert resp.status_code == 200

        resp = client.get("/carga-inicial-prestaciones/reporte")
        assert resp.status_code == 200


@pytest.mark.validation
def test_carga_inicial_prestacion_create_apply_and_delete_workflow(app, client, admin_user, db_session):
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")
        _, moneda, prestacion, empleado = _seed_minimal_entities(db_session)

        # Create
        resp = client.post(
            "/carga-inicial-prestaciones/nueva",
            data={
                "empleado_id": empleado.id,
                "prestacion_id": prestacion.id,
                "anio_corte": 2024,
                "mes_corte": 6,
                "moneda_id": moneda.id,
                "saldo_acumulado": "1500.50",
                "tipo_cambio": "1.0",
                "saldo_convertido": "1500.50",
                "observaciones": "Test carga inicial",
                "submit": "Guardar",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302

        carga = (
            db_session.query(CargaInicialPrestacion)
            .filter(
                CargaInicialPrestacion.empleado_id == empleado.id,
                CargaInicialPrestacion.prestacion_id == prestacion.id,
                CargaInicialPrestacion.anio_corte == 2024,
                CargaInicialPrestacion.mes_corte == 6,
            )
            .one_or_none()
        )
        assert carga is not None
        assert carga.estado == "draft"

        # Apply
        resp = client.post(f"/carga-inicial-prestaciones/{carga.id}/aplicar", follow_redirects=False)
        assert resp.status_code == 302

        db_session.refresh(carga)
        assert carga.estado == "applied"

        trans = (
            db_session.query(PrestacionAcumulada).filter(PrestacionAcumulada.carga_inicial_id == carga.id).one_or_none()
        )
        assert trans is not None
        assert trans.tipo_transaccion == "saldo_inicial"

        # Delete applied should redirect and keep record
        resp = client.post(f"/carga-inicial-prestaciones/{carga.id}/eliminar", follow_redirects=False)
        assert resp.status_code == 302

        still_exists = db_session.get(CargaInicialPrestacion, carga.id)
        assert still_exists is not None
