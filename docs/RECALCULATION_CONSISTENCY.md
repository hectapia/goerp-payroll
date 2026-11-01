# Sistema de Consistencia en Recálculo de Nóminas

## Resumen

Este documento describe el sistema implementado para garantizar que las nóminas sean recalculables de forma consistente, preservando el contexto de cálculo original.

## Problema

Anteriormente, el sistema no garantizaba que una nómina recalculada produjera los mismos resultados que la nómina original debido a:

1. **Datos externos mutables**: Configuraciones, fórmulas, tipos de cambio podían cambiar
2. **Fecha de cálculo variable**: Se usaba `date.today()` al recalcular, afectando antigüedad y acumulados
3. **Sin versionado**: No se guardaban snapshots de configuraciones usadas
4. **Variables dinámicas**: Cálculos temporales dependían de la fecha actual

## Solución Implementada

### 1. Campos de Snapshot en Modelo Nomina

Se agregaron los siguientes campos a la tabla `nomina`:

```python
fecha_calculo_original: date          # Fecha de cálculo original
configuracion_snapshot: JSON          # Configuración de empresa
tipos_cambio_snapshot: JSON           # Tipos de cambio usados
catalogos_snapshot: JSON              # Percepciones/Deducciones/Prestaciones
es_recalculo: bool                    # Flag de recálculo
nomina_original_id: str               # Referencia a nómina original
```

### 2. Servicio de Captura de Snapshots

**Archivo**: `goerp_payroll/nomina_engine/services/snapshot_service.py`

El `SnapshotService` captura snapshots inmutables de:

- **Configuración de empresa**: Días/mes, días/año, tasas de interés, etc.
- **Tipos de cambio**: Tasas de conversión para todas las monedas usadas
- **Catálogos**: Fórmulas completas de percepciones, deducciones y prestaciones

```python
snapshot = snapshot_service.capture_complete_snapshot(planilla, periodo_inicio, periodo_fin, fecha_calculo)
```

### 3. Integración en Ejecución de Nómina

**Archivo**: `goerp_payroll/nomina_engine/services/payroll_execution_service.py`

Al ejecutar una nómina, se capturan automáticamente todos los snapshots:

```python
# Capture configuration snapshots for recalculation consistency
snapshot = self.snapshot_service.capture_complete_snapshot(planilla, periodo_inicio, periodo_fin, fecha_calculo)

nomina = Nomina(
    # ... otros campos ...
    fecha_calculo_original=fecha_calculo,
    configuracion_snapshot=snapshot["configuracion"],
    tipos_cambio_snapshot=snapshot["tipos_cambio"],
    catalogos_snapshot=snapshot["catalogos"],
)
```

> Nota: el snapshot de vacaciones se almacena en `snapshot["vacaciones"]` y se replica en
> `snapshot["catalogos"]["vacaciones"]` solo para inspección/exportación; el motor usa la
> clave `snapshot["vacaciones"]` como fuente de verdad en recálculos.

### 4. Lógica de Recálculo Consistente

**Archivo**: `goerp_payroll/vistas/planilla/services/nomina_service.py`

Al recalcular, se preserva la fecha de cálculo original:

```python
# Usar fecha_calculo_original en lugar de date.today()
fecha_calculo_original = nomina.fecha_calculo_original or nomina.fecha_generacion.date()

engine = NominaEngine(
    planilla=planilla,
    periodo_inicio=periodo_inicio,
    periodo_fin=periodo_fin,
    fecha_calculo=fecha_calculo_original,  # ← Fecha original
    usuario=usuario,
)
```

### 5. Auditoría de Recálculos

Cada recálculo genera un registro de auditoría:

```python
crear_log_auditoria_nomina(
    nomina=new_nomina,
    accion="recalculated",
    usuario=usuario,
    descripcion=f"Nómina recalculada desde nómina original {nomina_original_id}",
    cambios={
        "nomina_original_id": nomina_original_id,
        "fecha_calculo_original": fecha_calculo_original.isoformat(),
        "periodo_inicio": periodo_inicio.isoformat(),
        "periodo_fin": periodo_fin.isoformat(),
    },
)
```

## Garantías de Consistencia

Con esta implementación, el sistema garantiza:

### ✅ Fecha de Cálculo Consistente
- Se preserva `fecha_calculo_original` al recalcular
- Antigüedad del empleado se calcula igual
- Acumulados se obtienen de la misma fecha

### ✅ Configuración Inmutable
- Snapshot de configuración de empresa
- Días/mes, días/año, tasas de interés preservadas
- Métodos de cálculo de interés inmutables

### ✅ Tipos de Cambio Preservados
- Tasas de conversión guardadas por moneda
- Fecha de vigencia del tipo de cambio registrada
- Conversiones consistentes en recálculo

### ✅ Catálogos Versionados
- Fórmulas de percepciones preservadas
- Fórmulas de deducciones preservadas
- Fórmulas de prestaciones preservadas
- Porcentajes y montos fijos inmutables

### ✅ Trazabilidad Completa
- Flag `es_recalculo` identifica recálculos
- `nomina_original_id` vincula con nómina original
- Audit log registra cada recálculo
- Snapshots permiten auditoría histórica

## Uso

### Recalcular una Nómina

```python
from goerp_payroll.vistas.planilla.services.nomina_service import NominaService

# Recalcular nómina (usa automáticamente fecha_calculo_original)
new_nomina, errors, warnings = NominaService.recalcular_nomina(
    nomina=nomina_existente,
    planilla=planilla,
    usuario="admin"
)

# Verificar si es recálculo
if new_nomina.es_recalculo:
    print(f"Recalculada desde: {new_nomina.nomina_original_id}")
    print(f"Fecha cálculo original: {new_nomina.fecha_calculo_original}")
```

### Consultar Snapshots

```python
# Ver configuración usada en el cálculo
config_snapshot = nomina.configuracion_snapshot
print(f"Días/mes: {config_snapshot['dias_mes']}")
print(f"Salario mínimo: {config_snapshot['salario_minimo']}")

# Ver tipos de cambio usados
tipos_cambio = nomina.tipos_cambio_snapshot
for moneda_id, data in tipos_cambio.items():
    print(f"Moneda {moneda_id}: Tasa {data['tasa']}")

# Ver catálogos usados
catalogos = nomina.catalogos_snapshot
for percepcion in catalogos['percepciones']:
    print(f"{percepcion['codigo']}: {percepcion['formula']}")
```

### Auditar Recálculos

```python
# Obtener historial de recálculos
audit_logs = nomina.audit_logs.filter_by(accion="recalculated").all()
for log in audit_logs:
    print(f"{log.timestamp}: {log.descripcion} por {log.usuario}")
```

## Restricciones

### Nóminas No Recalculables

Las siguientes nóminas **NO** pueden ser recalculadas:

- ❌ Nóminas en estado `aplicado` (pagadas)
- ❌ Nóminas en estado `pagado`

```python
if nomina.estado == "aplicado":
    raise ValueError("No se puede recalcular una nómina aplicada")
```

### Datos que Sí Cambian en Recálculo

Algunos datos **sí** se actualizan al recalcular:

- ✅ **Novedades del período**: Se cargan las novedades actuales
- ✅ **Datos del empleado**: Salario actual, cargo, área (se guarda snapshot en NominaEmpleado)
- ✅ **Préstamos/Adelantos**: Saldos actuales al momento del recálculo
- ✅ **Acumulados anuales**: Valores actuales de acumulados

Esto es intencional para permitir correcciones de novedades y ajustes de datos del empleado.

## Beneficios

1. **Reproducibilidad**: Resultados consistentes en recálculos
2. **Auditoría**: Trazabilidad completa de cambios
3. **Transparencia**: Snapshots visibles para auditoría
4. **Confiabilidad**: Elimina sorpresas en recálculos
5. **Cumplimiento**: Facilita auditorías legales y fiscales

## Consideraciones de Rendimiento

- Los snapshots JSON agregan ~10-50 KB por nómina
- Captura de snapshots agrega ~100-200ms al tiempo de ejecución
- Índices en `es_recalculo` y `nomina_original_id` optimizan consultas

## Futuras Mejoras

1. **Modo de recálculo con datos actuales**: Flag para recalcular con configuración actual
2. **Comparación de resultados**: Herramienta para comparar nómina original vs recalculada
3. **Validación de consistencia**: Alertas si recálculo difiere significativamente
4. **Compresión de snapshots**: Reducir tamaño de JSON almacenado
5. **Snapshot de novedades**: Opción para preservar novedades originales

## Referencias

- **Modelo**: `goerp_payroll/model.py` - Clase `Nomina`
- **Servicio de Snapshots**: `goerp_payroll/nomina_engine/services/snapshot_service.py`
- **Ejecución de Nómina**: `goerp_payroll/nomina_engine/services/payroll_execution_service.py`
- **Recálculo**: `goerp_payroll/vistas/planilla/services/nomina_service.py`
- **Auditoría**: `goerp_payroll/audit_helpers.py`
- **Migración**: `migrations/add_nomina_recalculation_snapshots.sql`

## Soporte

Para preguntas o problemas relacionados con el sistema de recálculo consistente, consultar:
- Documentación de auditoría: `docs/AUDIT_GOVERNANCE_SYSTEM.md`
- Sistema de nóminas: `docs/guia/nominas.md`
