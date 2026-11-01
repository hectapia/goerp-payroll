# Data Governance and Audit System

## Overview

This document describes the comprehensive data governance and audit logging system implemented in GoERP Payroll to ensure compliance.

## Key Features

### 1. **Approval Workflow (Borrador/Aprobado)**

All critical payroll configuration entities support a two-state approval workflow:

- **Borrador (Draft)**: Initial state when created or after being edited
- **Aprobado (Approved)**: Approved state, ready for production use

#### Entities with Approval Workflow:
- ✅ **Percepciones** (Income/Perceptions)
- ✅ **Deducciones** (Deductions)
- ✅ **Prestaciones** (Benefits/Employer Contributions)
- ✅ **Reglas de Cálculo** (Calculation Rules)
- ✅ **Planillas** (Payroll Templates)

### 2. **Automatic Audit Logging**

Every change to critical entities is automatically logged with:
- **Who** made the change (usuario)
- **When** the change was made (timestamp)
- **What** was changed (field-level before/after values)
- **Why** (action type: created, updated, approved, rejected, etc.)

#### Audit Log Tables:
- `concepto_audit_log` - For Percepciones, Deducciones, Prestaciones
- `regla_calculo_audit_log` - For Calculation Rules
- `planilla_audit_log` - For Payroll Templates
- `nomina_audit_log` - For Payroll Executions

### 3. **Draft Status on Edit**

When an **approved** configuration is edited, it automatically returns to **draft** status, requiring re-approval. This ensures:
- No unauthorized changes go into production
- All changes are reviewed before use
- Complete audit trail of modifications

### 4. **Plugin Auto-Approval**

Configurations created by trusted plugins can be automatically approved:
- `creado_por_plugin` flag identifies plugin-created entities
- `plugin_source` stores the plugin identifier
- Auto-approved entities bypass manual approval workflow

### 5. **Validation Warnings for Draft Configurations**

When executing payroll with draft configurations:
- ⚠️ **Warnings are shown** but execution is **not blocked**
- Allows test runs with draft configurations
- Production runs should use only approved configurations
- Detailed list of draft items is provided

### 6. **Payroll Reproducibility (Snapshots)**

Every payroll execution (`Nomina`) stores complete snapshots:

```python
configuracion_snapshot     # Company configuration at calculation time
tipos_cambio_snapshot      # Exchange rates used
catalogos_snapshot         # Percepciones/Deducciones/Prestaciones formulas
fecha_calculo_original     # Original calculation date
es_recalculo              # Flag if this is a recalculation
nomina_original_id        # Reference to original if recalculated
```

This ensures:
- ✅ Calculations can be **exactly reproduced** months or years later
- ✅ Audit trail shows what configuration was used
- ✅ Compliance with financial regulations (SOX, COSO)

## Database Schema

### Governance Fields (All Configuration Entities)

```python
estado_aprobacion = Column(String(20), default="borrador", index=True)
aprobado_por = Column(String(150), nullable=True)
aprobado_en = Column(DateTime, nullable=True)
creado_por_plugin = Column(Boolean, default=False)
plugin_source = Column(String(200), nullable=True)
```

### Audit Log Structure

```python
# Common fields in all audit logs
accion = Column(String(50), index=True)  # created, updated, approved, rejected, etc.
usuario = Column(String(150), index=True)
descripcion = Column(String(1000))
cambios = Column(OrjsonType)  # JSON: {field: {old: value, new: value}}
estado_anterior = Column(String(20))
estado_nuevo = Column(String(20))
created_at = Column(DateTime, default=utc_now)  # From BaseTabla
```

## Usage Examples

### 1. Approving a Concept

```python
from goerp_payroll.audit_helpers import aprobar_concepto

# Approve a perception
success = aprobar_concepto(percepcion, usuario="admin@company.com")

# This will:
# - Change estado_aprobacion to "aprobado"
# - Set aprobado_por and aprobado_en
# - Create audit log entry
```

### 2. Editing an Approved Concept

```python
from goerp_payroll.audit_helpers import marcar_como_borrador_si_editado, detectar_cambios

# Detect changes
cambios = detectar_cambios(original_data, new_data)

# Update the concept
percepcion.nombre = "New Name"
percepcion.monto_default = 1500.00

# Mark as draft if it was approved
marcar_como_borrador_si_editado(percepcion, usuario="editor@company.com", cambios=cambios)

# This will:
# - Change estado_aprobacion back to "borrador"
# - Clear aprobado_por and aprobado_en
# - Create audit log entry with detailed changes
```

### 3. Validating Payroll Configuration

```python
from goerp_payroll.audit_helpers import validar_configuracion_nomina

# Before executing payroll
validacion = validar_configuracion_nomina(planilla_id)

if validacion["tiene_advertencias"]:
    for advertencia in validacion["advertencias"]:
        flash(advertencia, "warning")
    
    # Show confirmation dialog:
    # "⚠️ Hay configuraciones en BORRADOR. ¿Desea continuar con la ejecución de prueba?"
```

### 4. Creating Plugin-Generated Configuration

```python
# When a plugin creates a configuration
percepcion = Percepcion(
    codigo="PLUGIN_BONUS",
    nombre="Plugin-Generated Bonus",
    creado_por_plugin=True,
    plugin_source="payroll_plugin_v1.0",
    estado_aprobacion="aprobado",  # Auto-approved
    creado_por="plugin@system"
)
```

### 5. Viewing Audit History

```python
# Get all audit logs for a concept
logs = percepcion.audit_logs.order_by(ConceptoAuditLog.created_at.desc()).all()

for log in logs:
    print(f"{log.created_at}: {log.usuario} - {log.accion}")
    print(f"  {log.descripcion}")
    if log.cambios:
        for campo, valores in log.cambios.items():
            print(f"    {campo}: {valores['old']} → {valores['new']}")
```

## Human-Readable Audit Messages

The system generates human-readable audit descriptions like:

```
✅ Usted creó percepción 'Salario Base' (código: SAL_BASE) – 2 hours ago

✅ Usted cambió de valor de Monto Default de 1000.00 a 1500.00, 
   Nombre de "Salario" a "Salario Base" – 1 hour ago

⚠️ Usted editó percepción 'Salario Base' - Monto Default cambió de 1500.00 a 2000.00. 
   Estado cambiado a borrador. – 30 minutes ago

✅ admin@company.com aprobó percepción 'Salario Base' (código: SAL_BASE) – 10 minutes ago
```

## Compliance Benefits

- ✅ Complete audit trail of all financial configuration changes
- ✅ Separation of duties (creator vs approver)
- ✅ Reproducible calculations with snapshots
- ✅ Immutable audit logs (append-only)
- ✅ Control Environment: Approval workflow
- ✅ Risk Assessment: Validation warnings
- ✅ Control Activities: Automatic draft marking on edit
- ✅ Information & Communication: Detailed audit logs
- ✅ Monitoring: Audit trail review capabilities

## Implementation Sizes

### Small Implementations
- Same user can create and approve
- Simplified workflow for small teams
- All governance features still active

### Large Implementations
- Separate creator and approver roles
- Enforced separation of duties

## API Functions

### Concept Management
```python
# From goerp_payroll.audit_helpers

aprobar_concepto(concepto, usuario) -> bool
rechazar_concepto(concepto, usuario, razon=None) -> bool
marcar_como_borrador_si_editado(concepto, usuario, cambios) -> None
crear_log_auditoria(concepto, accion, usuario, ...) -> ConceptoAuditLog
```

### Calculation Rule Management
```python
aprobar_regla_calculo(regla, usuario) -> bool
rechazar_regla_calculo(regla, usuario, razon=None) -> bool
marcar_regla_calculo_como_borrador_si_editada(regla, usuario, cambios) -> None
crear_log_auditoria_regla_calculo(regla, accion, usuario, ...) -> ReglaCalculoAuditLog
```

### Planilla Management
```python
aprobar_planilla(planilla, usuario) -> bool
rechazar_planilla(planilla, usuario, razon=None) -> bool
marcar_planilla_como_borrador_si_editada(planilla, usuario, cambios) -> None
crear_log_auditoria_planilla(planilla, accion, usuario, ...) -> PlanillaAuditLog
```

### Nomina Management
```python
aprobar_nomina(nomina, usuario) -> bool
aplicar_nomina(nomina, usuario) -> bool
anular_nomina(nomina, usuario, razon) -> bool
crear_log_auditoria_nomina(nomina, accion, usuario, ...) -> NominaAuditLog
```

### Validation
```python
validar_configuracion_nomina(planilla_id) -> Dict[str, Any]
obtener_conceptos_en_borrador(planilla_id) -> Dict[str, list]
obtener_reglas_calculo_en_borrador(planilla_id) -> list
tiene_conceptos_en_borrador(planilla_id) -> bool
```

## Testing

Unit tests are provided in:
- `tests/test_audit_helpers.py` - Audit logging functions
- `tests/test_governance_workflow.py` - Approval workflows
- `tests/test_nomina_snapshots.py` - Payroll reproducibility
