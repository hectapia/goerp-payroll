# Sistema de Registro de Inasistencias

## Descripción General

El sistema de GoERP Payroll incluye un módulo completo para el registro y procesamiento de inasistencias (ausencias) de los empleados. Este módulo permite configurar **cuatro tipos diferentes** de inasistencias según su impacto en el pago del trabajador.

## Tipos de Inasistencias

### 1. Inasistencias que NO se descuentan del pago

Estas son ausencias justificadas que no afectan el salario del empleado. Por ejemplo:
- Citas médicas justificadas
- Permisos especiales
- Días festivos trabajados compensados

**Configuración:**
- `es_inasistencia = True`
- `descontar_pago_inasistencia = False`

**Efecto:** El sistema registra la ausencia para fines de auditoría y control, pero NO deduce ningún monto del salario del empleado.

**Ejemplo:**
```python
novedad = NominaNovedad(
    codigo_concepto="PERMISO_JUSTIFICADO",
    valor_cantidad=Decimal("1.00"),
    tipo_valor="dias",
    es_inasistencia=True,
    descontar_pago_inasistencia=False,  # NO descuenta
)
# Resultado: Empleado recibe su salario completo
```

### 2. Inasistencias que SÍ se descuentan del pago

Estas son ausencias injustificadas o no autorizadas que resultan en una deducción proporcional del salario. Por ejemplo:
- Ausencias injustificadas
- Llegadas tardías no autorizadas
- Abandono de puesto

**Configuración:**
- `es_inasistencia = True`
- `descontar_pago_inasistencia = True`

**Efecto:** El sistema calcula el valor proporcional de la ausencia y lo deduce del salario base del empleado antes de calcular otras deducciones.

**Cálculo:**
```
Descuento por día = Salario Mensual / Días del Mes
Descuento por hora = (Salario Mensual / Días del Mes) / Horas por Día
```

**Ejemplo:**
```python
# Salario: $15,000, Días del mes: 30
# Ausencia: 1 día
novedad = NominaNovedad(
    codigo_concepto="AUSENCIA_INJUSTIFICADA",
    valor_cantidad=Decimal("1.00"),
    tipo_valor="dias",
    es_inasistencia=True,
    descontar_pago_inasistencia=True,  # SÍ descuenta
)
# Resultado: Descuenta $500 (15000/30)
# Salario final: $14,500
```

### 3. Inasistencias con compensación en el mismo concepto

Estas son ausencias que se descuentan del salario pero se compensan o pagan a través de una deducción con el mismo código. Por ejemplo:
- Licencias especiales con compensación diferida
- Ausencias con pago diferenciado por categoría
- Permisos compensados con bonificaciones

**Configuración:**
- `es_inasistencia = True`
- `descontar_pago_inasistencia = True`
- Existe una **deducción** en el catálogo con el mismo `codigo_concepto`

**Efecto:** El sistema:
1. Deduce el valor de la ausencia del salario base
2. Previene la aplicación duplicada de la deducción del catálogo (evita doble descuento)
3. Permite que la lógica de la deducción catalogada maneje el monto final

**Ejemplo:**
```python
# Deducción en catálogo
deduccion = Deduccion(
    codigo="LICENCIA_ESPECIAL",
    formula_tipo=FormulaType.FIJO,
    monto_default=Decimal("300.00"),  # Descuento fijo diferente
)

# Novedad de ausencia con mismo código
novedad = NominaNovedad(
    codigo_concepto="LICENCIA_ESPECIAL",  # Mismo código
    valor_cantidad=Decimal("1.00"),
    tipo_valor="dias",
    es_inasistencia=True,
    descontar_pago_inasistencia=True,
)
# Resultado: Se descuenta el día pero NO se aplica la deducción
# del catálogo (evita doble descuento)
```

### 4. Inasistencias con subsidio parcial (Subsidio Médico)

Este es un caso especial muy común donde un empleado está ausente pero recibe un subsidio parcial que incrementa sus ingresos en un porcentaje. Por ejemplo:
- Incapacidad médica con subsidio del 60%-80%
- Licencia por enfermedad con compensación del seguro social
- Ausencia médica con pago parcial

**Configuración:**
- **Ausencia**: `es_inasistencia = True`, `descontar_pago_inasistencia = True`
- **Subsidio**: Una **percepción** independiente que se suma al salario

**Efecto:** El sistema:
1. Deduce el 100% del día ausente del salario base
2. Agrega el monto del subsidio como percepción (ej: 60% del salario diario)
3. Resultado neto: El empleado recibe el porcentaje del subsidio (pierde solo el complemento)

**Ejemplo - Caso Real:**
```python
# Salario mensual: $30,000
# Salario quincenal: $15,000
# Salario diario: $1,000
# Primera quincena: 5 días con subsidio médico al 60%

# 1. Crear ausencia médica (descuenta 5 días completos = $5,000)
novedad_ausencia = NominaNovedad(
    codigo_concepto="AUSENCIA_MEDICA",
    valor_cantidad=Decimal("5.00"),
    tipo_valor="dias",
    es_inasistencia=True,
    descontar_pago_inasistencia=True,  # Descuenta los 5 días
)

# 2. Crear subsidio médico (suma 60% = $3,000)
novedad_subsidio = NominaNovedad(
    codigo_concepto="SUBSIDIO_MEDICO",
    valor_cantidad=Decimal("3000.00"),  # 60% de $5,000
    tipo_valor="monto",
    es_inasistencia=False,  # NO es ausencia, es compensación
    descontar_pago_inasistencia=False,
)

# Resultado final:
# Salario base quincenal: $15,000.00
# Menos ausencia (5 días): -$5,000.00
# Salario después de ausencia: $10,000.00
# Más subsidio (60%): +$3,000.00
# Total ingreso: $13,000.00
# Pérdida neta: $2,000.00 (40% de los 5 días)
```

## Estructura de Datos

### Modelo `NominaNovedad`

```python
class NominaNovedad:
    # Campos de identificación
    nomina_id: str                    # FK a Nomina
    empleado_id: str                  # FK a Empleado
    codigo_concepto: str              # Código del concepto
    
    # Valor de la novedad
    tipo_valor: str                   # 'dias' | 'horas' | 'cantidad' | 'monto' | 'porcentaje'
    valor_cantidad: Decimal           # Cantidad de unidades (ej: 2 días, 8 horas)
    fecha_novedad: date               # Fecha del evento
    
    # Flags para inasistencias
    es_inasistencia: bool             # Marca si es una ausencia
    descontar_pago_inasistencia: bool # Si se debe descontar del pago
```

### Configuración de Valores Predeterminados en Conceptos

**Nueva funcionalidad desde v1.2.0:** Los conceptos de **Percepción** y **Deducción** pueden tener valores predeterminados para las banderas de ausencia:

```python
class Percepcion:
    codigo: str
    nombre: str
    # ... otros campos ...
    es_inasistencia: bool              # Valor predeterminado para novedades
    descontar_pago_inasistencia: bool  # Valor predeterminado para novedades

class Deduccion:
    codigo: str
    nombre: str
    # ... otros campos ...
    es_inasistencia: bool              # Valor predeterminado para novedades
    descontar_pago_inasistencia: bool  # Valor predeterminado para novedades
```

#### ¿Cómo funcionan los valores predeterminados?

1. **Si la novedad NO especifica** valores para `es_inasistencia` o `descontar_pago_inasistencia`, el sistema **hereda automáticamente** los valores del concepto asociado (Percepción o Deducción).

2. **Si la novedad SÍ especifica** valores explícitos, estos **tienen prioridad** sobre los predeterminados del concepto.

#### Ventajas

✅ **Consistencia:** Todas las novedades de un tipo se comportan igual por defecto  
✅ **Menos errores:** No es necesario recordar las banderas cada vez  
✅ **Flexibilidad:** Puede sobrescribir el comportamiento en casos especiales  
✅ **Mantenibilidad:** Cambiar el concepto actualiza todas las novedades futuras

#### Ejemplo de Configuración

```python
# 1. Configurar un concepto de percepción con valores predeterminados
percepcion_vacaciones = Percepcion(
    codigo="VACACIONES",
    nombre="Vacaciones Anuales",
    es_inasistencia=True,              # Predeterminado: Sí es ausencia
    descontar_pago_inasistencia=False, # Predeterminado: NO descontar
)

# 2. Crear una novedad sin especificar banderas
# Hereda automáticamente es_inasistencia=True, descontar_pago=False
novedad_auto = NominaNovedad(
    codigo_concepto="VACACIONES",
    valor_cantidad=Decimal("5.00"),
    tipo_valor="dias",
    # NO se especifican es_inasistencia ni descontar_pago_inasistencia
    # Sistema usa los valores del concepto VACACIONES
)

# 3. Crear una novedad con valores explícitos (sobrescribir)
# Ignora los predeterminados del concepto
novedad_custom = NominaNovedad(
    codigo_concepto="VACACIONES",
    valor_cantidad=Decimal("2.00"),
    tipo_valor="dias",
    es_inasistencia=True,
    descontar_pago_inasistencia=True,  # Sobrescribe el predeterminado (False)
)
```

Para más información sobre cómo configurar estos valores en las interfaces de usuario, consulte:
- [Guía de Percepciones](guia/percepciones.md)
- [Guía de Deducciones](guia/deducciones.md)

### Modelo `EmpleadoCalculo`

El objeto `EmpleadoCalculo` rastrea información de ausencias durante el cálculo de nómina:

```python
class EmpleadoCalculo:
    # Tracking de inasistencias
    inasistencia_dias: Decimal                  # Total de días ausentes con descuento
    inasistencia_horas: Decimal                 # Total de horas ausentes con descuento
    inasistencia_descuento: Decimal             # Monto total descontado por ausencias
    salario_neto_inasistencia: Decimal          # Salario después de descuentos por ausencia
    inasistencia_codigos_descuento: set[str]    # Códigos de conceptos ya descontados
```

## Flujo de Procesamiento

### Paso 1: Carga de Novedades

El `NoveltyProcessor` carga las novedades del empleado para el período:

```python
novedades, ausencia_resumen, codigos_descuento = processor.load_novelties_with_absences(
    empleado, periodo_inicio, periodo_fin
)
```

**Retorna:**
- `novedades`: Diccionario con todos los conceptos y sus valores
- `ausencia_resumen`: Diccionario con `{'dias': Decimal, 'horas': Decimal}`
- `codigos_descuento`: Set de códigos que ya fueron descontados por ausencia

### Paso 2: Cálculo de Descuento por Ausencia

El `PayrollExecutionService` calcula el monto a descontar:

```python
descuento = (salario_diario * dias_ausencia) + (salario_hora * horas_ausencia)
```

Donde:
- `salario_diario = salario_mensual / dias_mes_nomina`
- `salario_hora = salario_diario / horas_jornada_diaria`

### Paso 3: Aplicación del Descuento

El descuento se aplica al salario base antes de calcular otras deducciones:

```python
salario_neto_inasistencia = salario_mensual - descuento_inasistencia
```

### Paso 4: Prevención de Doble Descuento

El `DeductionCalculator` verifica si el código de una deducción ya fue aplicado por ausencia:

```python
if deduccion.codigo in emp_calculo.inasistencia_codigos_descuento:
    continue  # Saltar esta deducción para evitar doble descuento
```

## Configuración del Sistema

### Parámetros Necesarios

En la tabla `configuracion` se deben configurar:

```python
configuracion = Configuracion(
    dias_mes_nomina=30,           # Días base para cálculo mensual
    horas_jornada_diaria=8,       # Horas de trabajo por día
)
```

### Creación de Novedades de Ausencia

#### Ejemplo 1: Ausencia Justificada (sin descuento)

```python
novedad = NominaNovedad(
    nomina_id=nomina.id,
    empleado_id=empleado.id,
    codigo_concepto="AUSENCIA_JUSTIFICADA",
    valor_cantidad=Decimal("1.00"),
    tipo_valor="dias",
    fecha_novedad=date(2025, 1, 15),
    es_inasistencia=True,
    descontar_pago_inasistencia=False,  # NO descontar
)
```

#### Ejemplo 2: Ausencia Injustificada (con descuento)

```python
novedad = NominaNovedad(
    nomina_id=nomina.id,
    empleado_id=empleado.id,
    codigo_concepto="AUSENCIA_INJUSTIFICADA",
    valor_cantidad=Decimal("2.00"),
    tipo_valor="dias",
    fecha_novedad=date(2025, 1, 20),
    es_inasistencia=True,
    descontar_pago_inasistencia=True,  # SÍ descontar
)
```

#### Ejemplo 3: Ausencia con Compensación en mismo concepto

```python
# 1. Crear la novedad de ausencia
novedad = NominaNovedad(
    nomina_id=nomina.id,
    empleado_id=empleado.id,
    codigo_concepto="LICENCIA_ESPECIAL",  # Mismo código que la deducción
    valor_cantidad=Decimal("1.00"),
    tipo_valor="dias",
    fecha_novedad=date(2025, 1, 25),
    es_inasistencia=True,
    descontar_pago_inasistencia=True,
)

# 2. Asegurar que existe una deducción con el mismo código
# Esta deducción NO se aplicará automáticamente debido al mecanismo
# de prevención de doble descuento
```

#### Ejemplo 4: Subsidio Médico (ausencia con percepción compensatoria)

```python
# Caso real: Primera quincena, 5 días de subsidio médico al 60%
# Salario mensual: $30,000, Quincenal: $15,000, Diario: $1,000

# 1. Crear ausencia médica (descuenta 5 días completos)
novedad_ausencia = NominaNovedad(
    nomina_id=nomina.id,
    empleado_id=empleado.id,
    codigo_concepto="AUSENCIA_MEDICA",
    valor_cantidad=Decimal("5.00"),
    tipo_valor="dias",
    fecha_novedad=date(2025, 1, 15),
    es_inasistencia=True,
    descontar_pago_inasistencia=True,  # Descuenta $5,000
)

# 2. Crear subsidio médico (60% de compensación)
novedad_subsidio = NominaNovedad(
    nomina_id=nomina.id,
    empleado_id=empleado.id,
    codigo_concepto="SUBSIDIO_MEDICO",
    valor_cantidad=Decimal("3000.00"),  # 60% de $5,000
    tipo_valor="monto",
    fecha_novedad=date(2025, 1, 15),
    percepcion_id=percepcion_subsidio.id,
    es_inasistencia=False,  # NO es ausencia, es compensación
    descontar_pago_inasistencia=False,
)

# Resultado:
# Base: $15,000 - Ausencia: $5,000 + Subsidio: $3,000 = $13,000
```

## Consultas y Reportes

### Obtener Total de Ausencias por Empleado

```sql
SELECT 
    e.codigo_empleado,
    e.primer_nombre,
    e.primer_apellido,
    COUNT(*) as total_ausencias,
    SUM(CASE WHEN nn.descontar_pago_inasistencia THEN nn.valor_cantidad ELSE 0 END) as dias_descontados,
    SUM(CASE WHEN NOT nn.descontar_pago_inasistencia THEN nn.valor_cantidad ELSE 0 END) as dias_justificados
FROM nomina_novedad nn
INNER JOIN empleado e ON nn.empleado_id = e.id
WHERE nn.es_inasistencia = TRUE
  AND nn.tipo_valor = 'dias'
  AND nn.fecha_novedad BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY e.codigo_empleado, e.primer_nombre, e.primer_apellido
ORDER BY total_ausencias DESC;
```

### Obtener Montos Descontados por Ausencia

```sql
SELECT 
    n.numero_nomina,
    e.codigo_empleado,
    en.inasistencia_dias,
    en.inasistencia_horas,
    en.inasistencia_descuento,
    en.salario_neto
FROM empleado_nomina en
INNER JOIN nomina n ON en.nomina_id = n.id
INNER JOIN empleado e ON en.empleado_id = e.id
WHERE en.inasistencia_descuento > 0
ORDER BY n.numero_nomina, e.codigo_empleado;
```

## Validaciones y Reglas de Negocio

### Validaciones Automáticas

1. **Configuración requerida:** El sistema valida que existan los parámetros `dias_mes_nomina` y `horas_jornada_diaria`
2. **Valores positivos:** Las ausencias deben tener valores positivos
3. **Tipo de valor válido:** El campo `tipo_valor` debe ser 'dias' o 'horas' para que se calcule el descuento
4. **Prevención de doble descuento:** El sistema automáticamente previene la aplicación duplicada de deducciones

### Mejores Prácticas

1. **Nomenclatura consistente:** Usar códigos descriptivos para los conceptos de ausencia
2. **Documentación:** Mantener en la descripción el tipo y efecto de cada ausencia
3. **Auditoría:** Registrar siempre la fecha del evento de ausencia
4. **Revisión periódica:** Verificar que los descuentos calculados son correctos

## Pruebas

El sistema incluye pruebas exhaustivas en `tests/test_engines/test_absence_deduction_avoidance.py`:

```bash
# Ejecutar pruebas de ausencias
pytest tests/test_engines/test_absence_deduction_avoidance.py -v

# Ejecutar todas las pruebas
pytest -x -q
```

## Soporte y Referencias

- **Código fuente:**
  - `goerp_payroll/nomina_engine/processors/novelty_processor.py`
  - `goerp_payroll/nomina_engine/calculators/deduction_calculator.py`
  - `goerp_payroll/nomina_engine/services/payroll_execution_service.py`
  - `goerp_payroll/nomina_engine/domain/employee_calculation.py`
  
- **Modelo de datos:** `goerp_payroll/model.py` (clase `NominaNovedad`)

- **Tests:** `tests/test_engines/test_absence_deduction_avoidance.py`

## Historial de Cambios

- **2025-02-09:** Implementación inicial del sistema de registro de inasistencias con soporte para tres tipos de ausencias y prevención de doble descuento.
