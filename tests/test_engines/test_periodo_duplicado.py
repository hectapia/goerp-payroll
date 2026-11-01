# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""CRITICAL tests for overlapping payroll period validation.

These tests ensure that the system prevents paying employees twice for the same days.
This is one of the most critical validations in the payroll system to prevent:
- Double payment to employees
- Accounting errors
- Legal/compliance issues
"""

from datetime import date
from decimal import Decimal


from goerp_payroll.enums import NominaEstado
from goerp_payroll.nomina_engine import NominaEngine


class TestPeriodoDuplicadoValidation:
    """CRITICAL tests for duplicate/overlapping payroll period detection."""

    def test_validar_periodo_exactamente_duplicado(self, app, db_session):
        """Test that exact duplicate periods are rejected."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            # Setup base entities
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="QUINCENAL",
                descripcion="Quincenal",
                periodicidad="biweekly",
                dias=15,
                periodos_por_anio=24,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Quincenal",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Create existing paid nomina for Jan 1-15
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                generado_por="admin",
                estado=NominaEstado.PAGADO,
                total_bruto=Decimal("15000.00"),
                total_deducciones=Decimal("2250.00"),
                total_neto=Decimal("12750.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()

            # Try to create another nomina for THE EXACT SAME PERIOD
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 1),  # SAME START
                periodo_fin=date(2025, 1, 15),  # SAME END
                fecha_calculo=date(2025, 1, 15),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be rejected!
            assert is_valid is False
            assert len(engine.errors) > 0
            assert "se solapa" in engine.errors[0].lower()
            # Note: The error message format may not include exact dates, just check for overlap message

    def test_validar_periodo_solapado_inicio(self, app, db_session):
        """Test that periods overlapping at the start are rejected."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="QUINCENAL",
                descripcion="Quincenal",
                periodicidad="biweekly",
                dias=15,
                periodos_por_anio=24,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Quincenal",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Existing paid nomina for Jan 1-15
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                generado_por="admin",
                estado=NominaEstado.PAGADO,
                total_bruto=Decimal("15000.00"),
                total_deducciones=Decimal("2250.00"),
                total_neto=Decimal("12750.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()

            # Try to create nomina for Jan 15-31 (day 15 overlaps!)
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 15),  # OVERLAPS with existing end
                periodo_fin=date(2025, 1, 31),
                fecha_calculo=date(2025, 1, 31),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be rejected because Jan 15 is in both periods
            assert is_valid is False
            assert len(engine.errors) > 0
            assert "se solapa" in engine.errors[0].lower()

    def test_validar_periodo_solapado_fin(self, app, db_session):
        """Test that periods overlapping at the end are rejected."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="QUINCENAL",
                descripcion="Quincenal",
                periodicidad="biweekly",
                dias=15,
                periodos_por_anio=24,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Quincenal",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Existing paid nomina for Jan 16-31
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 16),
                periodo_fin=date(2025, 1, 31),
                generado_por="admin",
                estado=NominaEstado.PAGADO,
                total_bruto=Decimal("15000.00"),
                total_deducciones=Decimal("2250.00"),
                total_neto=Decimal("12750.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()

            # Try to create nomina for Jan 1-16 (day 16 overlaps!)
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 16),  # OVERLAPS with existing start
                fecha_calculo=date(2025, 1, 16),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be rejected because Jan 16 is in both periods
            assert is_valid is False
            assert len(engine.errors) > 0
            assert "se solapa" in engine.errors[0].lower()

    def test_validar_periodo_completamente_contenido(self, app, db_session):
        """Test that a period completely contained within an existing period is rejected."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                periodos_por_anio=12,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Mensual",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("30000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Existing paid nomina for entire month Jan 1-31
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 31),
                generado_por="admin",
                estado=NominaEstado.PAGADO,
                total_bruto=Decimal("30000.00"),
                total_deducciones=Decimal("4500.00"),
                total_neto=Decimal("25500.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()

            # Try to create nomina for middle of month Jan 10-20 (completely contained!)
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 10),  # Inside existing period
                periodo_fin=date(2025, 1, 20),  # Inside existing period
                fecha_calculo=date(2025, 1, 20),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be rejected because entire period is already paid
            assert is_valid is False
            assert len(engine.errors) > 0
            assert "se solapa" in engine.errors[0].lower()

    def test_validar_periodo_envuelve_existente(self, app, db_session):
        """Test that a period that completely contains an existing period is rejected."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="MENSUAL",
                descripcion="Mensual",
                periodicidad="monthly",
                dias=30,
                periodos_por_anio=12,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Mensual",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("30000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Existing paid nomina for Jan 10-20 (middle of month)
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 10),
                periodo_fin=date(2025, 1, 20),
                generado_por="admin",
                estado=NominaEstado.PAGADO,
                total_bruto=Decimal("10000.00"),
                total_deducciones=Decimal("1500.00"),
                total_neto=Decimal("8500.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()

            # Try to create nomina for entire month Jan 1-31 (contains existing!)
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 1),  # Before existing
                periodo_fin=date(2025, 1, 31),  # After existing
                fecha_calculo=date(2025, 1, 31),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be rejected because it would pay days 10-20 twice
            assert is_valid is False
            assert len(engine.errors) > 0
            assert "se solapa" in engine.errors[0].lower()

    def test_validar_periodos_consecutivos_permitidos(self, app, db_session):
        """Test that consecutive non-overlapping periods are allowed."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="QUINCENAL",
                descripcion="Quincenal",
                periodicidad="biweekly",
                dias=15,
                periodos_por_anio=24,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Quincenal",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Existing paid nomina for Jan 1-15
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                generado_por="admin",
                estado=NominaEstado.PAGADO,
                total_bruto=Decimal("15000.00"),
                total_deducciones=Decimal("2250.00"),
                total_neto=Decimal("12750.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()

            # Try to create nomina for Jan 16-31 (consecutive, no overlap!)
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 16),  # Day after previous period
                periodo_fin=date(2025, 1, 31),
                fecha_calculo=date(2025, 1, 31),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be ALLOWED because periods don't overlap
            assert is_valid is True
            assert len(engine.errors) == 0

    def test_validar_nomina_anulada_no_bloquea(self, app, db_session):
        """Test that cancelled nominas don't block new periods."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="QUINCENAL",
                descripcion="Quincenal",
                periodicidad="biweekly",
                dias=15,
                periodos_por_anio=24,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Quincenal",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Existing CANCELLED nomina for Jan 1-15
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                generado_por="admin",
                estado=NominaEstado.ANULADO,  # CANCELLED!
                total_bruto=Decimal("15000.00"),
                total_deducciones=Decimal("2250.00"),
                total_neto=Decimal("12750.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()

            # Try to create nomina for same period (should be allowed since previous was cancelled)
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                fecha_calculo=date(2025, 1, 15),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be ALLOWED because cancelled nominas don't count
            assert is_valid is True
            assert len(engine.errors) == 0

    def test_validar_diferentes_planillas_no_interfieren(self, app, db_session):
        """Test that nominas from different planillas don't interfere."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="Córdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="QUINCENAL",
                descripcion="Quincenal",
                periodicidad="biweekly",
                dias=15,
                periodos_por_anio=24,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            # Create two different planillas
            planilla1 = Planilla(
                nombre="Planilla Administrativa",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla1)

            planilla2 = Planilla(
                nombre="Planilla Operativa",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla2)

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="Pérez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp1 = PlanillaEmpleado(planilla_id=planilla1.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp1)

            planilla_emp2 = PlanillaEmpleado(planilla_id=planilla2.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp2)

            # Existing paid nomina for Planilla 1 for Jan 1-15
            nomina_planilla1 = Nomina(
                planilla_id=planilla1.id,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                generado_por="admin",
                estado=NominaEstado.PAGADO,
                total_bruto=Decimal("15000.00"),
                total_deducciones=Decimal("2250.00"),
                total_neto=Decimal("12750.00"),
            )
            db_session.add(nomina_planilla1)
            db_session.commit()

            # Try to create nomina for Planilla 2 for same period
            # This should be ALLOWED because it's a different planilla
            engine = NominaEngine(
                planilla=planilla2,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                fecha_calculo=date(2025, 1, 15),
                usuario="admin",
            )

            is_valid = engine.validar_planilla()

            # Should be ALLOWED because it's a different planilla
            assert is_valid is True
            assert len(engine.errors) == 0

    def test_validar_recalculo_ignora_nomina_original(self, app, db_session):
        """Test that recalculation can ignore the original non-approved nomina."""
        from goerp_payroll.model import Empresa, Moneda, TipoPlanilla, Planilla, Empleado, PlanillaEmpleado, Nomina

        with app.app_context():
            moneda = Moneda(codigo="NIO", nombre="CÃ³rdoba", simbolo="C$", activo=True)
            db_session.add(moneda)

            empresa = Empresa(codigo="TEST001", razon_social="Test Company SA", ruc="J-12345678")
            db_session.add(empresa)
            db_session.flush()

            tipo_planilla = TipoPlanilla(
                codigo="QUINCENAL",
                descripcion="Quincenal",
                periodicidad="biweekly",
                dias=15,
                periodos_por_anio=24,
                mes_inicio_fiscal=1,
                dia_inicio_fiscal=1,
            )
            db_session.add(tipo_planilla)
            db_session.flush()

            planilla = Planilla(
                nombre="Planilla Quincenal",
                tipo_planilla_id=tipo_planilla.id,
                empresa_id=empresa.id,
                moneda_id=moneda.id,
                activo=True,
            )
            db_session.add(planilla)
            db_session.flush()

            empleado = Empleado(
                codigo_empleado="EMP001",
                primer_nombre="Juan",
                primer_apellido="PÃ©rez",
                identificacion_personal="001-010180-0001A",
                fecha_alta=date(2024, 1, 1),
                salario_base=Decimal("15000.00"),
                moneda_id=moneda.id,
                empresa_id=empresa.id,
                activo=True,
            )
            db_session.add(empleado)
            db_session.flush()

            planilla_emp = PlanillaEmpleado(planilla_id=planilla.id, empleado_id=empleado.id, activo=True)
            db_session.add(planilla_emp)

            # Existing non-approved nomina for Jan 1-15.
            nomina_existente = Nomina(
                planilla_id=planilla.id,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                generado_por="admin",
                estado=NominaEstado.GENERADO,
                total_bruto=Decimal("15000.00"),
                total_deducciones=Decimal("2250.00"),
                total_neto=Decimal("12750.00"),
            )
            db_session.add(nomina_existente)
            db_session.commit()
            db_session.refresh(nomina_existente)

            # Recalculation should ignore the source nomina and allow the same period.
            engine = NominaEngine(
                planilla=planilla,
                periodo_inicio=date(2025, 1, 1),
                periodo_fin=date(2025, 1, 15),
                fecha_calculo=date(2025, 1, 15),
                usuario="admin",
                excluded_nomina_id=nomina_existente.id,
            )

            is_valid = engine.validar_planilla()

            assert is_valid is True
            assert len(engine.errors) == 0
