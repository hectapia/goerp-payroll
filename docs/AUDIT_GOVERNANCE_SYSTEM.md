# Sistema de Auditoría y Gobernanza para el Sistema de Nómina

## Descripción General

Este documento describe el sistema de auditoría y gobernanza implementado para todo el sistema de nómina GoERP Payroll, incluyendo:
- **Conceptos de nómina**: Percepciones, Deducciones y Prestaciones
- **Planillas**: Configuraciones de nómina
- **Nóminas**: Ejecuciones y resultados de nómina

## Objetivos

El sistema garantiza que:

1. **Trazabilidad completa**: Todos los cambios a conceptos de nómina son registrados con información de quién, cuándo y qué cambió.
2. **Flujo de aprobación**: Los conceptos deben pasar por un proceso de revisión antes de ser utilizados en producción.
3. **Flexibilidad**: Permite corridas de prueba con conceptos en borrador mientras advierte claramente sobre su estado.
4. **Segregación de funciones**: En implementaciones grandes, un usuario crea y otro valida.
5. **Compatibilidad con plugins**: Los conceptos creados por plugins pueden ser pre-aprobados.

## Estados de Aprobación

Los conceptos de nómina (percepciones, deducciones, prestaciones) pueden estar en dos estados:

### Borrador (`borrador`)
- Estado inicial al crear un nuevo concepto
- Requiere aprobación antes de uso en producción
- Puede usarse en corridas de prueba (con advertencias)
- Si un concepto aprobado es editado, vuelve a borrador automáticamente

### Aprobado (`aprobado`)
- Concepto validado y listo para uso en producción
- Solo usuarios con rol ADMIN o HHRR pueden aprobar
- Se registra quién aprobó y cuándo
- No genera advertencias en corridas de nómina

## Roles y Permisos

### Usuarios que pueden aprobar conceptos:
- **ADMIN**: Administradores del sistema
- **HHRR**: Personal de Recursos Humanos

### Usuarios que pueden crear/editar conceptos:
- **ADMIN**: Administradores del sistema
- **HHRR**: Personal de Recursos Humanos

### Nota sobre implementaciones
- **Implementaciones pequeñas**: Un mismo usuario puede crear y aprobar conceptos
- **Implementaciones grandes**: Se recomienda segregación de funciones (un usuario crea, otro aprueba)

## Flujo de Trabajo

### 1. Creación de Concepto

```
Usuario crea concepto → Estado: BORRADOR → Se registra en audit log
```

**Campos registrados**:
- `creado_por`: Usuario que creó el concepto
- `estado_aprobacion`: "borrador"
- Audit log con acción "created"

### 2. Edición de Concepto

**Si el concepto está en BORRADOR**:
```
Usuario edita → Permanece en BORRADOR → Se registra cambio en audit log
```

**Si el concepto está APROBADO**:
```
Usuario edita → Vuelve a BORRADOR → Se registra cambio y cambio de estado
```

**Excepción**: Conceptos creados por plugins no cambian de estado al editarse.

### 3. Aprobación de Concepto

```
Usuario ADMIN/HHRR aprueba → Estado: APROBADO → Se registra aprobación
```

**Campos actualizados**:
- `estado_aprobacion`: "aprobado"
- `aprobado_por`: Usuario que aprobó
- `aprobado_en`: Fecha y hora de aprobación
- Audit log con acción "approved"

### 4. Rechazo de Concepto

```
Usuario ADMIN/HHRR rechaza → Estado: BORRADOR → Se registra rechazo
```

Útil para devolver un concepto aprobado a borrador con una razón documentada.

## Corridas de Nómina con Conceptos en Borrador

### Comportamiento

El sistema **permite** corridas de nómina con conceptos en borrador porque:
- Es necesario hacer corridas de prueba para validar cálculos
- Los usuarios necesitan ver resultados antes de aprobar definitivamente

### Advertencias Mostradas

Cuando se ejecuta una nómina con conceptos en borrador, el sistema muestra:

```
⚠️ ADVERTENCIA: 2 percepción(es) en estado BORRADOR: Horas Extra, Comisiones. 
Valide cuidadosamente los resultados de la nómina.

⚠️ ADVERTENCIA: 1 deducción(es) en estado BORRADOR: Préstamo Personal. 
Valide cuidadosamente los resultados de la nómina.
```

### Sin Advertencias

Si **todos** los conceptos están aprobados, no se muestran mensajes de alerta.

## Conceptos Creados por Plugins

### Comportamiento Especial

Los conceptos creados por plugins tienen un tratamiento especial:

**Campos**:
- `creado_por_plugin`: `true`
- `plugin_source`: Nombre del plugin que lo creó
- `estado_aprobacion`: "aprobado" (directamente)

**Razón**: Se asume que el mantenedor del plugin ha realizado validaciones rigurosas.

**Ventajas**:
- No requieren aprobación manual
- No vuelven a borrador al editarse
- Facilitan la integración de plugins de terceros

### Ejemplo de Creación por Plugin

```python
from goerp_payroll.model import Percepcion, db
from goerp_payroll.enums import EstadoAprobacion

# Crear percepción desde plugin
percepcion = Percepcion()
percepcion.codigo = "PLUGIN_BONUS"
percepcion.nombre = "Bono Especial Plugin"
percepcion.estado_aprobacion = EstadoAprobacion.APROBADO
percepcion.creado_por_plugin = True
percepcion.plugin_source = "mi_plugin_nomina"
percepcion.aprobado_por = "plugin:mi_plugin_nomina"
percepcion.aprobado_en = utc_now()

db.session.add(percepcion)
db.session.commit()
```

## Registro de Auditoría (Audit Log)

### Información Registrada

Cada cambio a un concepto genera una entrada en `concepto_audit_log` con:

| Campo | Descripción |
|-------|-------------|
| `timestamp` | Fecha y hora del cambio |
| `usuario` | Usuario que realizó el cambio |
| `accion` | Tipo de acción (created, updated, approved, rejected) |
| `descripcion` | Descripción legible del cambio |
| `cambios` | JSON con detalles campo por campo |
| `estado_anterior` | Estado de aprobación previo |
| `estado_nuevo` | Nuevo estado de aprobación |

### Ejemplo de Registro

```json
{
  "timestamp": "2025-01-15 10:30:45",
  "usuario": "jperez",
  "accion": "updated",
  "descripcion": "Editó percepcion 'Horas Extra' - Monto Default cambió de 0.00 a 15.50. Estado cambiado a borrador.",
  "cambios": {
    "monto_default": {
      "old": "0.00",
      "new": "15.50"
    }
  },
  "estado_anterior": "aprobado",
  "estado_nuevo": "borrador"
}
```

### Visualización del Historial

Los usuarios pueden ver el historial completo de auditoría:
- Ruta: `/percepciones/audit/<id>`, `/deducciones/audit/<id>`, `/prestaciones/audit/<id>`
- Muestra todos los cambios en orden cronológico inverso
- Incluye detalles expandibles de cada cambio

## Modelo de Datos

### Campos Agregados a Percepcion, Deduccion, Prestacion

```python
# Estado de aprobación
estado_aprobacion = Column(String(20), default="borrador", index=True)

# Información de aprobación
aprobado_por = Column(String(150), nullable=True)
aprobado_en = Column(DateTime, nullable=True)

# Información de plugins
creado_por_plugin = Column(Boolean, default=False)
plugin_source = Column(String(200), nullable=True)

# Relación con audit logs
audit_logs = relationship("ConceptoAuditLog", ...)
```

### Tabla ConceptoAuditLog

```python
class ConceptoAuditLog(Model):
    # Foreign keys (solo uno estará poblado)
    percepcion_id = Column(String(26), ForeignKey("percepcion.id"))
    deduccion_id = Column(String(26), ForeignKey("deduccion.id"))
    prestacion_id = Column(String(26), ForeignKey("prestacion.id"))
    
    # Tipo y acción
    tipo_concepto = Column(String(20))  # percepcion|deduccion|prestacion
    accion = Column(String(50))  # created|updated|approved|rejected
    
    # Usuario y descripción
    usuario = Column(String(150))
    descripcion = Column(String(1000))
    
    # Cambios detallados
    cambios = Column(JSONB)
    
    # Estados
    estado_anterior = Column(String(20))
    estado_nuevo = Column(String(20))
```

## API de Funciones Helper

### `puede_aprobar_concepto(usuario_tipo: str) -> bool`
Verifica si un usuario puede aprobar conceptos.

### `aprobar_concepto(concepto, usuario: str) -> bool`
Aprueba un concepto y registra la acción.

### `rechazar_concepto(concepto, usuario: str, razon: str) -> bool`
Rechaza un concepto (lo marca como borrador) con una razón.

### `marcar_como_borrador_si_editado(concepto, usuario: str, cambios: dict)`
Marca un concepto como borrador si fue editado mientras estaba aprobado.

### `obtener_conceptos_en_borrador(planilla_id: str) -> dict`
Obtiene todos los conceptos en borrador asociados a una planilla.

### `crear_log_auditoria(...)`
Crea una entrada en el registro de auditoría.

## Rutas HTTP

### Aprobación
- `POST /percepciones/approve/<id>` - Aprobar percepción
- `POST /deducciones/approve/<id>` - Aprobar deducción
- `POST /prestaciones/approve/<id>` - Aprobar prestación

### Rechazo
- `POST /percepciones/reject/<id>` - Rechazar percepción
- `POST /deducciones/reject/<id>` - Rechazar deducción
- `POST /prestaciones/reject/<id>` - Rechazar prestación

### Historial de Auditoría
- `GET /percepciones/audit/<id>` - Ver historial de percepción
- `GET /deducciones/audit/<id>` - Ver historial de deducción
- `GET /prestaciones/audit/<id>` - Ver historial de prestación

## Migración de Datos Existentes

El sistema utiliza las migraciones automáticas de SQLAlchemy/Alembic. Los nuevos campos se agregarán automáticamente cuando:

1. Se ejecute `db.create_all()` en una base de datos nueva
2. Se genere y aplique una migración de Alembic en bases de datos existentes

### Para bases de datos existentes

Los conceptos existentes tendrán `estado_aprobacion = 'borrador'` por defecto. Se recomienda:

1. Ejecutar un script para marcar conceptos existentes como aprobados:

```python
from goerp_payroll.model import Percepcion, Deduccion, Prestacion, db, utc_now
from goerp_payroll.enums import EstadoAprobacion

# Aprobar todos los conceptos existentes (compatibilidad hacia atrás)
for model in [Percepcion, Deduccion, Prestacion]:
    conceptos = db.session.query(model).filter_by(estado_aprobacion='borrador').all()
    for concepto in conceptos:
        concepto.estado_aprobacion = EstadoAprobacion.APROBADO
        concepto.aprobado_por = 'system'
        concepto.aprobado_en = utc_now()

db.session.commit()
```

2. O usar Alembic para generar la migración automáticamente:

```bash
# Generar migración
alembic revision --autogenerate -m "Add audit and governance fields"

# Aplicar migración
alembic upgrade head
```

## Mejores Prácticas

### Para Implementaciones Pequeñas
1. Un usuario puede crear y aprobar sus propios conceptos
2. Revisar el historial de auditoría periódicamente
3. Aprobar conceptos después de probarlos en nóminas de prueba

### Para Implementaciones Grandes
1. **Segregación de funciones**: Usuario A crea, Usuario B aprueba
2. Establecer un proceso formal de revisión
3. Documentar razones de rechazo
4. Revisar audit logs en auditorías internas

### Para Desarrolladores de Plugins
1. Marcar conceptos como `creado_por_plugin=True`
2. Establecer `plugin_source` con el nombre del plugin
3. Crear conceptos directamente en estado `aprobado`
4. Documentar validaciones realizadas

## Ejemplo de Uso Completo

### Escenario: Crear y Aprobar una Nueva Percepción

```python
from flask_login import current_user
from goerp_payroll.model import Percepcion, db
from goerp_payroll.audit_helpers import aprobar_concepto, crear_log_auditoria
from goerp_payroll.enums import EstadoAprobacion

# 1. Usuario HHRR crea percepción
percepcion = Percepcion()
percepcion.codigo = "BONO_ANUAL"
percepcion.nombre = "Bono Anual"
percepcion.monto_default = 1000.00
percepcion.estado_aprobacion = EstadoAprobacion.BORRADOR
percepcion.creado_por = current_user.usuario

db.session.add(percepcion)
db.session.flush()

# Crear audit log
crear_log_auditoria(
    concepto=percepcion,
    accion="created",
    usuario=current_user.usuario,
    descripcion=f"Creó percepcion '{percepcion.nombre}'",
    estado_nuevo=EstadoAprobacion.BORRADOR
)

db.session.commit()

# 2. Probar en nómina (con advertencias)
# ... ejecutar nómina de prueba ...

# 3. Usuario ADMIN aprueba
if aprobar_concepto(percepcion, "admin_user"):
    db.session.commit()
    print("Percepción aprobada exitosamente")
```

## Soporte y Mantenimiento

Para preguntas o problemas con el sistema de auditoría:
- Revisar logs en `concepto_audit_log`
- Verificar permisos de usuario
- Consultar este documento

## Sistema de Auditoría para Planillas

### Estados de Aprobación en Planillas

Las planillas también utilizan el sistema de estados borrador/aprobado:

- **Borrador**: Planilla en configuración, puede ser modificada
- **Aprobado**: Planilla validada y lista para ejecutar nóminas

### Flujo de Trabajo para Planillas

1. **Creación**: Planilla se crea en estado borrador
2. **Configuración**: Se agregan empleados, percepciones, deducciones, prestaciones
3. **Pruebas**: Se ejecutan nóminas de prueba (con advertencias si hay conceptos en borrador)
4. **Aprobación**: Usuario ADMIN/HHRR aprueba la planilla
5. **Edición**: Si se edita una planilla aprobada, vuelve a borrador

### Audit Log de Planillas

Se registran todas las acciones:
- Creación y modificación de planilla
- Aprobación/rechazo
- Adición/remoción de empleados
- Adición/remoción de conceptos (percepciones, deducciones, prestaciones)
- Cambios en configuración

### Funciones Helper para Planillas

```python
from goerp_payroll.audit_helpers import (
    aprobar_planilla,
    rechazar_planilla,
    crear_log_auditoria_planilla,
    marcar_planilla_como_borrador_si_editada
)

# Aprobar planilla
if aprobar_planilla(planilla, current_user.usuario):
    db.session.commit()
    
# Rechazar planilla
rechazar_planilla(planilla, current_user.usuario, "Falta configurar INSS")
db.session.commit()
```

## Sistema de Auditoría para Nóminas

### Estados de Nómina

Las nóminas tienen un flujo de estados más complejo:

1. **Calculando**: Nómina en proceso de cálculo
2. **Generado**: Cálculo completado, pendiente de revisión
3. **Aprobado**: Revisada y aprobada por ADMIN/HHRR
4. **Aplicado**: Ejecutada y pagada a empleados
5. **Anulado**: Cancelada (con razón documentada)
6. **Error**: Error durante el cálculo

### Transiciones de Estado

```
Calculando → Generado → Aprobado → Aplicado
                ↓           ↓          ↓
              Anulado    Anulado    Anulado
```

### Campos de Auditoría en Nómina

```python
# Aprobación
aprobado_por: str
aprobado_en: datetime

# Aplicación
aplicado_por: str
aplicado_en: datetime

# Anulación
anulado_por: str
anulado_en: datetime
razon_anulacion: str
```

### Audit Log de Nóminas

Se registran todas las transiciones de estado:
- Generación de nómina
- Aprobación
- Aplicación/pago
- Anulación (con razón)
- Recálculos
- Modificaciones manuales

### Funciones Helper para Nóminas

```python
from goerp_payroll.audit_helpers import (
    aprobar_nomina,
    aplicar_nomina,
    anular_nomina,
    crear_log_auditoria_nomina
)

# Aprobar nómina
if aprobar_nomina(nomina, current_user.usuario):
    db.session.commit()
    flash("Nómina aprobada exitosamente")

# Aplicar nómina (marcar como pagada)
if aplicar_nomina(nomina, current_user.usuario):
    db.session.commit()
    flash("Nómina aplicada exitosamente")

# Anular nómina
if anular_nomina(nomina, current_user.usuario, "Error en cálculo de INSS"):
    db.session.commit()
    flash("Nómina anulada")
```

### Ejemplo Completo: Flujo de Nómina con Auditoría

```python
from goerp_payroll.nomina_engine import ejecutar_nomina
from goerp_payroll.audit_helpers import aprobar_nomina, aplicar_nomina

# 1. Generar nómina (automáticamente crea audit log)
nomina, errores, advertencias = ejecutar_nomina(
    planilla_id="01HXXX",
    periodo_inicio=date(2025, 1, 1),
    periodo_fin=date(2025, 1, 15),
    usuario=current_user.usuario
)

# 2. Revisar resultados y aprobar
if nomina and not errores:
    if aprobar_nomina(nomina, current_user.usuario):
        db.session.commit()
        
    # 3. Aplicar (marcar como pagada)
    if aplicar_nomina(nomina, current_user.usuario):
        db.session.commit()
```

## Tablas de Audit Log

### ConceptoAuditLog
Registra cambios en Percepcion, Deduccion, Prestacion

### PlanillaAuditLog
Registra cambios en Planilla y su configuración

### NominaAuditLog
Registra transiciones de estado y modificaciones en Nomina

## Changelog

- **2025-01-15**: Implementación inicial del sistema de auditoría y gobernanza
  - Estados borrador/aprobado para conceptos y planillas
  - Registro de auditoría completo para conceptos, planillas y nóminas
  - Soporte para plugins
  - Advertencias en corridas de nómina
  - Tracking completo de transiciones de estado en nóminas
