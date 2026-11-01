# Glosario

Términos y conceptos utilizados en GoERP Payroll.

## A

### Adelanto Salarial
Porción del salario pagada anticipadamente al empleado. Se descuenta en la siguiente nómina o en cuotas acordadas.

### Aguinaldo
También conocido como "treceavo mes". Prestación equivalente a un mes de salario que se paga anualmente. En Nicaragua se paga en diciembre.

### Acumulado Anual
Registro que mantiene los valores acumulados de salario e impuestos de un empleado durante el año fiscal. Utilizado para cálculos progresivos como el IR.

## B

### Base de Cálculo
El monto sobre el cual se aplica un porcentaje para calcular una percepción, deducción o prestación. Puede ser: salario base, salario bruto, salario gravable o salario neto.

### Base Gravable
Monto sobre el cual se calculan los impuestos. Se obtiene restando las deducciones "antes de impuesto" del salario bruto.

### Background Processing (Procesamiento en Segundo Plano)
Sistema que ejecuta tareas de larga duración (como calcular nóminas grandes) en segundo plano sin bloquear la interfaz de usuario. Proporciona feedback en tiempo real del progreso.

## C

### Campo Personalizado
Campo adicional definido por el usuario para almacenar información específica de empleados que no está incluida en los campos estándar. Ejemplos: tipo de sangre, contacto de emergencia, talla de uniforme.

### Centro de Costos
Unidad organizacional o proyecto al que se imputan los gastos de nómina. Permite segmentar el costo de personal por departamento o proyecto.

### Cuota
Monto fijo que se descuenta periódicamente de un préstamo o adelanto hasta saldar la deuda.

## D

### Deducción
Concepto que se resta del salario bruto del empleado. Ejemplos: INSS laboral, IR, cuota sindical, préstamos.

### Dramatiq
Sistema de colas de tareas distribuido que usa Redis como backend. Utilizado para procesamiento en segundo plano en entornos de producción.

### Deducción Antes de Impuesto
Deducción que se aplica antes de calcular el impuesto sobre la renta, reduciendo así la base gravable. Ejemplo: INSS laboral.

### Deducción Obligatoria
Deducción que se aplica aunque el salario disponible no sea suficiente. Se usa para cumplir obligaciones legales.

## E

### Empleado
Persona que trabaja para la empresa y recibe un salario procesado a través del sistema de nómina.

### Estado de Nómina
Situación en que se encuentra una nómina:

- **Generado**: Calculada, pendiente de revisión
- **Aprobado**: Revisada y autorizada para pago
- **Aplicado**: Pagada/completada

## F

### Fórmula
Expresión matemática utilizada para calcular el monto de una percepción, deducción o prestación. Puede incluir variables como salario_base, días_trabajados, etc.

### Fecha de Alta
Fecha en que el empleado comenzó a trabajar en la empresa. Importante para cálculos de antigüedad y prestaciones.

### Fecha de Baja
Fecha en que el empleado dejó de trabajar en la empresa.

## G

### Gravable
Que está sujeto al pago de impuestos. Una percepción gravable aumenta la base sobre la cual se calcula el IR.

## I

### INATEC
Instituto Nacional Tecnológico de Nicaragua. El aporte al INATEC es del 2% del salario bruto, pagado por el empleador.

### Indemnización
Compensación que se paga al empleado al terminar la relación laboral. En Nicaragua, es de un mes de salario por año trabajado.

### INSS
Instituto Nicaragüense de Seguridad Social. Administra el sistema de seguridad social en Nicaragua.

### INSS Laboral
Aporte del trabajador al INSS (7% del salario bruto). Es una deducción.

### INSS Patronal
Aporte del empleador al INSS (22.5% en régimen integral). Es una prestación/costo patronal.

### IR (Impuesto sobre la Renta)
Impuesto que se aplica sobre los ingresos del empleado. En Nicaragua se calcula con una tabla progresiva sobre la expectativa salarial anual.

## M

### Moneda
Unidad monetaria en la que se expresan y pagan los salarios. El sistema soporta múltiples monedas.

## N

### Nómina
Ejecución de una planilla para un período específico. Contiene el cálculo de salarios para todos los empleados asignados.

### NominaEmpleado
Registro del cálculo de nómina para un empleado específico en una ejecución de nómina.

### NominaDetalle
Registro individual de cada percepción, deducción o prestación aplicada a un empleado en una nómina.

### Novedad
Evento o cambio que afecta la nómina de un empleado en un período específico. Ejemplos: horas extras trabajadas, días de ausencia, bonos especiales.

## P

### Percepción
Concepto que se suma al salario base del empleado. Ejemplos: bonos, comisiones, horas extras, viáticos.

### Período Fiscal
Año fiscal para efectos de cálculos tributarios. Puede coincidir o no con el año calendario.

### Planilla
Configuración maestra que define qué empleados se procesan, qué conceptos se aplican y cómo se calculan. Es el elemento central del sistema.

### Prestación
Aporte o beneficio que paga el empleador pero que **NO** afecta el salario neto del empleado. Son costos patronales. Ejemplos: INSS patronal, vacaciones, aguinaldo.

### Préstamo
Monto otorgado al empleado que se recupera en cuotas periódicas descontadas de la nómina.

### Prioridad
Número que determina el orden en que se aplican las deducciones. Menor número = mayor prioridad (se aplica primero).

## R

### Recurrente
Que se aplica automáticamente en cada período de nómina sin necesidad de configuración adicional.

### Regla de Cálculo (ReglaCalculo)
Esquema JSON configurable que define lógica de cálculo compleja, como tablas de impuestos progresivos o seguridad social con topes. Permite definir cálculos por tramos sin necesidad de programar.

## S

### Salario Base
Monto mensual acordado con el empleado, antes de cualquier adición o descuento.

### Salario Bruto
Salario base más todas las percepciones. Es el total antes de deducciones.

```
Salario Bruto = Salario Base + Percepciones
```

### Salario Gravable
Monto sobre el cual se calcula el impuesto. Es el salario bruto menos las deducciones antes de impuesto.

```
Salario Gravable = Salario Bruto - Deducciones Antes de Impuesto
```

### Salario Neto
Monto que recibe el empleado después de todas las deducciones.

```
Salario Neto = Salario Bruto - Total Deducciones
```

## T

### Tipo de Cambio
Tasa de conversión entre dos monedas. Se usa cuando el empleado tiene salario en una moneda diferente a la planilla.

### Tipo de Planilla
Configuración que define la periodicidad de pago (mensual, quincenal, semanal) y parámetros del período fiscal.

### Tope
Monto máximo sobre el cual se aplica un cálculo. Por ejemplo, el INSS patronal tiene un tope salarial sobre el cual se calcula.

## U

### ULID
Universally Unique Lexicographically Sortable Identifier. Identificador único usado para las claves primarias en la base de datos.

## V

### Vacaciones
Período de descanso remunerado al que tiene derecho el empleado. En Nicaragua son 30 días al año (2.5 días por mes trabajado).

### Vigencia
Período de tiempo durante el cual una percepción, deducción o prestación es válida. Definido por las fechas "Vigente Desde" y "Válido Hasta".
