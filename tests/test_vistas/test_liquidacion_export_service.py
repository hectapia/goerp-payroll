# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.

from __future__ import annotations

from datetime import date
from decimal import Decimal
from io import BytesIO

import pytest

from goerp_payroll.model import Empresa, Empleado, Liquidacion, LiquidacionDetalle


def test_exportar_liquidacion_excel_success(app, db_session):
    with app.app_context():
        from goerp_payroll.vistas.planilla.services.export_service import ExportService

        empresa = Empresa(codigo="E1", razon_social="Empresa", ruc="RUC", activo=True)
        db_session.add(empresa)
        db_session.flush()

        empleado = Empleado(
            empresa_id=empresa.id,
            codigo_empleado="EMPX",
            primer_nombre="Juan",
            primer_apellido="Perez",
            identificacion_personal="ID-EMPX",
            fecha_alta=date(2025, 1, 1),
            salario_base=Decimal("300.00"),
            activo=True,
        )
        db_session.add(empleado)
        db_session.flush()

        liquidacion = Liquidacion(
            empleado_id=empleado.id,
            fecha_calculo=date(2025, 1, 1),
            ultimo_dia_pagado=date(2024, 12, 31),
            dias_por_pagar=1,
            estado="draft",
            total_bruto=Decimal("10.00"),
            total_deducciones=Decimal("0.00"),
            total_neto=Decimal("10.00"),
        )
        db_session.add(liquidacion)
        db_session.flush()

        d1 = LiquidacionDetalle(
            liquidacion_id=liquidacion.id,
            tipo="income",
            codigo="DIAS_POR_PAGAR",
            descripcion="Días por pagar",
            monto=Decimal("10.00"),
            orden=1,
        )
        db_session.add(d1)
        db_session.commit()

        output, filename = ExportService.exportar_liquidacion_excel(liquidacion)

        assert isinstance(output, BytesIO)
        assert filename.startswith("liquidacion_")
        output.seek(0)
        content = output.read()
        assert content.startswith(b"PK")


def test_exportar_liquidacion_excel_missing_openpyxl(app, db_session, monkeypatch):
    with app.app_context():
        from goerp_payroll.vistas.planilla.services import export_service
        from goerp_payroll.vistas.planilla.services.export_service import ExportService

        def mock_check_openpyxl():
            return None

        monkeypatch.setattr(export_service, "check_openpyxl_available", mock_check_openpyxl)

        liquidacion = Liquidacion(
            empleado_id="dummy",
            fecha_calculo=date(2025, 1, 1),
            dias_por_pagar=0,
            estado="draft",
        )

        with pytest.raises(ImportError, match="openpyxl no está disponible"):
            ExportService.exportar_liquidacion_excel(liquidacion)
