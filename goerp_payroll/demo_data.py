# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Demo data loading for manual testing.

This module provides comprehensive sample data to facilitate manual testing
of the payroll system. Data is loaded when COATI_LOAD_DEMO_DATA environment
variable is set.
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from datetime import date, timedelta
from decimal import Decimal
from typing import cast
from dateutil.relativedelta import relativedelta

# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from goerp_payroll.enums import NominaEstado, NovedadEstado
from goerp_payroll.model import (
    db,
    Empresa,
    Empleado,
    Moneda,
    TipoPlanilla,
    Planilla,
    PlanillaEmpleado,
    PlanillaIngreso,
    PlanillaDeduccion,
    PlanillaPrestacion,
    Percepcion,
    Deduccion,
    Prestacion,
    Nomina,
    NominaNovedad,
)
from goerp_payroll.log import log


def load_demo_companies() -> tuple[Empresa, Empresa]:
    """Create two demo companies with complete information.

    Returns:
        tuple: Two Empresa objects (company1, company2)
    """
    log.trace("Loading demo companies...")

    empresa1 = db.session.execute(db.select(Empresa).filter_by(codigo="DEMO001")).scalar_one_or_none()
    empresa2 = db.session.execute(db.select(Empresa).filter_by(codigo="DEMO002")).scalar_one_or_none()

    if empresa1 is None:
        empresa1 = Empresa()
        empresa1.codigo = "DEMO001"
        empresa1.razon_social = "Tecnología y Soluciones S.A."
        empresa1.nombre_comercial = "TechSol"
        empresa1.ruc = "J0310000123456"
        empresa1.direccion = "Km 7.5 Carretera a Masaya, Managua"
        empresa1.telefono = "+505 2255-1234"
        empresa1.correo = "info@techsol-demo.com"
        empresa1.sitio_web = "www.techsol-demo.com"
        empresa1.representante_legal = "María Elena Gutiérrez"
        empresa1.activo = True
        db.session.add(empresa1)
        log.trace("Created demo company: Tecnología y Soluciones S.A.")

    if empresa2 is None:
        empresa2 = Empresa()
        empresa2.codigo = "DEMO002"
        empresa2.razon_social = "Servicios Profesionales BMO Ltda."
        empresa2.nombre_comercial = "BMO Services"
        empresa2.ruc = "J0310000654321"
        empresa2.direccion = "Plaza España, módulo 5, Managua"
        empresa2.telefono = "+505 2277-5678"
        empresa2.correo = "contacto@bmo-services-demo.com"
        empresa2.sitio_web = "www.bmo-services-demo.com"
        empresa2.representante_legal = "Carlos Antonio Ramírez"
        empresa2.activo = True
        db.session.add(empresa2)
        log.trace("Created demo company: Servicios Profesionales BMO Ltda.")

    db.session.commit()
    return empresa1, empresa2


def load_demo_employees(empresa1: Empresa, empresa2: Empresa) -> list[Empleado]:
    """Create diverse demo employees for testing.

    Creates 15 employees with varied:
    - Salaries (from minimum wage to executive level)
    - Positions and departments
    - Contract types and employment dates
    - Personal information

    Args:
        empresa1: First demo company
        empresa2: Second demo company

    Returns:
        list: List of created Empleado objects
    """
    log.trace("Loading demo employees...")

    # Get currency (use NIO if available, otherwise first available)
    moneda = db.session.execute(db.select(Moneda).filter_by(codigo="NIO")).scalar_one_or_none()

    if moneda is None:
        moneda = db.session.execute(db.select(Moneda)).scalars().first()

    if moneda is None:
        log.trace("No currency available for demo employees")
        return []

    empleados_data = [
        # Company 1 - Tecnología y Soluciones
        {
            "codigo": "DEMO-EMP001",
            "primer_nombre": "Juan",
            "segundo_nombre": "Carlos",
            "primer_apellido": "Pérez",
            "segundo_apellido": "González",
            "identificacion_personal": "001-150890-0001K",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1990, 8, 15),
            "cargo": "Gerente de Tecnología",
            "area": "Tecnología",
            "salario_base": Decimal("35000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=730),  # 2 years ago
            "empresa": empresa1,
            "correo": "jperez@techsol-demo.com",
            "telefono": "+505 8888-1234",
        },
        {
            "codigo": "DEMO-EMP002",
            "primer_nombre": "María",
            "segundo_nombre": "Elena",
            "primer_apellido": "Rodríguez",
            "segundo_apellido": "Morales",
            "identificacion_personal": "001-220685-0002M",
            "genero": "Femenino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1985, 6, 22),
            "cargo": "Desarrolladora Senior",
            "area": "Tecnología",
            "salario_base": Decimal("28000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=1095),  # 3 years ago
            "empresa": empresa1,
            "correo": "mrodriguez@techsol-demo.com",
            "telefono": "+505 8888-2345",
        },
        {
            "codigo": "DEMO-EMP003",
            "primer_nombre": "Carlos",
            "segundo_nombre": "Alberto",
            "primer_apellido": "Martínez",
            "segundo_apellido": "López",
            "identificacion_personal": "001-100992-0003N",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1992, 9, 10),
            "cargo": "Desarrollador Junior",
            "area": "Tecnología",
            "salario_base": Decimal("15000.00"),
            "tipo_contrato": "Temporal",
            "fecha_alta": date.today() - timedelta(days=180),  # 6 months ago
            "empresa": empresa1,
            "correo": "cmartinez@techsol-demo.com",
            "telefono": "+505 8888-3456",
        },
        {
            "codigo": "DEMO-EMP004",
            "primer_nombre": "Ana",
            "segundo_nombre": "Patricia",
            "primer_apellido": "García",
            "segundo_apellido": "Hernández",
            "identificacion_personal": "001-050888-0004L",
            "genero": "Femenino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1988, 8, 5),
            "cargo": "Contador",
            "area": "Finanzas",
            "salario_base": Decimal("22000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=1460),  # 4 years ago
            "empresa": empresa1,
            "correo": "agarcia@techsol-demo.com",
            "telefono": "+505 8888-4567",
        },
        {
            "codigo": "DEMO-EMP005",
            "primer_nombre": "Roberto",
            "segundo_nombre": "José",
            "primer_apellido": "Flores",
            "segundo_apellido": "Gutiérrez",
            "identificacion_personal": "001-181195-0005P",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1995, 11, 18),
            "cargo": "Asistente Administrativo",
            "area": "Administración",
            "salario_base": Decimal("12000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=365),  # 1 year ago
            "empresa": empresa1,
            "correo": "rflores@techsol-demo.com",
            "telefono": "+505 8888-5678",
        },
        {
            "codigo": "DEMO-EMP006",
            "primer_nombre": "Laura",
            "segundo_nombre": "Isabel",
            "primer_apellido": "Ramírez",
            "segundo_apellido": "Castro",
            "identificacion_personal": "001-250687-0006R",
            "genero": "Femenino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1987, 6, 25),
            "cargo": "Jefa de Recursos Humanos",
            "area": "Recursos Humanos",
            "salario_base": Decimal("26000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=900),  # ~2.5 years ago
            "empresa": empresa1,
            "correo": "lramirez@techsol-demo.com",
            "telefono": "+505 8888-6789",
        },
        {
            "codigo": "DEMO-EMP007",
            "primer_nombre": "Diego",
            "segundo_nombre": "Andrés",
            "primer_apellido": "Sánchez",
            "segundo_apellido": "Vargas",
            "identificacion_personal": "001-120993-0007T",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1993, 9, 12),
            "cargo": "Analista de Soporte",
            "area": "Tecnología",
            "salario_base": Decimal("18000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=545),  # ~1.5 years ago
            "empresa": empresa1,
            "correo": "dsanchez@techsol-demo.com",
            "telefono": "+505 8888-7890",
        },
        {
            "codigo": "DEMO-EMP008",
            "primer_nombre": "Gabriela",
            "segundo_nombre": "Sofía",
            "primer_apellido": "Mendoza",
            "segundo_apellido": "Ortiz",
            "identificacion_personal": "001-080391-0008U",
            "genero": "Femenino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1991, 3, 8),
            "cargo": "Diseñadora UX/UI",
            "area": "Tecnología",
            "salario_base": Decimal("20000.00"),
            "tipo_contrato": "Temporal",
            "fecha_alta": date.today() - timedelta(days=270),  # 9 months ago
            "empresa": empresa1,
            "correo": "gmendoza@techsol-demo.com",
            "telefono": "+505 8888-8901",
        },
        # Company 2 - Servicios Profesionales BMO
        {
            "codigo": "DEMO-EMP009",
            "primer_nombre": "Fernando",
            "segundo_nombre": "Luis",
            "primer_apellido": "Torres",
            "segundo_apellido": "Ruiz",
            "identificacion_personal": "001-301284-0009V",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1984, 12, 30),
            "cargo": "Director General",
            "area": "Dirección",
            "salario_base": Decimal("50000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=1825),  # 5 years ago
            "empresa": empresa2,
            "correo": "ftorres@bmo-services-demo.com",
            "telefono": "+505 7777-1234",
        },
        {
            "codigo": "DEMO-EMP010",
            "primer_nombre": "Patricia",
            "segundo_nombre": "Mercedes",
            "primer_apellido": "Jiménez",
            "segundo_apellido": "Silva",
            "identificacion_personal": "001-140689-0010W",
            "genero": "Femenino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1989, 6, 14),
            "cargo": "Consultora Senior",
            "area": "Consultoría",
            "salario_base": Decimal("32000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=1095),  # 3 years ago
            "empresa": empresa2,
            "correo": "pjimenez@bmo-services-demo.com",
            "telefono": "+505 7777-2345",
        },
        {
            "codigo": "DEMO-EMP011",
            "primer_nombre": "Miguel",
            "segundo_nombre": "Ángel",
            "primer_apellido": "Herrera",
            "segundo_apellido": "Díaz",
            "identificacion_personal": "001-221090-0011X",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1990, 10, 22),
            "cargo": "Consultor",
            "area": "Consultoría",
            "salario_base": Decimal("24000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=730),  # 2 years ago
            "empresa": empresa2,
            "correo": "mherrera@bmo-services-demo.com",
            "telefono": "+505 7777-3456",
        },
        {
            "codigo": "DEMO-EMP012",
            "primer_nombre": "Claudia",
            "segundo_nombre": "Beatriz",
            "primer_apellido": "Moreno",
            "segundo_apellido": "Rivas",
            "identificacion_personal": "001-190992-0012Y",
            "genero": "Femenino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1992, 9, 19),
            "cargo": "Asistente de Consultoría",
            "area": "Consultoría",
            "salario_base": Decimal("16000.00"),
            "tipo_contrato": "Temporal",
            "fecha_alta": date.today() - timedelta(days=365),  # 1 year ago
            "empresa": empresa2,
            "correo": "cmoreno@bmo-services-demo.com",
            "telefono": "+505 7777-4567",
        },
        {
            "codigo": "DEMO-EMP013",
            "primer_nombre": "Sergio",
            "segundo_nombre": "Rafael",
            "primer_apellido": "Vega",
            "segundo_apellido": "Campos",
            "identificacion_personal": "001-051286-0013Z",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1986, 12, 5),
            "cargo": "Contador General",
            "area": "Finanzas",
            "salario_base": Decimal("28000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=1460),  # 4 years ago
            "empresa": empresa2,
            "correo": "svega@bmo-services-demo.com",
            "telefono": "+505 7777-5678",
        },
        {
            "codigo": "DEMO-EMP014",
            "primer_nombre": "Lucía",
            "segundo_nombre": "Fernanda",
            "primer_apellido": "Navarro",
            "segundo_apellido": "Pérez",
            "identificacion_personal": "001-280894-0014A",
            "genero": "Femenino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1994, 8, 28),
            "cargo": "Recepcionista",
            "area": "Administración",
            "salario_base": Decimal("11000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=545),  # ~1.5 years ago
            "empresa": empresa2,
            "correo": "lnavarro@bmo-services-demo.com",
            "telefono": "+505 7777-6789",
        },
        {
            "codigo": "DEMO-EMP015",
            "primer_nombre": "Andrés",
            "segundo_nombre": "Mauricio",
            "primer_apellido": "Cruz",
            "segundo_apellido": "Aguilar",
            "identificacion_personal": "001-170791-0015B",
            "genero": "Masculino",
            "nacionalidad": "Nicaragüense",
            "fecha_nacimiento": date(1991, 7, 17),
            "cargo": "Analista Financiero",
            "area": "Finanzas",
            "salario_base": Decimal("19000.00"),
            "tipo_contrato": "Indefinido",
            "fecha_alta": date.today() - timedelta(days=630),  # ~1.7 years ago
            "empresa": empresa2,
            "correo": "acruz@bmo-services-demo.com",
            "telefono": "+505 7777-7890",
        },
    ]

    empleados = []
    for emp_data in empleados_data:
        # Check if employee already exists
        existing = db.session.execute(
            db.select(Empleado).filter_by(codigo_empleado=emp_data["codigo"])
        ).scalar_one_or_none()

        if existing is None:
            empleado = Empleado()
            empleado.codigo_empleado = emp_data["codigo"]
            empleado.primer_nombre = emp_data["primer_nombre"]
            empleado.segundo_nombre = emp_data.get("segundo_nombre")
            empleado.primer_apellido = emp_data["primer_apellido"]
            empleado.segundo_apellido = emp_data.get("segundo_apellido")
            empleado.identificacion_personal = emp_data["identificacion_personal"]
            empleado.genero = emp_data.get("genero")
            empleado.nacionalidad = emp_data.get("nacionalidad")
            empleado.tipo_identificacion = "Cédula"
            empleado.fecha_nacimiento = emp_data.get("fecha_nacimiento")
            empleado.fecha_alta = emp_data["fecha_alta"]
            empleado.activo = True
            empleado.cargo = emp_data.get("cargo")
            empleado.area = emp_data.get("area")
            empleado.salario_base = emp_data["salario_base"]
            empleado.tipo_contrato = emp_data.get("tipo_contrato")
            empleado.moneda_id = moneda.id
            empresa = cast(Empresa, emp_data["empresa"])
            empleado.empresa_id = empresa.id
            empleado.correo = emp_data.get("correo")
            empleado.telefono = emp_data.get("telefono")
            empleado.estado_civil = "Soltero"

            db.session.add(empleado)
            empleados.append(empleado)
            log.trace("Created demo employee: %s %s", empleado.primer_nombre, empleado.primer_apellido)
        else:
            empleados.append(existing)

    db.session.commit()
    return empleados


def load_demo_payrolls(
    empresa1: Empresa, empresa2: Empresa, empleados: list[Empleado]
) -> tuple[Planilla | None, Planilla | None]:
    """Create demo payrolls with assigned employees and concepts.

    Args:
        empresa1: First demo company
        empresa2: Second demo company
        empleados: List of demo employees

    Returns:
        tuple: Two Planilla objects (planilla1, planilla2)
    """
    log.trace("Loading demo payrolls...")

    # Get or create required data
    moneda = db.session.execute(db.select(Moneda).filter_by(codigo="NIO")).scalar_one_or_none()

    if moneda is None:
        moneda = db.session.execute(db.select(Moneda)).scalars().first()

    tipo_planilla = db.session.execute(db.select(TipoPlanilla).filter_by(codigo="MONTHLY")).scalar_one_or_none()

    if tipo_planilla is None:
        tipo_planilla = db.session.execute(db.select(TipoPlanilla)).scalars().first()

    if moneda is None or tipo_planilla is None:
        log.trace("Required data (currency or payroll type) not available")
        return None, None

    # Create Planilla 1 for Company 1
    planilla1 = db.session.execute(db.select(Planilla).filter_by(nombre="Planilla Demo - TechSol")).scalar_one_or_none()

    if planilla1 is None:
        planilla1 = Planilla()
        planilla1.nombre = "Planilla Demo - TechSol"
        planilla1.descripcion = "Planilla de demostración para Tecnología y Soluciones S.A."
        planilla1.tipo_planilla_id = tipo_planilla.id
        planilla1.moneda_id = moneda.id
        planilla1.empresa_id = empresa1.id
        planilla1.activo = True
        db.session.add(planilla1)
        log.trace("Created demo payroll: Planilla Demo - TechSol")

    # Create Planilla 2 for Company 2
    planilla2 = db.session.execute(
        db.select(Planilla).filter_by(nombre="Planilla Demo - BMO Services")
    ).scalar_one_or_none()

    if planilla2 is None:
        planilla2 = Planilla()
        planilla2.nombre = "Planilla Demo - BMO Services"
        planilla2.descripcion = "Planilla de demostración para Servicios Profesionales BMO Ltda."
        planilla2.tipo_planilla_id = tipo_planilla.id
        planilla2.moneda_id = moneda.id
        planilla2.empresa_id = empresa2.id
        planilla2.activo = True
        db.session.add(planilla2)
        log.trace("Created demo payroll: Planilla Demo - BMO Services")

    db.session.commit()

    # Assign employees to payrolls
    for empleado in empleados:
        if empleado.empresa_id == empresa1.id:
            planilla = planilla1
        elif empleado.empresa_id == empresa2.id:
            planilla = planilla2
        else:
            continue

        # Check if already assigned
        existing = db.session.execute(
            db.select(PlanillaEmpleado).filter_by(planilla_id=planilla.id, empleado_id=empleado.id)
        ).scalar_one_or_none()

        if existing is None:
            asignacion = PlanillaEmpleado()
            asignacion.planilla_id = planilla.id
            asignacion.empleado_id = empleado.id
            asignacion.activo = True
            asignacion.fecha_inicio = empleado.fecha_alta
            db.session.add(asignacion)
            log.trace("Assigned employee %s to payroll %s", empleado.codigo_empleado, planilla.nombre)

    db.session.commit()

    # Assign perceptions, deductions, and benefits
    _assign_concepts_to_payroll(planilla1)
    _assign_concepts_to_payroll(planilla2)

    return planilla1, planilla2


def _assign_concepts_to_payroll(planilla: Planilla) -> None:
    """Assign common perceptions, deductions, and benefits to a payroll.

    Args:
        planilla: Planilla to assign concepts to
    """
    # Get some common concepts
    percepciones = (
        db.session.execute(
            db.select(Percepcion).filter(Percepcion.codigo.in_(["OVERTIME", "BONUSES", "TRANSPORT_ALLOWANCE"]))
        )
        .scalars()
        .all()
    )

    for percepcion in percepciones:
        existing = db.session.execute(
            db.select(PlanillaIngreso).filter_by(planilla_id=planilla.id, percepcion_id=percepcion.id)
        ).scalar_one_or_none()

        if existing is None:
            asignacion = PlanillaIngreso()
            asignacion.planilla_id = planilla.id
            asignacion.percepcion_id = percepcion.id
            asignacion.activo = True
            asignacion.editable = True
            db.session.add(asignacion)

    # Assign deductions
    deducciones = (
        db.session.execute(
            db.select(Deduccion).filter(Deduccion.codigo.in_(["UNPAID_ABSENCES", "TARDINESS", "INTERNAL_LOANS"]))
        )
        .scalars()
        .all()
    )

    for idx, deduccion in enumerate(deducciones):
        existing = db.session.execute(
            db.select(PlanillaDeduccion).filter_by(planilla_id=planilla.id, deduccion_id=deduccion.id)
        ).scalar_one_or_none()

        if existing is None:
            asignacion = PlanillaDeduccion()
            asignacion.planilla_id = planilla.id
            asignacion.deduccion_id = deduccion.id
            asignacion.prioridad = 300 + (idx * 10)  # Set priority
            asignacion.activo = True
            asignacion.editable = True
            db.session.add(asignacion)

    # Assign benefits
    prestaciones = (
        db.session.execute(
            db.select(Prestacion).filter(
                Prestacion.codigo.in_(["PAID_VACATION_PROVISION", "THIRTEENTH_SALARY_PROVISION"])
            )
        )
        .scalars()
        .all()
    )

    for prestacion in prestaciones:
        existing = db.session.execute(
            db.select(PlanillaPrestacion).filter_by(planilla_id=planilla.id, prestacion_id=prestacion.id)
        ).scalar_one_or_none()

        if existing is None:
            asignacion = PlanillaPrestacion()
            asignacion.planilla_id = planilla.id
            asignacion.prestacion_id = prestacion.id
            asignacion.activo = True
            asignacion.editable = True
            db.session.add(asignacion)

    db.session.commit()


def create_demo_nomina(planilla: Planilla) -> Nomina | None:
    """Create a demo payroll run for next month.

    Creates a nomina with dynamically generated dates to ensure it always
    occurs in the month immediately following the initial application setup date.

    Args:
        planilla: Planilla to create nomina for

    Returns:
        Nomina object or None if creation failed
    """
    log.trace("Creating demo nomina for payroll: %s", planilla.nombre)

    # Calculate dates for next month
    today = date.today()
    next_month_start = today.replace(day=1) + relativedelta(months=1)
    next_month_end = (next_month_start + relativedelta(months=1)) - timedelta(days=1)

    # Check if demo nomina already exists for this period
    existing = db.session.execute(
        db.select(Nomina).filter_by(
            planilla_id=planilla.id, periodo_inicio=next_month_start, periodo_fin=next_month_end
        )
    ).scalar_one_or_none()

    if existing is not None:
        log.trace("Demo nomina already exists for period %s to %s", next_month_start, next_month_end)
        return existing

    # Create nomina
    nomina = Nomina()
    nomina.planilla_id = planilla.id
    nomina.periodo_inicio = next_month_start
    nomina.periodo_fin = next_month_end
    nomina.estado = NominaEstado.GENERADO
    nomina.total_bruto = Decimal("0.00")
    nomina.total_deducciones = Decimal("0.00")
    nomina.total_neto = Decimal("0.00")
    db.session.add(nomina)
    db.session.commit()

    log.trace("Created demo nomina for period %s to %s", next_month_start, next_month_end)
    return nomina


def create_demo_novelties(empleados: list[Empleado]) -> None:
    """Create demo novelties (overtime, absences) for employees.

    Creates various types of novelties to demonstrate the system's
    capability to handle employee-specific adjustments.

    Args:
        empleados: List of employees to create novelties for
    """
    log.trace("Creating demo novelties...")

    if len(empleados) < 5:
        log.trace("Not enough employees to create demo novelties")
        return

    # Get perceptions for overtime
    overtime = db.session.execute(db.select(Percepcion).filter_by(codigo="OVERTIME")).scalar_one_or_none()

    # Get deduction for absences
    absence = db.session.execute(db.select(Deduccion).filter_by(codigo="UNPAID_ABSENCES")).scalar_one_or_none()

    # Get a demo nomina to associate novelties with
    # (We'll use the first available nomina or None)
    nomina = db.session.execute(db.select(Nomina)).scalars().first()

    if nomina is None:
        log.trace("No nomina available to associate novelties")
        # Novelties can still be created without a nomina (as pending)

    # Create overtime for some employees
    if overtime:
        for i in [0, 1, 4]:  # First, second, and fifth employee
            if i < len(empleados):
                empleado = empleados[i]

                # Check if novedad already exists
                if nomina:
                    existing = db.session.execute(
                        db.select(NominaNovedad).filter_by(
                            nomina_id=nomina.id, empleado_id=empleado.id, codigo_concepto=overtime.codigo
                        )
                    ).scalar_one_or_none()

                    if existing is None:
                        novedad = NominaNovedad()
                        novedad.nomina_id = nomina.id
                        novedad.empleado_id = empleado.id
                        novedad.tipo_valor = "horas"
                        novedad.codigo_concepto = overtime.codigo
                        novedad.valor_cantidad = Decimal("8.0")  # 8 hours overtime
                        novedad.fecha_novedad = date.today() - timedelta(days=5)
                        novedad.percepcion_id = overtime.id
                        novedad.es_inasistencia = bool(getattr(overtime, "es_inasistencia", False))
                        novedad.descontar_pago_inasistencia = bool(
                            getattr(overtime, "descontar_pago_inasistencia", False)
                        )
                        novedad.estado = NovedadEstado.PENDIENTE
                        db.session.add(novedad)
                        log.trace("Created overtime novedad for %s", empleado.codigo_empleado)

    # Create absences for some employees
    if absence:
        for i in [2, 3]:  # Third and fourth employee
            if i < len(empleados):
                empleado = empleados[i]

                # Check if novedad already exists
                if nomina:
                    existing = db.session.execute(
                        db.select(NominaNovedad).filter_by(
                            nomina_id=nomina.id, empleado_id=empleado.id, codigo_concepto=absence.codigo
                        )
                    ).scalar_one_or_none()

                    if existing is None:
                        novedad = NominaNovedad()
                        novedad.nomina_id = nomina.id
                        novedad.empleado_id = empleado.id
                        novedad.tipo_valor = "dias"
                        novedad.codigo_concepto = absence.codigo
                        novedad.valor_cantidad = Decimal("1.0")  # 1 day absence
                        novedad.fecha_novedad = date.today() - timedelta(days=3)
                        novedad.deduccion_id = absence.id
                        novedad.es_inasistencia = bool(getattr(absence, "es_inasistencia", False))
                        novedad.descontar_pago_inasistencia = bool(
                            getattr(absence, "descontar_pago_inasistencia", False)
                        )
                        novedad.estado = NovedadEstado.PENDIENTE
                        db.session.add(novedad)
                        log.trace("Created absence novedad for %s", empleado.codigo_empleado)

    db.session.commit()


def load_demo_data() -> None:
    """Load all demo data into the database.

    This function orchestrates the loading of comprehensive demo data:
    1. Creates demo companies
    2. Creates demo employees
    3. Creates demo payrolls and assigns employees
    4. Assigns perceptions, deductions, and benefits
    5. Creates a demo nomina for next month
    6. Creates demo novelties

    This function is idempotent - safe to call multiple times.
    """
    try:
        log.trace("=" * 60)
        log.trace("Loading demo data for manual testing...")
        log.trace("=" * 60)

        # 1. Create demo companies
        empresa1, empresa2 = load_demo_companies()

        # 2. Create demo employees
        empleados = load_demo_employees(empresa1, empresa2)

        if not empleados:
            log.trace("No employees created, skipping payroll and nomina creation")
            return

        # 3. Create demo payrolls with employees and concepts
        planilla1, _ = load_demo_payrolls(empresa1, empresa2, empleados)

        # 4. Create demo nomina for next month (for first payroll)
        if planilla1:
            create_demo_nomina(planilla1)

        # 5. Create demo novelties
        create_demo_novelties(empleados)

        log.trace("=" * 60)
        log.trace("Demo data loading completed successfully!")
        log.trace("=" * 60)
        log.trace("Created %s demo employees", len(empleados))
        log.trace("Created 2 demo companies")
        log.trace("Created 2 demo payrolls with assigned concepts")
        log.trace("Created demo novelties (overtime, absences)")
        log.trace("=" * 60)

    except Exception as exc:
        log.error("Error loading demo data: %s", exc)
        log.exception("Demo data loading exception")
        db.session.rollback()
