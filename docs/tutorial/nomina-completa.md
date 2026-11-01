# Tutorial: Nómina Completa Paso a Paso

Este tutorial le guiará paso a paso para configurar GoERP Payroll desde cero y ejecutar una nómina completa con percepciones, deducciones, prestaciones y préstamos a empleados.

## Escenario

Configuraremos una empresa ficticia con:

- **Empresa**: Comercial ABC, S.A.
- **País**: Nicaragua
- **Moneda**: Córdoba Nicaragüense (NIO)
- **Periodicidad**: Mensual
- **Empleados**: 3 empleados
- **Componentes**:
  - Percepciones: Salario base, horas extras, bonificaciones
  - Deducciones: INSS laboral, IR, cuota sindical
  - Prestaciones: INSS patronal, INATEC, vacaciones, aguinaldo, indemnización
  - Préstamos: Un empleado tiene un préstamo activo

## Paso 1: Configuración Inicial

### 1.1 Iniciar Sesión

1. Abra el navegador y acceda a `http://localhost:5000`
2. Inicie sesión con:
   - Usuario: `coati-admin`
   - Contraseña: `coati-admin`

!!! warning "Cambiar Contraseña"
    En un entorno de producción, cambie estas credenciales inmediatamente.

### 1.2 Crear la Moneda

1. Navegue a **Configuración > Monedas**
2. Haga clic en **Nueva Moneda**
3. Complete:

| Campo | Valor |
|-------|-------|
| Código | `NIO` |
| Nombre | `Córdoba Nicaragüense` |
| Símbolo | `C$` |
| Activo | ✓ |

4. Haga clic en **Guardar**

---

## Paso 2: Crear Percepciones

Las percepciones son los ingresos del empleado.

### 2.1 Percepción: Horas Extras

1. Navegue a **Configuración > Percepciones**
2. Haga clic en **Nueva Percepción**
3. Complete:

| Campo | Valor |
|-------|-------|
| Código | `HRS_EXTRA` |
| Nombre | `Horas Extras` |
| Descripción | `Pago por horas trabajadas adicionales` |
| Tipo de Cálculo | `Por Horas` |
| Gravable | ✓ |
| Recurrente | ☐ |
| Activo | ✓ |

4. Haga clic en **Guardar**

### 2.2 Percepción: Bono de Productividad

1. Haga clic en **Nueva Percepción**
2. Complete:

| Campo | Valor |
|-------|-------|
| Código | `BONO_PROD` |
| Nombre | `Bono de Productividad` |
| Descripción | `Bonificación mensual por cumplimiento de metas` |
| Tipo de Cálculo | `Monto Fijo` |
| Monto Predeterminado | `1500.00` |
| Gravable | ✓ |
| Recurrente | ✓ |
| Activo | ✓ |

3. Haga clic en **Guardar**

---

## Paso 3: Crear Deducciones

Las deducciones son los descuentos del salario.

### 3.1 Deducción: INSS Laboral

1. Navegue a **Configuración > Deducciones**
2. Haga clic en **Nueva Deducción**
3. Complete:

| Campo | Valor |
|-------|-------|
| Código | `INSS_LABORAL` |
| Nombre | `INSS Laboral` |
| Descripción | `Aporte del trabajador al Seguro Social (7%)` |
| Tipo de Deducción | `Seguro Social` |
| Es Impuesto | ☐ |
| Tipo de Cálculo | `Porcentaje del Salario Bruto` |
| Porcentaje | `7.00` |
| Antes de Impuesto | ✓ |
| Recurrente | ✓ |
| Activo | ✓ |

4. Haga clic en **Guardar**

### 3.2 Deducción: Impuesto sobre la Renta (IR)

1. Haga clic en **Nueva Deducción**
2. Complete:

| Campo | Valor |
|-------|-------|
| Código | `IR` |
| Nombre | `Impuesto sobre la Renta` |
| Descripción | `Retención de IR según tabla progresiva` |
| Tipo de Deducción | `Impuesto` |
| Es Impuesto | ✓ |
| Tipo de Cálculo | `Porcentaje del Salario Gravable` |
| Porcentaje | `15.00` |
| Antes de Impuesto | ☐ |
| Recurrente | ✓ |
| Activo | ✓ |

!!! note "Cálculo del IR"
    En este ejemplo simplificado usamos un porcentaje fijo del 15%. En producción, configure una regla de cálculo con la tabla progresiva completa del IR Nicaragua. Consulte la [Guía de Configuración de Planillas](../guia/planillas.md) para más detalles sobre reglas de cálculo y la sección de [Deducciones](../guia/deducciones.md#tablas-de-impuesto) para información sobre tablas de impuestos.

3. Haga clic en **Guardar**

### 3.3 Deducción: Cuota Sindical

1. Haga clic en **Nueva Deducción**
2. Complete:

| Campo | Valor |
|-------|-------|
| Código | `SINDICATO` |
| Nombre | `Cuota Sindical` |
| Descripción | `Aporte al sindicato de trabajadores` |
| Tipo de Deducción | `Sindical` |
| Tipo de Cálculo | `Porcentaje del Salario Base` |
| Porcentaje | `2.00` |
| Antes de Impuesto | ☐ |
| Recurrente | ✓ |
| Activo | ✓ |

3. Haga clic en **Guardar**

---

## Paso 4: Crear Prestaciones

Las prestaciones son aportes patronales (la empresa paga, no el empleado).

### 4.1 Prestación: INSS Patronal

1. Navegue a **Configuración > Prestaciones**
2. Haga clic en **Nueva Prestación**
3. Complete:

| Campo | Valor |
|-------|-------|
| Código | `INSS_PATRONAL` |
| Nombre | `INSS Patronal` |
| Descripción | `Aporte patronal al Seguro Social (22.5%)` |
| Tipo de Prestación | `Seguro Social Patronal` |
| Tipo de Cálculo | `Porcentaje del Salario Bruto` |
| Porcentaje | `22.50` |
| Recurrente | ✓ |
| Activo | ✓ |

4. Haga clic en **Guardar**

### 4.2 Prestación: INATEC

1. Haga clic en **Nueva Prestación**
2. Complete:

| Campo | Valor |
|-------|-------|
| Código | `INATEC` |
| Nombre | `Aporte INATEC` |
| Descripción | `Aporte para capacitación técnica (2%)` |
| Tipo de Prestación | `Capacitación` |
| Tipo de Cálculo | `Porcentaje del Salario Bruto` |
| Porcentaje | `2.00` |
| Recurrente | ✓ |
| Activo | ✓ |

3. Haga clic en **Guardar**

### 4.3 Prestación: Provisión de Vacaciones

1. Haga clic en **Nueva Prestación**
2. Complete:

| Campo | Valor |
|-------|-------|
| Código | `VACACIONES` |
| Nombre | `Provisión de Vacaciones` |
| Descripción | `Provisión mensual para vacaciones (8.33%)` |
| Tipo de Prestación | `Vacaciones` |
| Tipo de Cálculo | `Porcentaje del Salario Bruto` |
| Porcentaje | `8.33` |
| Recurrente | ✓ |
| Activo | ✓ |

3. Haga clic en **Guardar**

### 4.4 Prestación: Provisión de Aguinaldo

1. Haga clic en **Nueva Prestación**
2. Complete:

| Campo | Valor |
|-------|-------|
| Código | `AGUINALDO` |
| Nombre | `Provisión de Aguinaldo` |
| Descripción | `Provisión mensual para treceavo mes (8.33%)` |
| Tipo de Prestación | `Aguinaldo` |
| Tipo de Cálculo | `Porcentaje del Salario Bruto` |
| Porcentaje | `8.33` |
| Recurrente | ✓ |
| Activo | ✓ |

3. Haga clic en **Guardar**

### 4.5 Prestación: Provisión de Indemnización

1. Haga clic en **Nueva Prestación**
2. Complete:

| Campo | Valor |
|-------|-------|
| Código | `INDEMNIZACION` |
| Nombre | `Provisión de Indemnización` |
| Descripción | `Provisión mensual por antigüedad (8.33%)` |
| Tipo de Prestación | `Indemnización` |
| Tipo de Cálculo | `Porcentaje del Salario Bruto` |
| Porcentaje | `8.33` |
| Recurrente | ✓ |
| Activo | ✓ |

3. Haga clic en **Guardar**

---

## Paso 5: Registrar Empleados

### 5.1 Empleado: Juan Pérez

1. Navegue a **Personal > Empleados**
2. Haga clic en **Nuevo Empleado**
3. Complete:

**Datos Personales:**

| Campo | Valor |
|-------|-------|
| Primer Nombre | `Juan` |
| Primer Apellido | `Pérez` |
| Segundo Apellido | `García` |
| Identificación Personal | `001-150585-0001A` |

**Datos Laborales:**

| Campo | Valor |
|-------|-------|
| Fecha de Alta | `01/01/2020` |
| Cargo | `Contador` |
| Área | `Administración` |
| Activo | ✓ |

**Datos de Pago:**

| Campo | Valor |
|-------|-------|
| Salario Base | `20000.00` |
| Moneda | `NIO - Córdoba Nicaragüense` |

4. Haga clic en **Guardar**

### 5.2 Empleado: María López

1. Haga clic en **Nuevo Empleado**
2. Complete:

**Datos Personales:**

| Campo | Valor |
|-------|-------|
| Primer Nombre | `María` |
| Primer Apellido | `López` |
| Segundo Apellido | `Rodríguez` |
| Identificación Personal | `001-200690-0002B` |

**Datos Laborales:**

| Campo | Valor |
|-------|-------|
| Fecha de Alta | `15/06/2022` |
| Cargo | `Asistente Administrativa` |
| Área | `Administración` |
| Activo | ✓ |

**Datos de Pago:**

| Campo | Valor |
|-------|-------|
| Salario Base | `15000.00` |
| Moneda | `NIO - Córdoba Nicaragüense` |

3. Haga clic en **Guardar**

### 5.3 Empleado: Carlos Ruiz

1. Haga clic en **Nuevo Empleado**
2. Complete:

**Datos Personales:**

| Campo | Valor |
|-------|-------|
| Primer Nombre | `Carlos` |
| Primer Apellido | `Ruiz` |
| Segundo Apellido | `Mendoza` |
| Identificación Personal | `001-180795-0003C` |

**Datos Laborales:**

| Campo | Valor |
|-------|-------|
| Fecha de Alta | `01/03/2024` |
| Cargo | `Vendedor` |
| Área | `Ventas` |
| Activo | ✓ |

**Datos de Pago:**

| Campo | Valor |
|-------|-------|
| Salario Base | `12000.00` |
| Moneda | `NIO - Córdoba Nicaragüense` |

3. Haga clic en **Guardar**

---

## Paso 6: Registrar Préstamo

Carlos Ruiz tiene un préstamo aprobado.

1. Navegue al módulo de **Adelantos/Préstamos** (o desde el registro del empleado)
2. Haga clic en **Nuevo**
3. Complete:

| Campo | Valor |
|-------|-------|
| Empleado | `Carlos Ruiz` |
| Fecha de Solicitud | `01/01/2025` |
| Monto Solicitado | `6000.00` |
| Cuotas Pactadas | `6` |
| Motivo | `Gastos médicos` |

4. **Aprobar el préstamo:**

| Campo | Valor |
|-------|-------|
| Monto Aprobado | `6000.00` |
| Fecha de Aprobación | `02/01/2025` |
| Monto por Cuota | `1000.00` |
| Estado | `Aprobado` |

5. Haga clic en **Guardar**

---

## Paso 7: Crear la Planilla

### 7.1 Crear Planilla Base

1. Navegue a **Planillas**
2. Haga clic en **Nueva Planilla**
3. Complete:

| Campo | Valor |
|-------|-------|
| Nombre | `Planilla Mensual NIO` |
| Descripción | `Planilla mensual en córdobas` |
| Tipo de Planilla | `Mensual` |
| Moneda | `NIO - Córdoba Nicaragüense` |
| Aplicar Préstamos Automáticamente | ✓ |
| Prioridad Préstamos | `250` |
| Aplicar Adelantos Automáticamente | ✓ |
| Prioridad Adelantos | `251` |
| Activo | ✓ |

4. Haga clic en **Guardar**

### 7.2 Asignar Empleados

En la pantalla de edición de la planilla:

1. En la sección **Empleados**, haga clic en **Agregar**
2. Agregue cada empleado:
   - Juan Pérez
   - María López
   - Carlos Ruiz

### 7.3 Asignar Percepciones

1. En la sección **Percepciones**, agregue:

| Percepción | Orden |
|------------|-------|
| Horas Extras | 1 |
| Bono de Productividad | 2 |

### 7.4 Asignar Deducciones

1. En la sección **Deducciones**, agregue con las siguientes prioridades:

| Deducción | Prioridad | Obligatoria |
|-----------|-----------|-------------|
| INSS Laboral | 10 | ✓ |
| Impuesto sobre la Renta | 50 | ✓ |
| Cuota Sindical | 300 | ☐ |

!!! info "Prioridad de Préstamos"
    Los préstamos se deducen automáticamente con prioridad 250 (configurada en la planilla).

### 7.5 Asignar Prestaciones

1. En la sección **Prestaciones**, agregue:

| Prestación | Orden |
|------------|-------|
| INSS Patronal | 1 |
| INATEC | 2 |
| Provisión de Vacaciones | 3 |
| Provisión de Aguinaldo | 4 |
| Provisión de Indemnización | 5 |

---

## Paso 8: Ejecutar la Nómina

### 8.1 Iniciar Ejecución

1. Desde la planilla, haga clic en **Ejecutar Nómina**
2. Configure el período:

| Campo | Valor |
|-------|-------|
| Período Inicio | `01/01/2025` |
| Período Fin | `31/01/2025` |
| Fecha de Cálculo | `31/01/2025` |

3. Haga clic en **Ejecutar**

### 8.2 Resultado Esperado

#### Resumen de la Nómina

| Empleado | Salario Bruto | Deducciones | Salario Neto |
|----------|---------------|-------------|--------------|
| Juan Pérez | C$ 21,500.00 | C$ 4,285.00 | C$ 17,215.00 |
| María López | C$ 16,500.00 | C$ 3,129.00 | C$ 13,371.00 |
| Carlos Ruiz | C$ 13,500.00 | C$ 3,460.50 | C$ 10,039.50 |
| **TOTAL** | **C$ 51,500.00** | **C$ 10,874.50** | **C$ 40,625.50** |

#### Detalle: Juan Pérez

**Percepciones:**
```
Salario Base:           C$ 20,000.00
Bono de Productividad:  C$  1,500.00
---------------------------------
SALARIO BRUTO:          C$ 21,500.00
```

**Deducciones:**
```
INSS Laboral (7%):      C$  1,505.00
IR (15% de base):       C$  2,380.00  (sobre C$ 19,995)
Cuota Sindical (2%):    C$    400.00
---------------------------------
TOTAL DEDUCCIONES:      C$  4,285.00
```

**Salario Neto:** C$ 21,500.00 - C$ 4,285.00 = **C$ 17,215.00**

**Prestaciones Patronales:**
```
INSS Patronal (22.5%):  C$  4,837.50
INATEC (2%):            C$    430.00
Vacaciones (8.33%):     C$  1,790.95
Aguinaldo (8.33%):      C$  1,790.95
Indemnización (8.33%):  C$  1,790.95
---------------------------------
TOTAL PRESTACIONES:     C$ 10,640.35
```

**Costo Total Empleado:** C$ 21,500.00 + C$ 10,640.35 = **C$ 32,140.35**

#### Detalle: Carlos Ruiz (con préstamo)

**Percepciones:**
```
Salario Base:           C$ 12,000.00
Bono de Productividad:  C$  1,500.00
---------------------------------
SALARIO BRUTO:          C$ 13,500.00
```

**Deducciones:**
```
INSS Laboral (7%):      C$    945.00
IR (15% de base):       C$  1,275.50  (sobre C$ 12,555)
Cuota Préstamo:         C$  1,000.00  ← Automático
Cuota Sindical (2%):    C$    240.00
---------------------------------
TOTAL DEDUCCIONES:      C$  3,460.50
```

**Salario Neto:** C$ 13,500.00 - C$ 3,460.50 = **C$ 10,039.50**

!!! success "Préstamo Actualizado"
    Después de la nómina, el préstamo de Carlos Ruiz queda:
    
    - Saldo anterior: C$ 6,000.00
    - Cuota pagada: C$ 1,000.00
    - Saldo nuevo: C$ 5,000.00
    - Cuotas restantes: 5

### 8.3 Agregar Novedades (Opcional)

Si necesita ajustar la nómina con eventos específicos (horas extras, bonos puntuales, ausencias), puede registrar novedades antes de aprobar.

**Ejemplo**: Registrar horas extras para María López

1. Desde la vista de la nómina, haga clic en **Novedades**
2. Haga clic en **Nueva Novedad**
3. Complete:

| Campo | Valor |
|-------|-------|
| Empleado | María López |
| Tipo de Concepto | Percepción |
| Percepción | Horas Extras |
| Código del Concepto | HRS_EXTRA |
| Tipo de Valor | Horas |
| Valor/Cantidad | 8 |
| Fecha de Novedad | 20/01/2025 |

4. Haga clic en **Guardar**
5. Regrese a la vista de la nómina
6. Haga clic en **Recalcular** para aplicar la novedad

!!! note "Recalcular Nómina"
    Al recalcular, el sistema procesa nuevamente todos los empleados incluyendo las novedades registradas. Los valores anteriores se eliminan y se generan nuevos cálculos.

### 8.4 Aprobar la Nómina

1. Revise todos los detalles
2. Verifique que los cálculos son correctos
3. Haga clic en **Aprobar**

### 8.5 Aplicar la Nómina

1. Una vez aprobada, haga clic en **Aplicar**
2. La nómina queda marcada como pagada

---

## Resumen

En este tutorial ha aprendido a:

- [x] Configurar monedas
- [x] Crear percepciones (ingresos)
- [x] Crear deducciones (descuentos)
- [x] Crear prestaciones (aportes patronales)
- [x] Registrar empleados
- [x] Registrar y aprobar préstamos
- [x] Configurar una planilla completa
- [x] Ejecutar una nómina con todos los componentes
- [x] Agregar novedades a la nómina (horas extras, bonos, etc.)
- [x] Revisar, aprobar y aplicar la nómina

## Siguientes Pasos

- Explore las diferentes configuraciones de percepciones y deducciones
- Configure reglas de cálculo para el IR con tabla progresiva
- Configure tipos de cambio si trabaja con múltiples monedas
- Utilice las novedades para registrar eventos variables de nómina
- Genere reportes de nómina
- Configure campos personalizados para empleados

## Recursos Adicionales

- [Gestión de Empleados](../guia/empleados.md)
- [Percepciones](../guia/percepciones.md)
- [Deducciones](../guia/deducciones.md)
- [Prestaciones](../guia/prestaciones.md)
- [Préstamos y Adelantos](../guia/prestamos.md)
- [Configuración de Planillas](../guia/planillas.md)
- [Ejecución de Nómina (incluye Novedades)](../guia/nomina.md)
