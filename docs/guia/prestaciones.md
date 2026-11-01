# Prestaciones (Aportes Patronales)

Las prestaciones son **aportes del empleador** que representan costos adicionales de la empresa. **NO afectan el salario neto del empleado**.

## Concepto Importante

!!! info "Diferencia con Deducciones"
    - **Deducciones**: Se restan del salario del empleado (él paga)
    - **Prestaciones**: Son costos del empleador (la empresa paga)
    
    Las prestaciones NO reducen el salario neto del empleado.

## ¿Para qué sirven?

Las prestaciones permiten:

- Calcular el costo total del empleado para la empresa
- Provisionar gastos futuros (vacaciones, aguinaldo)
- Generar asientos contables de los aportes patronales
- Cumplir con obligaciones legales (INSS patronal, INATEC)

## Acceder al Módulo

1. Navegue a **Configuración > Prestaciones**

## Crear Nueva Prestación

1. Haga clic en **Nueva Prestación**
2. Complete el formulario

### Datos Básicos

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| Código | Identificador único (ej: `INSS_PATRONAL`) | Sí |
| Nombre | Nombre descriptivo | Sí |
| Descripción | Descripción detallada | No |
| Tipo de Prestación | Categoría | Sí |

### Tipos de Prestación

| Tipo | Descripción |
|------|-------------|
| **Aporte Patronal** | Aportes generales del empleador |
| **Seguro Social Patronal** | INSS patronal u otros |
| **Vacaciones** | Provisión de vacaciones |
| **Aguinaldo** | Provisión de treceavo mes |
| **Indemnización** | Provisión por antigüedad |
| **Capacitación** | INATEC u otros aportes de capacitación |
| **Otro** | Otras prestaciones |

### Configuración de Cálculo

| Campo | Descripción |
|-------|-------------|
| Tipo de Cálculo | Cómo se calcula el monto |
| Monto Predeterminado | Valor fijo |
| Porcentaje | Porcentaje a aplicar |
| Base de Cálculo | Sobre qué se calcula |
| Tope de Aplicación | Monto máximo para el cálculo |

#### Tipos de Cálculo

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Monto Fijo** | Valor fijo mensual | Aporte fijo |
| **Porcentaje del Salario Base** | % del salario base | Vacaciones |
| **Porcentaje del Salario Bruto** | % del bruto | INSS patronal |
| **Provisión Mensual** | 1/12 del salario (provisión) | Aguinaldo, vacaciones |
| **Fórmula Personalizada** | Cálculo con fórmula JSON | Cálculos complejos |

#### Efecto detallado por opción

- **Monto Fijo**: usa el valor de **Monto Predeterminado**.
- **Porcentaje del Salario Base**: `salario_base × porcentaje`.
- **Porcentaje del Salario Bruto**: `salario_bruto × porcentaje`.
- **Provisión Mensual**: requiere una fórmula/regla configurada que implemente la provisión.
- **Fórmula Personalizada**: requiere un esquema de fórmula configurado; sin esquema no hay cálculo automático.

#### Base de Cálculo

La base se conserva como referencia para fórmulas. El motor base de prestaciones no usa la base salvo que una regla/fórmula la considere explícitamente.

### Tipo de Acumulación

El **Tipo de Acumulación** define cómo se guarda el saldo acumulado de la prestación:

| Opción | Efecto en el saldo |
|--------|-------------------|
| **Mensual** | El saldo se reinicia al iniciar un nuevo mes. |
| **Anual** | El saldo se acumula durante el año fiscal. |
| **Vida Laboral** | El saldo se acumula durante toda la relación laboral. |

#### Casos límite y opciones sin efecto directo

- **Provisión Mensual** requiere una fórmula/regla configurada; sin esquema no hay cálculo automático.
- **Base de Cálculo** no altera el cálculo estándar; solo tiene efecto si una fórmula/regla la usa explícitamente.

### Tope de Aplicación

Algunas prestaciones tienen un tope (techo salarial). Por ejemplo, el INSS patronal en Nicaragua se calcula sobre un máximo salarial:

```yaml
Tope de Aplicación: 132,267.50  # Techo INSS 2024
```

Si el salario supera el tope, la prestación se calcula solo sobre el tope.

## Prestaciones Comunes en Nicaragua

### INSS Patronal

```yaml
Código: INSS_PATRONAL
Nombre: INSS Patronal
Tipo de Prestación: Seguro Social Patronal
Tipo de Cálculo: Porcentaje del Salario Bruto
Porcentaje: 22.50  # Régimen Integral
Base de Cálculo: Salario Bruto
Tope de Aplicación: 132267.50  # Techo INSS
```

!!! note "Régimen INSS"
    El porcentaje varía según el régimen:
    - Régimen Integral: 22.50%
    - Régimen IVM-RP: 13.00%

### INATEC

```yaml
Código: INATEC
Nombre: Aporte INATEC
Tipo de Prestación: Capacitación
Tipo de Cálculo: Porcentaje del Salario Bruto
Porcentaje: 2.00
Base de Cálculo: Salario Bruto
```

### Provisión de Vacaciones

En Nicaragua, los empleados acumulan 2.5 días de vacaciones por mes trabajado (30 días al año). La provisión mensual es:

```yaml
Código: VACACIONES
Nombre: Provisión de Vacaciones
Tipo de Prestación: Vacaciones
Tipo de Cálculo: Porcentaje del Salario Bruto
Porcentaje: 8.33  # 1/12 = 8.33%
Base de Cálculo: Salario Bruto
```

### Provisión de Aguinaldo

El aguinaldo (treceavo mes) es un mes de salario al año:

```yaml
Código: AGUINALDO
Nombre: Provisión de Aguinaldo
Tipo de Prestación: Aguinaldo
Tipo de Cálculo: Porcentaje del Salario Bruto
Porcentaje: 8.33  # 1/12 = 8.33%
Base de Cálculo: Salario Bruto
```

### Provisión de Indemnización

La indemnización por antigüedad es un mes por año trabajado:

```yaml
Código: INDEMNIZACION
Nombre: Provisión de Indemnización
Tipo de Prestación: Indemnización
Tipo de Cálculo: Porcentaje del Salario Bruto
Porcentaje: 8.33  # 1/12 = 8.33%
Base de Cálculo: Salario Bruto
```

## Resumen de Costos Patronales (Nicaragua)

| Concepto | Porcentaje | Tope |
|----------|------------|------|
| INSS Patronal | 22.50% | Sí |
| INATEC | 2.00% | No |
| Vacaciones | 8.33% | No |
| Aguinaldo | 8.33% | No |
| Indemnización | 8.33% | No |
| **Total** | **49.49%** | - |

!!! warning "Costo Real"
    El costo real de un empleado para la empresa es aproximadamente **150%** de su salario bruto cuando se incluyen todas las prestaciones.

## Cálculo del Costo Total del Empleado

```mermaid
graph LR
    A[Salario Bruto] --> B[+ INSS Patronal 22.5%]
    B --> C[+ INATEC 2%]
    C --> D[+ Vacaciones 8.33%]
    D --> E[+ Aguinaldo 8.33%]
    E --> F[+ Indemnización 8.33%]
    F --> G[= Costo Total Empleado]
```

### Ejemplo de Cálculo

Para un empleado con salario bruto de C$ 20,000:

| Concepto | Cálculo | Monto |
|----------|---------|-------|
| Salario Bruto | - | C$ 20,000.00 |
| INSS Patronal | 20,000 × 22.5% | C$ 4,500.00 |
| INATEC | 20,000 × 2% | C$ 400.00 |
| Vacaciones | 20,000 × 8.33% | C$ 1,666.00 |
| Aguinaldo | 20,000 × 8.33% | C$ 1,666.00 |
| Indemnización | 20,000 × 8.33% | C$ 1,666.00 |
| **Costo Total** | - | **C$ 29,898.00** |

## Asignar a Planilla

1. Navegue a **Planillas** y edite la planilla
2. En la sección **Prestaciones**, haga clic en **Agregar Prestación**
3. Seleccione la prestación
4. Configure el orden (opcional)
5. Haga clic en **Agregar**

## Vigencia y Topes

### Fechas de Vigencia

Configure fechas de vigencia para:

- Cambios en porcentajes por ley
- Nuevas prestaciones
- Prestaciones que dejan de aplicarse

### Topes (Techos)

El **Tope de Aplicación** es el monto máximo sobre el cual se calcula la prestación:

```
Si Salario > Tope:
    Prestación = Tope × Porcentaje
Sino:
    Prestación = Salario × Porcentaje
```

## Información Contable

Configure las cuentas contables para generar asientos:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| Cuenta Debe | Cuenta de gasto | 5110 - Gastos de Personal |
| Cuenta Haber | Cuenta de pasivo/provisión | 2150 - Provisiones |

## En la Nómina

Al ejecutar una nómina, las prestaciones se calculan para cada empleado pero:

- **NO** se restan del salario del empleado
- Aparecen en un apartado separado "Prestaciones Patronales"
- Se usan para calcular el costo total del empleado
- Generan asientos contables de provisión

## Buenas Prácticas

### Actualización

- Actualice porcentajes cuando cambie la ley
- Actualice techos anualmente (el techo INSS cambia cada año)
- Use fechas de vigencia para programar cambios

### Contabilidad

- Configure cuentas contables correctas
- Las provisiones deben cuadrar con los pasivos
- Revise los asientos generados

### Auditoría

- Cada nómina registra las prestaciones calculadas
- Puede generar reportes de costo total por empleado

## Solución de Problemas

### "La prestación no aparece en la nómina"

- Verifique que esté activa
- Verifique las fechas de vigencia
- Verifique que esté asignada a la planilla

### "El monto es diferente al esperado"

- Verifique el tope de aplicación
- Verifique la base de cálculo (base vs bruto)
- Revise si hay un monto override en la asignación
