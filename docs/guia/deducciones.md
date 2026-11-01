# Deducciones

Las deducciones son conceptos que se **restan** del salario bruto del empleado para obtener el salario neto.

## Concepto

```
Salario Bruto - Deducciones = Salario Neto
```

Las deducciones incluyen:

- Seguro social (INSS laboral)
- Impuesto sobre la renta (IR)
- Cuotas de préstamos
- Adelantos salariales
- Pensiones alimenticias
- Cuotas sindicales
- Ahorros voluntarios

## Acceder al Módulo

1. Navegue a **Configuración > Deducciones**

## Crear Nueva Deducción

1. Haga clic en **Nueva Deducción**
2. Complete el formulario

### Datos Básicos

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| Código | Identificador único (ej: `INSS_LABORAL`) | Sí |
| Nombre | Nombre descriptivo | Sí |
| Descripción | Descripción detallada | No |
| Tipo de Deducción | Categoría de la deducción | Sí |
| Es Impuesto | Si es un impuesto (IR, ISR) | No |

### Tipos de Deducción

| Tipo | Descripción |
|------|-------------|
| **General** | Deducción general |
| **Impuesto** | Impuestos (IR, ISR) |
| **Seguro Social** | Aportes a seguridad social |
| **Préstamo** | Cuotas de préstamos |
| **Adelanto** | Adelantos salariales |
| **Pensión Alimenticia** | Pensiones ordenadas judicialmente |
| **Ahorro** | Ahorro voluntario |
| **Sindical** | Cuota sindical |
| **Otro** | Otras deducciones |

### Configuración de Cálculo

| Campo | Descripción |
|-------|-------------|
| Tipo de Cálculo | Cómo se calcula el monto |
| Monto Predeterminado | Valor fijo |
| Porcentaje | Porcentaje a aplicar |
| Base de Cálculo | Sobre qué se calcula |
| Antes de Impuesto | Si se deduce antes del IR |

#### Tipos de Cálculo

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Monto Fijo** | Un valor fijo | Cuota sindical de C$ 100 |
| **Porcentaje del Salario Base** | % del salario base | N/A |
| **Porcentaje del Salario Bruto** | % del bruto | INSS 7% |
| **Porcentaje del Salario Gravable** | % del gravable | IR |
| **Tabla de Impuestos** | Usa tabla progresiva | IR Nicaragua |
| **Fórmula Personalizada** | Cálculo con fórmula JSON | Cálculos complejos |

#### Efecto detallado por opción

- **Monto Fijo**: usa el valor de **Monto Predeterminado**.
- **Porcentaje del Salario Base**: `salario_base × porcentaje`.
- **Porcentaje del Salario Bruto**: `salario_bruto × porcentaje`.
- **Porcentaje del Salario Gravable** y **Tabla de Impuestos**: requieren una regla o fórmula que implemente el cálculo; sin esquema configurado no hay cálculo automático.
- **Fórmula Personalizada**: requiere un esquema de fórmula configurado; sin esquema no hay cálculo automático.

#### Base de Cálculo

La base se conserva como referencia para fórmulas. El motor base de deducciones no usa la base salvo que una regla/fórmula la considere explícitamente.

#### Casos límite y opciones sin efecto directo

- **Porcentaje del Salario Gravable** y **Tabla de Impuestos** requieren una regla o fórmula configurada; sin esquema no hay cálculo automático.
- **Base de Cálculo** no altera el cálculo estándar; solo tiene efecto si una fórmula/regla la usa explícitamente.

### Configuración Adicional

| Campo | Descripción |
|-------|-------------|
| Antes de Impuesto | ¿Se deduce antes de calcular impuestos? |
| Recurrente | ¿Se aplica automáticamente? |
| Vigente Desde | Fecha de inicio de vigencia |
| Válido Hasta | Fecha de fin de vigencia |
| Editable en Nómina | ¿Se puede modificar? |

### Configuración de Ausencias Predeterminadas

Al igual que las percepciones, las deducciones pueden configurar comportamientos predeterminados para el manejo de ausencias:

| Campo | Descripción | Valores |
|-------|-------------|---------|
| Es Inasistencia | Marca esta deducción como relacionada con ausencias | Sí/No |
| Descontar Pago por Inasistencia | Si debe deducirse del salario cuando hay ausencias | Sí/No |

#### ¿Cómo funcionan los valores predeterminados en deducciones?

Cuando crea una **novedad de nómina** (NominaNovedad) basada en esta deducción:

1. **Si la novedad NO especifica** valores explícitos para `es_inasistencia` o `descontar_pago_inasistencia`, el sistema **hereda automáticamente** los valores configurados en el concepto de deducción.

2. **Si la novedad SÍ especifica** valores explícitos, estos **tienen prioridad** sobre los predeterminados del concepto.

#### Casos de Uso Comunes

**Descuento por Ausencia Injustificada:**
```yaml
Código: FALTA_INJUSTIFICADA
Nombre: Ausencia Injustificada
Es Inasistencia: Sí
Descontar Pago por Inasistencia: Sí  # Descuenta el día completo
```

**Día de Incapacidad a Descontar:**
```yaml
Código: INCAPACIDAD_DESC
Nombre: Descuento por Incapacidad
Es Inasistencia: Sí
Descontar Pago por Inasistencia: Sí  # Descuenta el salario del día
# Este concepto se usa para descontar antes de aplicar el subsidio
```

**Suspensión Sin Goce:**
```yaml
Código: SUSPENSION
Nombre: Suspensión Sin Goce de Salario
Es Inasistencia: Sí
Descontar Pago por Inasistencia: Sí  # Descuenta completamente
```

#### Prevención de Doble Deducción

Un caso especial ocurre cuando una inasistencia ya está descontando el pago base pero **NO** queremos que también se aplique una deducción adicional:

```yaml
# Incapacidad que descuenta el día pero no debe aplicar deducciones como INSS
Código: INCAPACIDAD_MEDICA
Es Inasistencia: Sí
Descontar Pago por Inasistencia: Sí  # Descuenta el día base
```

En este caso, si el código de esta novedad coincide con el código de una deducción existente (ej: `INCAPACIDAD_MEDICA`), el sistema **NO aplicará esa deducción** para evitar doble descuento. Luego puede aplicarse un concepto de subsidio separado.

#### Ventajas de los Valores Predeterminados

✅ **Consistencia**: Todas las novedades del mismo tipo se comportan igual por defecto  
✅ **Menos errores**: No es necesario recordar configurar las banderas en cada novedad  
✅ **Flexibilidad**: Aún puede sobrescribir el comportamiento en casos especiales  
✅ **Mantenibilidad**: Cambiar el comportamiento de un concepto actualiza todas las novedades futuras

!!! info "Relación con el Sistema de Inasistencias"
    Para más detalles sobre cómo funcionan las inasistencias, la prevención de doble deducción, y su impacto en el cálculo de nómina, consulte el [Sistema de Inasistencias](../sistema-inasistencias.md).

## Prioridad de Deducciones

!!! important "Concepto Clave"
    Las deducciones se aplican en **orden de prioridad**. Si el salario no alcanza para todas las deducciones, se aplican primero las de mayor prioridad (número menor).

### Guía de Prioridades

| Rango | Tipo de Deducción | Ejemplo |
|-------|-------------------|---------|
| 1-100 | Legal/Obligatorias | INSS, IR, pensión alimenticia |
| 101-200 | Ordenadas judicialmente | Embargos |
| 201-300 | Préstamos y adelantos | Cuotas de préstamos |
| 301-400 | Voluntarias | Ahorro, sindicato |
| 401+ | Otras | Otras deducciones |

### Configurar Prioridad

La prioridad se configura al asignar la deducción a la planilla:

1. Edite la planilla
2. Al agregar una deducción, configure la prioridad
3. Menor número = mayor prioridad (se aplica primero)

### Información Contable

Las deducciones pueden configurarse para generar asientos contables automáticos:

| Campo | Descripción |
|-------|-------------|
| Contabilizable | ¿Genera asiento contable? |
| Invertir Asiento Contable | Invierte débito y crédito en el asiento |
| Mostrar como Ingreso en Reportes | Controla presentación en informes financieros |
| Cuenta Contable (Debe) | Cuenta para el débito |
| Cuenta Contable (Haber) | Cuenta para el crédito |

#### Invertir Asiento Contable

**Introducido en v1.1.0**

Este campo permite invertir la dirección de las cuentas débito/crédito en el asiento contable generado. Es útil para situaciones especiales donde la naturaleza contable de la deducción requiere un tratamiento inverso al estándar.

**Configuración Estándar (invertir = False):**
```
Débito:  Cuenta configurada en "Cuenta Contable (Debe)"
Crédito: Cuenta configurada en "Cuenta Contable (Haber)"
```

**Configuración Invertida (invertir = True):**
```
Débito:  Cuenta configurada en "Cuenta Contable (Haber)"  ← Invertido
Crédito: Cuenta configurada en "Cuenta Contable (Debe)"   ← Invertido
```

**Casos de Uso:**
- Deducciones que contablemente funcionan como percepciones
- Ajustes de nómina con tratamiento contable especial
- Reversiones o correcciones

#### Mostrar como Ingreso en Reportes

**Introducido en v1.1.0**

Este campo controla cómo se presenta la deducción en los reportes e informes financieros.

**Valores:**
- `True` (predeterminado): Se muestra en la sección correspondiente del reporte
- `False`: Se oculta o presenta de forma diferente según el tipo de reporte

**Casos de Uso:**
- Ajustes técnicos que no deben aparecer en reportes estándar
- Deducciones que son reversiones o correcciones
- Conceptos internos de control

!!! info "Impacto en Reportes"
    Esta configuración solo afecta la **presentación visual** en reportes. El cálculo de nómina y contabilización no se ven afectados.

## Ejemplos de Deducciones

### INSS Laboral (Nicaragua)

```yaml
Código: INSS_LABORAL
Nombre: INSS Laboral
Tipo de Deducción: Seguro Social
Tipo de Cálculo: Porcentaje del Salario Bruto
Porcentaje: 7.00
Antes de Impuesto: Sí
Es Impuesto: No
```

### Impuesto sobre la Renta (IR)

```yaml
Código: IR
Nombre: Impuesto sobre la Renta
Tipo de Deducción: Impuesto
Tipo de Cálculo: Tabla de Impuestos (o Fórmula)
Antes de Impuesto: No
Es Impuesto: Sí
```

!!! note "Cálculo del IR"
    El IR en Nicaragua se calcula sobre la expectativa salarial anual usando una tabla progresiva. Consulte la sección de [Configuración de Planillas](planillas.md) para más detalles sobre reglas de cálculo.

### Cuota Sindical

```yaml
Código: SINDICATO
Nombre: Cuota Sindical
Tipo de Deducción: Sindical
Tipo de Cálculo: Porcentaje del Salario Base
Porcentaje: 2.00
Antes de Impuesto: No
```

### Pensión Alimenticia

```yaml
Código: PENSION_ALIM
Nombre: Pensión Alimenticia
Tipo de Deducción: Pensión Alimenticia
Tipo de Cálculo: Porcentaje del Salario Neto
Porcentaje: 25.00  # O el % ordenado por el juez
Antes de Impuesto: No
```

### Ahorro Voluntario

```yaml
Código: AHORRO
Nombre: Ahorro Voluntario
Tipo de Deducción: Ahorro
Tipo de Cálculo: Monto Fijo
Monto Predeterminado: 500.00
Antes de Impuesto: No
```

## Deducciones Antes de Impuesto

El campo **Antes de Impuesto** determina si la deducción reduce la base imponible para el cálculo del IR.

### Se deducen ANTES del IR:

- INSS laboral (7%)
- Aportes a AFP/fondos de pensión
- Algunos seguros médicos

### Se deducen DESPUÉS del IR:

- Préstamos
- Adelantos
- Ahorros voluntarios
- Cuotas sindicales

## Asignar a Planilla

1. Navegue a **Planillas** y edite la planilla
2. En la sección **Deducciones**, haga clic en **Agregar Deducción**
3. Configure:
   - Seleccione la deducción
   - Configure la **prioridad**
   - Marque si es **obligatoria**
4. Haga clic en **Agregar**

### Deducción Obligatoria

Si marca una deducción como obligatoria:

- Se aplicará incluso si el salario neto queda en negativo
- Útil para deducciones legales que no pueden omitirse

## Deducciones Automáticas

Los préstamos y adelantos se deducen automáticamente si:

- Están registrados en el módulo de Adelantos
- El estado es "aprobado"
- Tienen saldo pendiente

Consulte la guía de [Préstamos y Adelantos](prestamos.md) para más información.

## Tablas de Impuesto

Para impuestos progresivos como el IR, puede configurar tablas de tramos:

| Desde | Hasta | % | Cuota Fija | Sobre Excedente |
|-------|-------|---|------------|-----------------|
| 0 | 100,000 | 0% | 0 | 0 |
| 100,001 | 200,000 | 15% | 0 | 100,000 |
| 200,001 | 350,000 | 20% | 15,000 | 200,000 |
| 350,001 | 500,000 | 25% | 45,000 | 350,000 |
| 500,001+ | - | 30% | 82,500 | 500,000 |

## Flujo de Cálculo

```mermaid
flowchart TD
    A[Salario Bruto] --> B{Deducciones antes de IR}
    B --> C[INSS Laboral -7%]
    C --> D[Base Gravable]
    D --> E{Cálculo IR}
    E --> F[IR según tabla]
    F --> G{Otras Deducciones}
    G --> H[Préstamos]
    H --> I[Adelantos]
    I --> J[Otras]
    J --> K[Salario Neto]
```

## Buenas Prácticas

### Prioridades

- Configure prioridades correctamente
- Las deducciones legales deben tener prioridad alta
- Documente el orden de prioridades

### Auditoría

- Cada nómina registra las deducciones aplicadas
- Puede consultar qué deducciones no se aplicaron por saldo insuficiente

### Actualización

- Actualice porcentajes cuando cambie la ley
- Use fechas de vigencia para cambios programados

## Solución de Problemas

### "La deducción no se aplicó"

- Verifique que esté activa
- Verifique que esté asignada a la planilla
- Si no es obligatoria, puede haberse omitido por saldo insuficiente (verifique advertencias)

### "El monto de IR es incorrecto"

- Verifique las deducciones antes de impuesto
- Verifique la tabla de impuestos configurada
- Verifique los valores acumulados del empleado
