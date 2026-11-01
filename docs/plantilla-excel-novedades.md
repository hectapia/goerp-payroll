# Plantilla Excel para Importación de Novedades

## Descripción

Este documento especifica la estructura de la plantilla Excel para importar novedades (novelties) de nómina de forma masiva, incluyendo soporte para novedades de vacaciones.

## Estructura de la Plantilla

### Hoja 1: Novedades

La plantilla debe contener las siguientes columnas en orden:

| Columna | Nombre del Campo | Tipo | Requerido | Descripción | Ejemplo |
|---------|------------------|------|-----------|-------------|---------|
| A | `codigo_empleado` | Texto | Sí | Código único del empleado | `EMP-ABC123` |
| B | `tipo_concepto` | Texto | Sí | Tipo de concepto: `percepcion` o `deduccion` | `percepcion` |
| C | `codigo_concepto` | Texto | Sí | Código del concepto que se aplica | `BONO_PROD` |
| D | `tipo_valor` | Texto | Sí | Tipo de valor: `monto`, `horas`, `dias`, `cantidad`, `porcentaje` | `dias` |
| E | `valor_cantidad` | Numérico | Sí | **CRÍTICO**: Días/horas a DESCONTAR del saldo (puede diferir de días calendario) | `2.00` |
| F | `fecha_novedad` | Fecha | No | Fecha en que ocurrió el evento (formato: DD/MM/YYYY) | `15/01/2025` |
| G | `es_inasistencia` | Booleano | No | Marca la novedad como inasistencia: `SI`, `NO`, `1`, `0`, `TRUE`, `FALSE` | `SI` |
| H | `descontar_pago_inasistencia` | Booleano | No | Indica si la inasistencia descuenta salario: `SI`, `NO`, `1`, `0`, `TRUE`, `FALSE` | `SI` |
| I | `es_descanso_vacaciones` | Booleano | No | Si es novedad de vacaciones: `SI`, `NO`, `1`, `0`, `TRUE`, `FALSE` | `SI` |
| J | `fecha_inicio_descanso` | Fecha | No | Fecha de inicio del período de descanso (calendario) (formato: DD/MM/YYYY) | `20/01/2025` |
| K | `fecha_fin_descanso` | Fecha | No | Fecha de fin del período de descanso (calendario) (formato: DD/MM/YYYY) | `24/01/2025` |

### Notas Importantes

1. **Encabezados**: La primera fila debe contener los nombres de las columnas exactamente como se especifican arriba.

2. **Código de Empleado**: Debe coincidir exactamente con el código del empleado en el sistema.

3. **Tipo de Concepto**: 
   - `percepcion`: Para ingresos adicionales (bonos, comisiones, horas extras)
   - `deduccion`: Para descuentos (ausencias, préstamos)

4. **Tipo de Valor**: Debe ser uno de los valores especificados. Determina cómo se interpreta el campo `valor_cantidad`.

5. **Inasistencias**: Si `es_inasistencia` es `SI`/`TRUE`/`1` y `descontar_pago_inasistencia` es `SI`, el descuento se calcula con la configuración de días/horas de la empresa.

6. **Vacaciones**: Si `es_descanso_vacaciones` es `SI`/`TRUE`/`1`, entonces:
   - Las fechas de inicio y fin del descanso son obligatorias
   - El sistema verificará que el empleado tenga saldo suficiente de vacaciones
   - Se creará automáticamente una entrada en el módulo de vacaciones
   - El balance de vacaciones del empleado se reducirá al aprobar y ejecutar la nómina

7. **Validaciones**:
   - El empleado debe existir en el sistema
   - El concepto (percepción o deducción) debe existir y estar activo
   - Si es vacación, el empleado debe tener una cuenta de vacaciones activa
   - Las fechas deben ser válidas y estar en el formato correcto

## Ejemplo de Plantilla

### Ejemplo 1: Bono sin vacaciones

| codigo_empleado | tipo_concepto | codigo_concepto | tipo_valor | valor_cantidad | fecha_novedad | es_inasistencia | descontar_pago_inasistencia | es_descanso_vacaciones | fecha_inicio_descanso | fecha_fin_descanso |
|-----------------|---------------|-----------------|------------|----------------|---------------|-----------------|----------------------------|------------------------|----------------------|-------------------|
| EMP-ABC123 | percepcion | BONO_PROD | monto | 1500.00 | 15/01/2025 | NO | NO | NO | | |
| EMP-DEF456 | percepcion | COMISION | monto | 2000.00 | 15/01/2025 | NO | NO | NO | | |

### Ejemplo 2: Horas extras sin vacaciones

| codigo_empleado | tipo_concepto | codigo_concepto | tipo_valor | valor_cantidad | fecha_novedad | es_inasistencia | descontar_pago_inasistencia | es_descanso_vacaciones | fecha_inicio_descanso | fecha_fin_descanso |
|-----------------|---------------|-----------------|------------|----------------|---------------|-----------------|----------------------------|------------------------|----------------------|-------------------|
| EMP-ABC123 | percepcion | HORAS_EXTRA | horas | 10.00 | 10/01/2025 | NO | NO | NO | | |

### Ejemplo 3: Vacaciones

| codigo_empleado | tipo_concepto | codigo_concepto | tipo_valor | valor_cantidad | fecha_novedad | es_inasistencia | descontar_pago_inasistencia | es_descanso_vacaciones | fecha_inicio_descanso | fecha_fin_descanso |
|-----------------|---------------|-----------------|------------|----------------|---------------|-----------------|----------------------------|------------------------|----------------------|-------------------|
| EMP-ABC123 | deduccion | AUSENCIA | dias | 5.00 | 20/01/2025 | SI | SI | SI | 20/01/2025 | 24/01/2025 |
| EMP-DEF456 | deduccion | AUSENCIA | dias | 3.00 | 15/01/2025 | SI | SI | SI | 15/01/2025 | 17/01/2025 |

### Ejemplo 4: Mixto (bonos y vacaciones)

| codigo_empleado | tipo_concepto | codigo_concepto | tipo_valor | valor_cantidad | fecha_novedad | es_inasistencia | descontar_pago_inasistencia | es_descanso_vacaciones | fecha_inicio_descanso | fecha_fin_descanso |
|-----------------|---------------|-----------------|------------|----------------|---------------|-----------------|----------------------------|------------------------|----------------------|-------------------|
| EMP-ABC123 | percepcion | BONO_PROD | monto | 1500.00 | 15/01/2025 | NO | NO | NO | | |
| EMP-ABC123 | deduccion | AUSENCIA | dias | 5.00 | 20/01/2025 | SI | SI | SI | 20/01/2025 | 24/01/2025 |
| EMP-DEF456 | percepcion | COMISION | monto | 2000.00 | 15/01/2025 | NO | NO | NO | | |

## Flujo de Procesamiento

1. **Carga del Archivo**: El usuario carga el archivo Excel en el sistema
2. **Validación**: El sistema valida cada fila:
   - Verifica que el empleado exista
   - Verifica que el concepto exista
   - Si es vacación, verifica que tenga cuenta de vacaciones activa
   - Valida formatos de fecha y valores numéricos
3. **Importación**: Si todas las validaciones pasan, se crean las novedades
4. **Vinculación con Vacaciones**: 
   - Si `es_descanso_vacaciones = SI`, se crea automáticamente una solicitud de vacaciones
   - La solicitud queda en estado "pendiente" hasta aprobación
5. **Procesamiento en Nómina**: 
   - Al ejecutar la nómina, las vacaciones aprobadas reducen el balance
   - Se crean entradas en el libro mayor de vacaciones

## Códigos de Error Comunes

| Código | Descripción | Solución |
|--------|-------------|----------|
| `E001` | Empleado no encontrado | Verificar que el código del empleado sea correcto |
| `E002` | Concepto no encontrado | Verificar que el código del concepto exista en el sistema |
| `E003` | Cuenta de vacaciones no encontrada | Crear una cuenta de vacaciones para el empleado |
| `E004` | Balance insuficiente de vacaciones | Verificar el balance o permitir balance negativo en la política |
| `E005` | Formato de fecha inválido | Usar formato DD/MM/YYYY |
| `E006` | Fechas de descanso requeridas | Completar fecha_inicio_descanso y fecha_fin_descanso |
| `E007` | Tipo de valor inválido | Usar: monto, horas, dias, cantidad, o porcentaje |

## Consideraciones Técnicas

### Implementación del Importador

Si se implementa la funcionalidad de importación Excel, debe:

1. **Usar `openpyxl`** para leer archivos Excel (ya instalado en el proyecto)
2. **Validar fila por fila** y acumular errores antes de fallar
3. **Crear transacciones atómicas**: Si una fila falla, deshacer toda la importación
4. **Registrar auditoría**: Quién importó, cuándo, cuántas filas
5. **Mostrar resumen**: X filas exitosas, Y errores, con detalle de errores

### Ejemplo de Código de Validación

```python
from openpyxl import load_workbook
from datetime import datetime

def validar_fila_novedad(row, row_num):
    """Validate a single row from the Excel template."""
    errors = []
    
    # Validate required fields
    if not row['codigo_empleado']:
        errors.append(f"Fila {row_num}: Código de empleado requerido")
    
    # Validate vacation fields
    if row['es_descanso_vacaciones'] in ['SI', 'TRUE', '1', True]:
        if not row['fecha_inicio_descanso']:
            errors.append(f"Fila {row_num}: Fecha inicio descanso requerida para vacaciones")
        if not row['fecha_fin_descanso']:
            errors.append(f"Fila {row_num}: Fecha fin descanso requerida para vacaciones")
    
    return errors
```

### Ruta Sugerida para Importación

```python
@planilla_bp.route("/<planilla_id>/nomina/<nomina_id>/novedades/importar", 
                   methods=["GET", "POST"])
@require_write_access()
def importar_novedades_excel(planilla_id: str, nomina_id: str):
    """Import novelties from Excel file."""
    # Implementation here
    pass
```

## Plantilla de Ejemplo

Se recomienda proporcionar una plantilla Excel de ejemplo descargable que incluya:

1. Hoja con las columnas correctamente configuradas
2. Hoja de instrucciones con esta documentación
3. Hoja con ejemplos de datos válidos
4. Validación de datos en celdas (listas desplegables para campos con valores fijos)

## Mantenimiento

Este documento debe actualizarse si:
- Se agregan nuevos campos al modelo `NominaNovedad`
- Cambian los requisitos de validación
- Se modifican los tipos de valores permitidos
- Se agregan nuevas funcionalidades al módulo de vacaciones

---

**Última actualización**: Diciembre 2025  
**Versión**: 1.0  
**Módulo**: Novedades de Nómina con Integración de Vacaciones
