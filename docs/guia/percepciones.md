# Percepciones (Ingresos)

Las percepciones son conceptos de **ingreso** que se **suman** al salario base del empleado para formar el salario bruto.

## Concepto

```
Salario Base + Percepciones = Salario Bruto
```

Las percepciones incluyen:

- Bonificaciones
- Comisiones
- Horas extras
- Viáticos
- Cualquier otro ingreso adicional

## Acceder al Módulo

1. Navegue a **Configuración > Percepciones**

## Crear Nueva Percepción

1. Haga clic en **Nueva Percepción**
2. Complete el formulario

### Datos Básicos

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| Código | Identificador único (ej: `HRS_EXTRA`) | Sí |
| Nombre | Nombre descriptivo | Sí |
| Descripción | Descripción detallada | No |

### Configuración de Cálculo

| Campo | Descripción |
|-------|-------------|
| Tipo de Cálculo | Cómo se calcula el monto |
| Monto Predeterminado | Valor fijo (para tipo Fijo) |
| Porcentaje | Porcentaje a aplicar |
| Base de Cálculo | Sobre qué se calcula el porcentaje |
| Unidad de Cálculo | Por hora, día, mes, etc. |

#### Tipos de Cálculo

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Monto Fijo** | Un valor fijo cada período | Bono mensual de C$ 500 |
| **Porcentaje del Salario Base** | % del salario base | 5% del salario como bono |
| **Porcentaje del Salario Bruto** | % del bruto acumulado | Comisión sobre ventas |
| **Por Horas** | Valor por hora trabajada | Horas extras |
| **Por Días** | Valor por día | Viáticos diarios |
| **Fórmula Personalizada** | Cálculo con fórmula JSON | Cálculos complejos |

#### Efecto detallado por opción

- **Monto Fijo**: usa el valor de **Monto Predeterminado**.
- **Porcentaje del Salario Base**: `salario_base × porcentaje`.
- **Porcentaje del Salario Bruto**: `salario_bruto × porcentaje`.
- **Por Horas / Por Días**:
  - Requiere una **novedad** con el código del concepto (ej: HRS_EXTRA).
  - Calcula la tasa por hora o día y multiplica por la cantidad registrada.
  - El **porcentaje** actúa como factor sobre la tasa (ej: 150% para horas extras).
- **Fórmula Personalizada**: requiere un esquema de fórmula configurado; sin esquema no hay cálculo automático.

#### Base de Cálculo

La base solo afecta cálculos **Por Horas** o **Por Días**:

- **Salario Bruto**: la tasa usa `salario_bruto`.
- **Cualquier otra opción**: la tasa usa `salario_mensual`.

#### Unidad de Cálculo

La **Unidad de Cálculo** es informativa para reportes/UI; no cambia el cálculo.

#### Casos límite y opciones sin efecto directo

- **Unidad de Cálculo** no altera el cálculo; solo afecta la presentación.
- **Base de Cálculo** solo impacta **Por Horas** o **Por Días**.
- Si no existe **novedad** para el código del concepto, el monto por horas/días será **0**.

### Configuración Adicional

| Campo | Descripción |
|-------|-------------|
| Gravable | ¿Está sujeta a impuestos? |
| Recurrente | ¿Se aplica automáticamente cada período? |
| Vigente Desde | Fecha desde la cual es válida |
| Válido Hasta | Fecha hasta la cual es válida |
| Editable en Nómina | ¿Se puede modificar durante la nómina? |

### Información Contable

| Campo | Descripción |
|-------|-------------|
| Contabilizable | ¿Genera asiento contable? |
| Invertir Asiento Contable | Invierte débito y crédito en el asiento |
| Mostrar como Ingreso en Reportes | Controla presentación en informes financieros |
| Cuenta Contable (Debe) | Cuenta para el débito |
| Cuenta Contable (Haber) | Cuenta para el crédito |

#### Invertir Asiento Contable

**Introducido en v1.1.0**

Este campo permite invertir la dirección de las cuentas débito/crédito en el asiento contable generado. Es útil para situaciones especiales donde la naturaleza contable de la percepción requiere un tratamiento inverso al estándar.

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
- Percepciones que contablemente funcionan como deducciones
- Ajustes de nómina con tratamiento contable especial
- Reversiones o correcciones

#### Mostrar como Ingreso en Reportes

**Introducido en v1.1.0**

Este campo controla cómo se presenta la percepción en los reportes e informes financieros.

**Valores:**
- `True` (predeterminado): Se muestra como ingreso del empleado
- `False`: Se oculta o presenta de forma diferente según el tipo de reporte

**Casos de Uso:**
- Ajustes técnicos que no deben aparecer como ingresos en reportes de compensación
- Percepciones que son reversiones o correcciones
- Conceptos internos de control que no son parte del salario visible

!!! info "Impacto en Reportes"
    Esta configuración solo afecta la **presentación visual** en reportes. El cálculo de nómina y contabilización no se ven afectados.

### Configuración de Ausencias Predeterminadas

Las percepciones pueden configurar comportamientos predeterminados para el manejo de ausencias:

| Campo | Descripción | Valores |
|-------|-------------|---------|
| Es Inasistencia | Marca esta percepción como relacionada con ausencias | Sí/No |
| Descontar Pago por Inasistencia | Si debe deducirse del salario cuando hay ausencias | Sí/No |

#### ¿Cómo funcionan los valores predeterminados?

Cuando crea una **novedad de nómina** (NominaNovedad) basada en esta percepción:

1. **Si la novedad NO especifica** valores explícitos para `es_inasistencia` o `descontar_pago_inasistencia`, el sistema **hereda automáticamente** los valores configurados en el concepto de percepción.

2. **Si la novedad SÍ especifica** valores explícitos, estos **tienen prioridad** sobre los predeterminados del concepto.

#### Casos de Uso Comunes

**Vacaciones Pagadas:**
```yaml
Código: VACACIONES
Nombre: Vacaciones Anuales
Es Inasistencia: Sí
Descontar Pago por Inasistencia: No  # No se descuenta porque son pagadas
```

**Incapacidad con Subsidio:**
```yaml
Código: INCAPACIDAD
Nombre: Incapacidad Médica
Es Inasistencia: Sí
Descontar Pago por Inasistencia: Sí  # Se descuenta el día normal
# Luego se compensa con otro concepto de subsidio
```

**Permiso Sin Goce de Salario:**
```yaml
Código: PERMISO_SIN_GOCE
Nombre: Permiso Sin Goce de Salario
Es Inasistencia: Sí
Descontar Pago por Inasistencia: Sí  # Se descuenta completamente
```

#### Ventajas de los Valores Predeterminados

✅ **Consistencia**: Todas las novedades del mismo tipo se comportan igual por defecto  
✅ **Menos errores**: No es necesario recordar configurar las banderas en cada novedad  
✅ **Flexibilidad**: Aún puede sobrescribir el comportamiento en casos especiales  
✅ **Mantenibilidad**: Cambiar el comportamiento de un concepto actualiza todas las novedades futuras

!!! info "Relación con el Sistema de Inasistencias"
    Para más detalles sobre cómo funcionan las inasistencias y su impacto en el cálculo de nómina, consulte el [Sistema de Inasistencias](../sistema-inasistencias.md).

## Ejemplos de Percepciones

### Horas Extras

```yaml
Código: HRS_EXTRA
Nombre: Horas Extras
Tipo de Cálculo: Por Horas
Monto Predeterminado: (Salario / 30 / 8) * 2  # Doble del valor hora
Gravable: Sí
Recurrente: No
```

!!! note "Novedades de Nómina"
    Las horas extras se registran como novedades en la nómina. El sistema multiplica la cantidad de horas por el valor hora.

### Bono de Productividad

```yaml
Código: BONO_PROD
Nombre: Bono de Productividad
Tipo de Cálculo: Monto Fijo
Monto Predeterminado: 1500.00
Gravable: Sí
Recurrente: Sí
```

### Comisión sobre Ventas

```yaml
Código: COMISION
Nombre: Comisiones de Ventas
Tipo de Cálculo: Porcentaje del Salario Bruto
Porcentaje: 5.00
Base de Cálculo: Salario Bruto
Gravable: Sí
Recurrente: No
```

### Viáticos

```yaml
Código: VIATICOS
Nombre: Viáticos
Tipo de Cálculo: Por Días
Monto Predeterminado: 500.00  # Por día
Gravable: No  # Generalmente no gravables
Recurrente: No
```

### Aguinaldo (cuando se paga)

```yaml
Código: AGUINALDO_PAGO
Nombre: Aguinaldo (Treceavo Mes)
Tipo de Cálculo: Fórmula Personalizada
Gravable: Sí
Recurrente: No  # Solo en diciembre
```

## Percepciones Gravables vs No Gravables

### Gravables

Sujetas a impuestos y deducciones de seguridad social:

- Salario base
- Bonificaciones regulares
- Comisiones
- Horas extras

### No Gravables

Exentas de impuestos (según legislación):

- Viáticos (hasta cierto límite)
- Indemnizaciones
- Algunos subsidios

!!! warning "Consulte la Ley"
    Las exenciones varían según la legislación de cada país. Consulte las normas locales para determinar qué percepciones son gravables.

## Asignar a Planilla

Después de crear una percepción, debe asignarla a las planillas donde aplica:

1. Navegue a **Planillas** y edite la planilla
2. En la sección **Percepciones**, haga clic en **Agregar Percepción**
3. Seleccione la percepción
4. Configure el orden de cálculo
5. Haga clic en **Agregar**

### Orden de Cálculo

El orden determina en qué secuencia se calculan las percepciones. Esto es importante cuando una percepción depende de otra (ej: comisión sobre el bruto que incluye otras percepciones).

## Vigencia

Las percepciones pueden tener fecha de vigencia:

- **Vigente Desde**: La percepción no se aplicará antes de esta fecha
- **Válido Hasta**: La percepción no se aplicará después de esta fecha

Esto es útil para:

- Bonos temporales
- Cambios en la política de compensación
- Conceptos que dejan de aplicarse

## Fórmulas Personalizadas

Para cálculos complejos, use el tipo **Fórmula Personalizada** con un esquema JSON:

```json
{
  "variables": {
    "salario_base": "salario_mensual",
    "dias_trabajados": "novedad_dias_trabajados"
  },
  "formula": "salario_base / 30 * dias_trabajados * 1.5",
  "output": "resultado"
}
```

!!! info "Motor de Fórmulas"
    El sistema incluye un motor de fórmulas que evalúa expresiones matemáticas con variables del contexto de cálculo.

## Buenas Prácticas

### Nomenclatura

- Use códigos cortos y descriptivos
- Mantenga consistencia en los nombres
- Documente cada percepción

### Configuración

- Defina correctamente si es gravable o no
- Configure la vigencia cuando corresponda
- Use el tipo de cálculo apropiado

### Auditoría

- El sistema registra quién creó/modificó cada percepción
- Las nóminas conservan el detalle de cada percepción aplicada

## Solución de Problemas

### "La percepción no aparece en la nómina"

- Verifique que esté activa
- Verifique las fechas de vigencia
- Verifique que esté asignada a la planilla

### "El monto calculado es incorrecto"

- Revise el tipo de cálculo configurado
- Verifique el porcentaje o monto predeterminado
- Revise si hay un monto override en la asignación a planilla
