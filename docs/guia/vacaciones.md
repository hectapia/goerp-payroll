# Guía de Usuario - Módulo de Vacaciones

## Introducción

El módulo de vacaciones de GoERP Payroll permite gestionar de forma robusta y auditable las vacaciones de los empleados. Este módulo es completamente flexible y se adapta a las regulaciones de cualquier país de América.

## Conceptos Clave

### Política de Vacaciones
Define las reglas de cómo se acumulan, usan y vencen las vacaciones. Una política puede aplicarse a:
- Una planilla específica (recomendado para multi-país)
- Una empresa completa
- Todo el sistema (política global)

### Cuenta de Vacaciones
Cada empleado tiene una cuenta de vacaciones que:
- Está asociada a una política específica
- Mantiene el balance actual de días/horas disponibles
- Registra la última fecha de acumulación

### Libro Mayor (Ledger)
Es el registro inmutable de todos los movimientos de vacaciones. Incluye:
- **Acumulación (ACCRUAL)**: Vacaciones ganadas
- **Uso (USAGE)**: Vacaciones tomadas
- **Ajuste (ADJUSTMENT)**: Correcciones manuales
- **Vencimiento (EXPIRATION)**: Vacaciones expiradas
- **Pago (PAYOUT)**: Vacaciones pagadas al terminar relación laboral

### Novedades de Vacaciones
Son solicitudes de tiempo libre que:
- Deben ser aprobadas por un administrador
- Se procesan automáticamente durante la ejecución de la nómina
- Reducen el balance de vacaciones del empleado

## Configuración Inicial

### Paso 0: Cargar Saldos Iniciales (Solo Durante Implementación)

**IMPORTANTE**: Si está implementando el sistema en una empresa que ya tiene empleados con vacaciones acumuladas, debe cargar los saldos iniciales ANTES de comenzar a procesar nóminas.

#### Opción A: Carga Individual

Para empresas pequeñas o para cargar empleados específicos:

1. Navegue a **Vacaciones → Dashboard**
2. En la sección **Carga de Saldos Iniciales**, haga clic en **Carga Individual**
3. Seleccione el empleado
4. Ingrese el **Saldo Inicial** (días u horas acumuladas)
5. Seleccione la **Fecha de Corte** (típicamente la fecha de implementación del sistema)
6. Agregue observaciones si es necesario
7. Haga clic en **Cargar Saldo Inicial**

**Requisitos**:
- El empleado debe tener una cuenta de vacaciones activa
- La cuenta no debe tener movimientos previos

#### Opción B: Carga Masiva desde Excel

Para empresas con muchos empleados:

1. Prepare un archivo Excel con las siguientes columnas (sin encabezados):
   - **Columna A**: Código de Empleado (ej: `EMP001`)
   - **Columna B**: Saldo Inicial (ej: `15.5`)
   - **Columna C**: Fecha de Corte en formato `DD/MM/YYYY` (ej: `31/12/2024`)
   - **Columna D**: Observaciones (opcional)

2. Ejemplo de archivo Excel:
   ```
   EMP001    15.5    31/12/2024    Saldo inicial 2024
   EMP002    20.0    31/12/2024    Vacaciones acumuladas
   EMP003    8.75    31/12/2024
   ```

3. Navegue a **Vacaciones → Dashboard**
4. En la sección **Carga de Saldos Iniciales**, haga clic en **Carga Masiva (Excel)**
5. Suba el archivo Excel
6. Revise los resultados de la carga

**Validaciones Automáticas**:
- Verifica que los empleados existan y estén activos
- Verifica que cada empleado tenga una cuenta de vacaciones activa
- Verifica que las cuentas no tengan movimientos previos
- Reporta errores por fila para facilitar correcciones

**Notas Importantes**:
- Solo puede cargar saldos iniciales en cuentas sin historial
- El sistema crea una entrada de tipo `ADJUSTMENT` en el libro mayor
- Todos los movimientos quedan registrados con auditoría completa

### Paso 1: Crear una Política de Vacaciones

1. Navegue a **Vacaciones → Políticas de Vacaciones**
2. Haga clic en **Nueva Política**
3. Complete la información básica:
   - **Código**: Identificador único (ej: `NIC-STANDARD`, `USA-HOURLY`)
   - **Nombre**: Nombre descriptivo
   - **Descripción**: Detalles de la política
   - **Planilla**: Seleccione la planilla a la que aplica (recomendado)
   - **Empresa**: Opcional, para políticas que aplican a toda la empresa

4. Configure la **Acumulación**:
   - **Método de Acumulación**:
     - `Periódico`: Cantidad fija por período
     - `Proporcional`: Basado en días/horas trabajadas
     - `Por Antigüedad`: Escalonado por años de servicio
   - **Tasa de Acumulación**: Cantidad que se acumula por período
   - **Frecuencia**: Mensual, Quincenal o Anual
   - **Base de Acumulación** (solo si el método es proporcional):
     - **Días Trabajados**: usa los días del período como base
     - **Horas Trabajadas**: usa horas estándar por día × días del período
   - **Días Mínimos de Servicio**: Días antes de comenzar a acumular

   **Efecto de la frecuencia**:
   - **Mensual/Quincenal/Anual** determinan el período esperado; si el período real no coincide, el sistema prorratea.

5. Configure los **Límites**:
   - **Balance Máximo**: Límite total de vacaciones acumulables
   - **Límite de Traspaso**: Máximo que puede pasar al siguiente período
   - **Permitir Balance Negativo**: Si se permiten vacaciones adelantadas

6. Configure el **Vencimiento**:
   - **Regla de Vencimiento**: Cuándo expiran las vacaciones no usadas
   - **Meses para Vencimiento**: Tiempo antes de expirar
   - **Fecha Personalizada**: Fecha exacta para vencimiento (si aplica)

   **Efecto de la regla de vencimiento**:
   - **Nunca**: no caducan por política.
   - **Fin de Año Fiscal**: caducan al cierre del año fiscal.
   - **Aniversario**: caducan en el aniversario del empleado.
   - **Fecha Personalizada**: caducan en la fecha indicada.

   > Nota: la regla queda registrada en la política y se aplica cuando el proceso de vencimientos está habilitado.

7. Configure el **Uso**:
   - **Tipo de Unidad**: Días u Horas
   - **Contar Fines de Semana**: Si se incluyen en el cálculo
   - **Contar Feriados**: Si se incluyen en el cálculo
   - **Permitir Unidades Parciales**: Si se permiten fracciones
   - **Regla de Redondeo**: Más cercano, hacia arriba o hacia abajo
   - **Pagar al Terminar**: Si se pagan vacaciones al terminar relación laboral

   **Efecto de las opciones de uso**:
   - **Tipo de Unidad**: define cómo se registran saldos y solicitudes (días u horas).
   - **Contar Fines de Semana / Feriados**: define si esos días se incluyen en el conteo.
   - **Permitir Unidades Parciales**: habilita el uso de fracciones.
   - **Regla de Redondeo**: se usa cuando hay fracciones y se aplica al registrar o calcular las unidades.

   **Casos límite**:
   - Las reglas de **vencimiento** y **redondeo** requieren un proceso activo que las aplique.
   - Si no se ejecuta dicho proceso, la política queda registrada pero no afecta el saldo automáticamente.

8. Haga clic en **Guardar**

#### Ejemplos de Configuración

**Nicaragua (Estándar):**
- Método: Periódico
- Tasa: 1.25 días/mes (15 días al año)
- Frecuencia: Mensual
- Unidad: Días
- Contar fines de semana y feriados: Sí
- Vencimiento: 12 meses después del aniversario

**USA (Por Horas):**
- Método: Proporcional
- Base: Horas trabajadas
- Tasa: 0.025 (1 hora por cada 40 trabajadas)
- Frecuencia: Mensual
- Unidad: Horas
- Permitir fracciones: Sí

**Por Antigüedad:**
- Método: Por Antigüedad
- Niveles:
  - 0-1 años: 10 días
  - 2-5 años: 15 días
  - 6+ años: 20 días
- Frecuencia: Anual

### Paso 2: Crear Cuentas de Vacaciones

Una vez creada la política, debe asignar cuentas de vacaciones a los empleados:

1. Navegue a **Vacaciones → Cuentas de Vacaciones**
2. Haga clic en **Nueva Cuenta**
3. Seleccione:
   - **Empleado**: El empleado al que pertenece la cuenta
   - **Política**: La política que rige esta cuenta
   - **Balance Inicial**: Si el empleado ya tiene vacaciones acumuladas
4. Haga clic en **Guardar**

**Nota**: El balance inicial se registrará como una entrada de tipo ADJUSTMENT en el libro mayor.

## Uso Diario

### ⚠️ IMPORTANTE: Días Calendario vs. Días de Vacaciones

**Distinción Crítica**: El sistema distingue entre:

1. **Período de Descanso (Días Calendario)**: Las fechas reales de ausencia del empleado
2. **Días/Horas a Descontar**: La cantidad real que se descuenta del saldo de vacaciones

**Ejemplo Real**:
- Un empleado toma **viernes y lunes** de descanso
- Período calendario: **4 días** (viernes, sábado, domingo, lunes)
- Según política de la empresa, solo se descuentan **2 días** de vacaciones
- El sistema permite especificar ambos valores por separado

Esta flexibilidad es esencial para adaptarse a diferentes políticas empresariales y legislaciones.

### Registrar Vacaciones

Hay tres formas de registrar vacaciones:

#### Opción 1: Registro Directo de Vacaciones Descansadas (Recomendado)

Esta es la forma más directa y común para registrar vacaciones que ya fueron tomadas. **IMPORTANTE**: Las vacaciones siempre se registran como una novedad (NominaNovedad) usando la infraestructura existente del sistema.

1. En el Dashboard de Vacaciones, haga clic en **Registrar Vacaciones Descansadas**
2. Complete el formulario:
   - **Empleado**: Seleccione el empleado que tomó las vacaciones
   - **Fecha Inicio del Descanso**: Primer día calendario de ausencia
   - **Fecha Fin del Descanso**: Último día calendario de ausencia
   - **Días/Horas a Descontar**: **CRÍTICO** - Cantidad real a descontar del saldo según política
   - **Tipo de Concepto**: Seleccione Percepción o Deducción
   - **Percepción/Deducción**: **REQUERIDO** - Seleccione el concepto de nómina asociado
   - **Observaciones**: Notas adicionales
3. Haga clic en **Registrar Vacaciones**

**Asociación con Percepción o Deducción**:
- **Deducción**: Si las vacaciones se descuentan del salario (ausencias no pagadas)
- **Percepción**: Si las vacaciones se pagan como ingreso adicional (pago de vacaciones)

La novedad debe estar asociada a un concepto existente para que el sistema pueda realizar los cálculos correctamente al procesar la nómina.

**¿Qué sucede?**
- Se descuenta automáticamente el saldo de la cuenta del empleado
- Se crea una entrada en el libro mayor de vacaciones
- Se crea una **novedad de nómina** (NominaNovedad) asociada al concepto seleccionado
- Al calcular la nómina del empleado, la novedad se procesa normalmente
- El registro de vacaciones queda aprobado y vinculado a la novedad

**Ejemplo de Uso**:
```
Empleado: Juan Pérez
Fecha Inicio: 15/01/2025 (viernes)
Fecha Fin: 18/01/2025 (lunes)
Días a Descontar: 2.00
Tipo Concepto: Deducción
Deducción: AUSENCIA - Ausencia por vacaciones

Resultado: 
- Se descuentan 2 días del saldo (no 4 días calendario)
- Se crea una novedad de tipo deducción asociada a AUSENCIA
- Al calcular la próxima nómina, se procesará la deducción
```

#### Opción 2: Solicitud con Aprobación (Para Planificación)

Para solicitudes que requieren aprobación previa:

1. Navegue a **Vacaciones → Solicitudes de Vacaciones**
2. Haga clic en **Nueva Solicitud**
3. Complete el formulario:
   - **Empleado**: Seleccione el empleado
   - **Fecha de Inicio**: Primer día de vacaciones
   - **Fecha de Fin**: Último día de vacaciones
   - **Días/Horas a Descontar**: Cantidad real a descontar (puede diferir de días calendario)
   - **Observaciones**: Notas adicionales
4. Haga clic en **Solicitar**

La solicitud quedará en estado **Pendiente** hasta que un administrador la apruebe.

#### Opción 3: A través de Novedades de Nómina

1. Al crear una novedad en la nómina, marque la casilla **Es Descanso de Vacaciones**
2. Complete:
   - **Valor/Cantidad**: Días u horas a descontar del saldo
   - **Fechas de Descanso**: Período calendario del descanso
3. La novedad se vinculará automáticamente con el módulo de vacaciones

**Nota**: La Opción 1 (Registro Directo) es más conveniente ya que crea automáticamente tanto el registro de vacaciones como la novedad de nómina.

### Aprobar/Rechazar Solicitudes

1. Navegue a **Vacaciones → Solicitudes de Vacaciones**
2. Filtre por **Pendientes**
3. Haga clic en el icono de "Ver" de la solicitud
4. Revise los detalles, incluyendo el balance actual del empleado
5. Haga clic en:
   - **Aprobar**: Para aprobar la solicitud
   - **Rechazar**: Para rechazarla (debe indicar el motivo)

**Importante**: Al aprobar una solicitud:
- Se crea automáticamente una entrada en el libro mayor
- Se reduce el balance de vacaciones del empleado
- La solicitud cambia a estado **Aprobado**

### Consultar Balance de Vacaciones

1. Navegue a **Vacaciones → Cuentas de Vacaciones**
2. Busque el empleado en la lista
3. Haga clic en el icono de "Ver" para ver detalles
4. Verá:
   - Balance actual en un card destacado
   - Información de la cuenta y política
   - Solicitudes pendientes
   - Historial completo de movimientos

## Integración con Nómina

### Acumulación Automática

Cuando ejecute una nómina, el sistema automáticamente:

1. **Identifica empleados con cuentas de vacaciones** asociadas a la planilla
2. **Calcula la acumulación** según la política:
   - Periódica: Cantidad fija por período
   - Proporcional: Basado en días/horas trabajadas
   - Por Antigüedad: Según años de servicio
3. **Verifica límites** (balance máximo, días mínimos de servicio)
4. **Crea entrada en el libro mayor** de tipo ACCRUAL
5. **Actualiza el balance** de la cuenta

**Ejemplo de Log en Nómina:**
```
Acumuladas 1.25 unidades de vacaciones para empleado EMP-ABC123
```

### Procesamiento de Vacaciones Tomadas

Si hay novedades de tipo "descanso de vacaciones" en el período:

1. El sistema **verifica que estén aprobadas**
2. **Crea entrada en el libro mayor** de tipo USAGE
3. **Reduce el balance** de la cuenta
4. **Cambia el estado** de la solicitud a "Disfrutado"

**Ejemplo de Log en Nómina:**
```
Procesadas 5.00 unidades de vacaciones usadas para empleado EMP-ABC123
```

### Crear Novedades de Vacaciones

Al crear o editar una nómina, puede agregar novedades de vacaciones:

1. En la gestión de novedades, marque **Es Descanso de Vacaciones**
2. Complete las fechas de inicio y fin
3. Especifique la cantidad de unidades
4. Al ejecutar la nómina, el sistema procesará automáticamente las vacaciones

## Casos de Uso Especiales

### Ajuste Manual de Balance

Si necesita ajustar manualmente el balance de un empleado (error, corrección, etc.):

1. Navegue a **Vacaciones → Cuentas de Vacaciones**
2. Vea los detalles de la cuenta del empleado
3. Como administrador, puede crear un ajuste manual
4. El ajuste quedará registrado en el libro mayor como tipo ADJUSTMENT

### Vacaciones Adelantadas

Si la política permite balance negativo (`allow_negative = true`):

1. El empleado puede solicitar más vacaciones de las que tiene acumuladas
2. El balance quedará negativo
3. Se compensará con futuras acumulaciones

### Pago de Vacaciones al Terminar

Cuando un empleado termina su relación laboral:

1. Si la política tiene `payout_on_termination = true`
2. El sistema generará automáticamente:
   - Entrada en el libro mayor de tipo PAYOUT
   - Balance queda en 0
   - Se integra con la nómina de liquidación

### Vencimiento de Vacaciones

Según la regla de vencimiento configurada:

1. El sistema identificará vacaciones vencidas
2. Creará entradas de tipo EXPIRATION
3. Reducirá el balance automáticamente

## Reportes y Consultas

### Consultar Historial de Movimientos

1. Abra los detalles de una cuenta de vacaciones
2. En la sección "Historial de Movimientos" verá:
   - Fecha de cada movimiento
   - Tipo (Acumulación, Uso, Ajuste, etc.)
   - Cantidad (+ o -)
   - Balance después del movimiento
   - Origen y observaciones

### Dashboard de Vacaciones

1. Navegue a **Vacaciones**
2. El dashboard muestra:
   - Total de políticas activas
   - Total de cuentas activas
   - Solicitudes pendientes
   - Actividad reciente

### Filtrar Solicitudes

En la lista de solicitudes puede filtrar por:
- **Todas**: Ver todas las solicitudes
- **Pendientes**: Solo las que esperan aprobación
- **Aprobadas**: Solicitudes aprobadas
- **Rechazadas**: Solicitudes rechazadas

## Mejores Prácticas

1. **Asocie políticas a planillas**: Esto permite tener reglas diferentes para distintos países o tipos de empleados

2. **Revise las solicitudes regularmente**: Las solicitudes pendientes aparecen en el dashboard

3. **Verifique balances antes de aprobar**: El sistema muestra el balance actual al revisar una solicitud

4. **Use novedades de vacaciones**: Integre las vacaciones con el flujo normal de la nómina

5. **Consulte el libro mayor**: Para auditoría completa de los movimientos de vacaciones

6. **Configure correctamente las políticas**: Tome tiempo para configurar las políticas según la legislación local

7. **Cargue saldos iniciales al implementar**: Use la carga masiva desde Excel para empresas con muchos empleados, facilita la migración al sistema

8. **Revise regularmente el libro mayor**: Para mantener auditoría completa y detectar posibles inconsistencias

7. **Documente ajustes manuales**: Siempre agregue observaciones en ajustes manuales

## Solución de Problemas

### El empleado no tiene cuenta de vacaciones

**Problema**: Al intentar crear una solicitud, aparece error de cuenta no encontrada.

**Solución**: Cree una cuenta de vacaciones para el empleado en **Vacaciones → Cuentas de Vacaciones**.

### No se acumulan vacaciones en la nómina

**Problema**: Después de ejecutar la nómina, no se acumularon vacaciones.

**Verificar**:
1. ¿El empleado tiene una cuenta de vacaciones activa?
2. ¿La cuenta está asociada a una política de la planilla?
3. ¿El empleado cumple con los días mínimos de servicio?
4. ¿Se alcanzó el balance máximo?

### Balance insuficiente para solicitud

**Problema**: No se puede aprobar la solicitud porque el balance es insuficiente.

**Soluciones**:
- Si la política permite, habilite `allow_negative` para permitir adelantos
- Rechace la solicitud y comunique al empleado
- Realice un ajuste manual si corresponde

## Auditoría y Cumplimiento Legal

El módulo de vacaciones está diseñado para cumplir con requisitos legales:

1. **Trazabilidad Completa**: Cada movimiento queda registrado en el libro mayor
2. **Inmutabilidad**: Los registros del libro mayor no se pueden modificar
3. **Auditoría**: Se registra quién y cuándo realizó cada acción
4. **Determinismo**: Dado el mismo conjunto de eventos, el balance es siempre el mismo
5. **Documentación**: Todo ajuste manual debe tener observaciones

## Preguntas Frecuentes

**¿Puedo tener múltiples políticas para una misma empresa?**

Sí. Puede asociar políticas diferentes a planillas diferentes, incluso dentro de la misma empresa. Esto es útil para manejar distintos países o tipos de empleados.

**¿Qué pasa si cambio una política después de que ya tiene cuentas asociadas?**

Los cambios en la política solo afectan acumulaciones futuras. Los registros históricos en el libro mayor permanecen inmutables.

**¿Puedo eliminar una cuenta de vacaciones?**

No se recomienda eliminar cuentas con historial. En su lugar, márquelas como inactivas.

**¿Se pueden revertir movimientos del libro mayor?**

No, el libro mayor es inmutable. Para corregir errores, debe crear un nuevo ajuste con el valor opuesto.

**¿Cómo manejo empleados part-time?**

Configure una política con acumulación proporcional basada en horas trabajadas.

## Soporte

Para más información o soporte técnico, consulte:
- [Documentación Técnica del Módulo de Vacaciones](../modulo-vacaciones.md)
- [Repositorio GitHub](https://github.com/williamjmorenor/coati)
- [Reporte de Problemas](https://github.com/williamjmorenor/coati/issues)
