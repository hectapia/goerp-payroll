# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Mapping of novelty codes to their calculation behavior.

This module defines the mapping between novelty codes and their
calculation behavior (perception/deduction, gravable, etc.).
"""

# ................................ CONTANTES ................................ #
NOVELTY_CODES = {
    "OVERTIME": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Horas extra trabajadas",
    },
    "OVERTIME_DOUBLE": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Horas extra dobles (feriados/domingos)",
    },
    "ABSENCE": {
        "tipo": "deduction",
        "gravable": False,
        "descripcion": "Ausencia no justificada",
    },
    "DISABILITY": {
        "tipo": "deduction",
        "gravable": False,
        "descripcion": "Incapacidad médica",
    },
    "COMMISSION": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Comisiones por ventas",
    },
    "BONUS": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Bonificación",
    },
    "ALLOWANCE": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Viáticos",
    },
    "VACATION": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Pago de vacaciones",
    },
    "ADVANCE": {
        "tipo": "deduction",
        "gravable": False,
        "descripcion": "Adelanto de salario",
    },
    "LOAN": {
        "tipo": "deduction",
        "gravable": False,
        "descripcion": "Cuota de préstamo",
    },
    # A. Compensación Base y Directa
    "BONUS_OBJECTIVES": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Bono por cumplimiento de objetivos",
    },
    "BONUS_ANNUAL": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Bono anual o trimestral",
    },
    "HAZARD_PAY": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Plus por peligrosidad o toxicidad",
    },
    "NIGHT_SHIFT": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Plus por trabajo nocturno",
    },
    "SENIORITY_PAY": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Plus por antigüedad",
    },
    # B. Compensaciones en Especie y Beneficios
    "VEHICLE_USE": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Uso de vehículo de empresa",
    },
    "HEALTH_INSURANCE": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Seguro de salud privado",
    },
    "PENSION_CONTRIBUTION": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Aporte patronal a pensión/retiro",
    },
    "STOCK_OPTIONS": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Opciones de compra de acciones",
    },
    "FOOD_ALLOWANCE": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Subsidio de alimentación",
    },
    "TRANSPORT_ALLOWANCE": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Subsidio de transporte",
    },
    "CHILDCARE_ALLOWANCE": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Subsidio de guardería",
    },
    # C. Compensaciones por Tiempo y Bienestar
    "HOLIDAY_PAY": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Pago por días festivos trabajados",
    },
    "THIRTEENTH_SALARY": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Aguinaldo o gratificación anual",
    },
    "UTILIDADES": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Participación en utilidades",
    },
    "PERMISO_PAGADO": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Permisos pagados (enfermedad, maternidad, etc.)",
    },
    "FONDO_AHORRO_EMPRESA": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Aporte empresa a fondo de ahorro",
    },
    "FONDO_AHORRO_EMPLEADO": {
        "tipo": "deduction",
        "gravable": False,
        "descripcion": "Aporte empleado a fondo de ahorro",
    },
    # D. Reembolsos y Dietas
    "GASTOS_REPRESENTACION": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Gastos de representación",
    },
    "REEMBOLSO_FORMACION": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Reembolso de gastos de formación",
    },
    "REEMBOLSO_MEDICO": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Reembolso de gastos médicos",
    },
    # E. Pagos por Eventos Específicos
    "INDEMNIZACION": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Indemnización por despido",
    },
    "COMPENSACION_REUBICACION": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Compensación por reubicación",
    },
    "PREMIO_PUNTUALIDAD": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Premio por puntualidad/asistencia",
    },
    "PREMIO_INNOVACION": {
        "tipo": "income",
        "gravable": True,
        "descripcion": "Premio por ideas innovadoras",
    },
    "AYUDA_FALLECIMIENTO": {
        "tipo": "income",
        "gravable": False,
        "descripcion": "Ayuda por fallecimiento de familiar",
    },
}
