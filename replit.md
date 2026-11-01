# Proyecto: GoERP Payroll - Sistema de Nómina Agnóstico a Jurisdicción

## Estado Actual
**Versión 1.0.0** - Release estable (02 feb 2026)

## Cambios Recientes - Compliance del Contrato Social

### Refactorización para Cumplimiento del SOCIAL_CONTRACT.md

1. **formula_engine_examples.py**: Renombrado `EXAMPLE_IR_NICARAGUA_SCHEMA` → `EXAMPLE_PROGRESSIVE_TAX_SCHEMA`
   - Alias de compatibilidad hacia atrás preservado
   - Disclaimers claros indicando datos ficticios

2. **Variables en ConceptCalculator**: Agregados aliases genéricos
   - `inss_periodo` (legacy, deprecado pero mantenido)
   - `pre_tax_deductions` (nuevo, recomendado)
   - `social_security_deduction` (nuevo, recomendado)

3. **Comentarios y ejemplos**: Cambiados de específicos a genéricos
   - `IR_NICARAGUA` → `INCOME_TAX_001`
   - `INSS_LABORAL` → `SOCIAL_SEC_001`
   - `Nicaragua` → `Country A`

4. **Documentación de valores por defecto**: Agregados disclaimers en config_repository.py

## Validación del Cálculo de IR

### Requisito ✅
Sistema calcula correctamente **IR anual de C$ 34,799.00** para trabajador con:
- Salario ordinario anual: C$ 300,000
- Ingresos ocasionales: C$ 17,000
- Total bruto anual: C$ 321,500
- Método: Acumulado (Art. 19 numeral 6 LCT)

## Tests Implementados

### Tests de Validación de IR - ✅ 41 TESTS PASANDO
- `tests/test_validation/test_nicaragua_ir_calculation.py` - 41 tests validando cálculo exacto de IR
- Alcanzado: IR exacto C$ 34,799.00 sin tolerancia

### Tests End-to-End de Vacaciones - 9/11 TESTS PASANDO
- Nuevo: `tests/test_vistas/test_vacation_e2e.py` - Tests basados en patrón test_prestamo_e2e.py
- Cubre: Políticas, cuentas, solicitudes de vacaciones
- Status: 9 tests pasando, 2 con problemas de fixture DB (no de lógica)

### Tests de Acumulación de Prestaciones - ✅ ACTUALIZADO
- `tests/test_validation/test_prestaciones_accumulation.py`
- Corregido: Método de cálculo para meses calendario completos (sin prorrateo)
- Resultado esperado: C$ 1,249.50 por mes (15000 × 8.33%)

## Archivos Principales

### Motores de Cálculo
- `goerp_payroll/nomina_engine.py` - Motor de nómina con cálculos exactos
- `goerp_payroll/formula_engine.py` - Motor de evaluación de fórmulas
- `goerp_payroll/vacation_service.py` - Servicio de gestión de vacaciones

### Vistas (Frontend)
- `goerp_payroll/vistas/vacation.py` - Gestión de políticas, cuentas y solicitudes de vacaciones (1035 líneas)

### Guías de Implementación
- `docs/local_guides/nicaragua-ir-paso-a-paso.md` - Guía paso a paso
- `docs/local_guides/nicaragua-implementacion-tecnica.md` - Detalles técnicos

## Diseño de Períodos de Pago

### Regla Crítica: Calendarios vs Prorratos
```
Meses calendario completos (1er día a último día):
- NO se prorratean
- Usan salario base completo
- Ejemplo: 1-31 enero = salario_base × porcentaje

Períodos parciales:
- SÍ se prorratean
- Divisor: 30 días estándar (TipoPlanilla.dias)
- Ejemplo: 15 días = (salario_base / 30) × 15 × porcentaje
```

## Control Interno: Validación Empresa-Empleado-Planilla

### Requisito de Control ✅ IMPLEMENTADO
Para que el sistema calcule correctamente una nómina, tanto el empleado como la planilla **DEBEN estar vinculados a la misma empresa**.

### Validaciones Implementadas
1. **Motor de Nómina (`nomina_engine.py`)**: Valida que `empleado.empresa_id == planilla.empresa_id` antes de procesar
2. **Formulario de Planilla**: `empresa_id` es **obligatorio** al crear/editar planilla
3. **Asignación de Empleados**: Solo se pueden asignar empleados de la misma empresa
4. **Filtro en UI**: `/planilla/<id>/config/empleados` solo muestra empleados de la misma empresa

### Tests de Validación - ✅ 7 TESTS PASANDO
- `tests/test_validation/test_empresa_employee_planilla_validation.py`
- Cubre: Validación en motor de nómina, asignación de empleados, filtrado en UI

### Mensajes de Error
- Si empleado no tiene empresa: "Empleado X no está asignado a ninguna empresa"
- Si empresas no coinciden: "Empleado X pertenece a empresa diferente a la planilla"

## Configuración Clave del Sistema

### INSS (Deducción)
- Formula: `formula_tipo="porcentaje_bruto"`
- Tasa: 7% del salario bruto
- Base: Incluye percepciones (no solo salario base)

### Prestaciones (Aguinaldo, Indemnización)
- Formula: `formula_tipo="porcentaje_salario"`
- Acumulación: Anual o de por vida
- Cálculo: Sin prorrateo en meses calendario completos

## Release 1.0.0

### Archivos Actualizados
- `goerp_payroll/version.py` - Versión actualizada a 1.0.0
- `CHANGELOG.md` - Historial de cambios del proyecto

### Características Principales
- Motor de nómina agnóstico a jurisdicción
- Motor de fórmulas con tablas de impuestos progresivos
- Gestión completa de vacaciones
- Control de acceso basado en roles (RBAC)
- Sistema de reportes personalizados
- Procesamiento en cola para nóminas grandes
- Internacionalización (i18n)

## Notas Técnicas
- Arquitectura limpia con separación de responsabilidades
- Evaluación segura de expresiones (patrón AST Visitor)
- Validación de esquemas en motor de fórmulas
- Todos los valores por defecto documentados como no-legales
