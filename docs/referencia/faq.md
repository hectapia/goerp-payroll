# Preguntas Frecuentes (FAQ)

Respuestas a las preguntas más comunes sobre GoERP Payroll.

## General

### ¿Qué es GoERP Payroll?

GoERP Payroll es un sistema de administración de nóminas y planillas que permite gestionar el proceso completo de pago de salarios, incluyendo percepciones, deducciones, prestaciones patronales y préstamos a empleados.

### ¿Qué tipo de empresas pueden usar GoERP Payroll?

El sistema está diseñado para empresas de cualquier tamaño que necesiten procesar nóminas. Es especialmente útil para empresas en Nicaragua y Centroamérica, aunque es configurable para cualquier país.

### ¿Requiere conexión a internet?

No necesariamente. GoERP Payroll puede instalarse en un servidor local sin conexión a internet. Solo necesita conexión si desea acceder desde ubicaciones remotas o usar servicios externos.

---

## Instalación y Configuración

### ¿Cuáles son los requisitos mínimos?

- Python 3.11 o superior
- 1 GB de RAM (recomendado 4 GB para producción)
- Base de datos SQLite (desarrollo) o PostgreSQL/MySQL (producción)

### ¿Cómo cambio la contraseña del administrador?

1. Inicie sesión como administrador
2. Navegue a **Configuración > Usuarios**
3. Edite el usuario administrador
4. Ingrese la nueva contraseña
5. Guarde los cambios

### ¿Cómo configuro el sistema para múltiples monedas?

1. Cree las monedas necesarias en **Configuración > Monedas**
2. Configure los tipos de cambio en **Configuración > Tipos de Cambio**
3. Al crear empleados, asigne la moneda de su salario
4. Al crear planillas, seleccione la moneda de pago

---

## Empleados

### ¿Cómo registro un nuevo empleado?

1. Navegue a **Personal > Empleados**
2. Haga clic en **Nuevo Empleado**
3. Complete la información requerida (nombre, identificación, salario, etc.)
4. Guarde el registro
5. Asigne el empleado a una planilla

### ¿Puedo tener un empleado en múltiples planillas?

Sí. Un empleado puede estar asignado a varias planillas si, por ejemplo, recibe pagos en diferentes periodicidades o monedas.

### ¿Qué pasa si un empleado renuncia?

1. Edite el registro del empleado
2. Complete la fecha de baja
3. Desmarque la casilla "Activo"
4. El empleado no será procesado en futuras nóminas

### ¿Cómo registro un aumento de salario?

1. Edite el registro del empleado
2. Modifique el campo "Salario Base"
3. El sistema mantiene un historial de cambios de salario

---

## Percepciones, Deducciones y Prestaciones

### ¿Cuál es la diferencia entre percepción, deducción y prestación?

| Concepto | Efecto en el Empleado | Quién Paga |
|----------|----------------------|------------|
| **Percepción** | Suma al salario | Empresa al empleado |
| **Deducción** | Resta del salario | Empleado (se le descuenta) |
| **Prestación** | No afecta el salario neto | Empresa (costo patronal) |

### ¿Por qué las prestaciones no afectan el salario del empleado?

Las prestaciones son costos que asume el empleador (INSS patronal, INATEC, provisiones). El empleado no las ve en su recibo como descuentos; son obligaciones de la empresa.

### ¿Cómo configuro el orden de las deducciones?

Al asignar una deducción a una planilla, configure el campo **Prioridad**:
- Número menor = mayor prioridad (se aplica primero)
- Recomendación: Use 1-100 para deducciones legales, 101-300 para préstamos, 301+ para voluntarias

### ¿Qué pasa si el salario no alcanza para todas las deducciones?

Las deducciones se aplican en orden de prioridad. Si el saldo es insuficiente:
- Las deducciones de baja prioridad se omiten
- Se genera una advertencia en la nómina
- Las deducciones marcadas como "obligatorias" se aplican aunque generen saldo negativo

---

## Préstamos y Adelantos

### ¿Cómo registro un préstamo a un empleado?

1. Acceda al módulo de Adelantos/Préstamos
2. Cree un nuevo registro con el monto y número de cuotas
3. Apruebe el préstamo configurando el monto por cuota
4. El sistema deducirá automáticamente las cuotas en cada nómina

### ¿Se deducen automáticamente los préstamos?

Sí, si la planilla tiene activada la opción "Aplicar Préstamos Automáticamente". El sistema busca préstamos aprobados con saldo pendiente y deduce la cuota configurada.

### ¿Qué pasa si el empleado quiere pagar anticipadamente?

Puede registrar un abono manual en el préstamo para reducir el saldo pendiente. Si el saldo llega a cero, el préstamo se marca como pagado.

### ¿Qué pasa con los préstamos si el empleado renuncia?

El préstamo permanece registrado. Debe gestionar el cobro del saldo pendiente manualmente o incluirlo en la liquidación del empleado.

---

## Nómina

### ¿Cómo ejecuto una nómina?

1. Configure la planilla con empleados, percepciones, deducciones y prestaciones
2. Navegue a la planilla y haga clic en **Ejecutar Nómina**
3. Configure las fechas del período
4. Haga clic en **Ejecutar**
5. Revise, apruebe y aplique la nómina

### ¿Puedo modificar una nómina después de generarla?

Una vez generada, la nómina no se puede modificar directamente. Si hay errores:
- Si está en estado "Generado": Puede eliminar la nómina y ejecutarla nuevamente
- Si está "Aprobada" o "Aplicada": Debe hacer ajustes en la siguiente nómina

### ¿Cómo registro horas extras?

Las horas extras se registran como novedades de nómina. Antes de ejecutar la nómina:
1. Registre las horas extras por empleado
2. Al ejecutar, el sistema multiplicará las horas por el valor configurado

### ¿Por qué un empleado no aparece en la nómina?

Verifique:
- El empleado está activo
- El empleado está asignado a la planilla
- La fecha de inicio de asignación es anterior al período de nómina

### ¿Cómo veo nóminas anteriores?

1. Navegue a la planilla
2. Haga clic en **Ver Nóminas**
3. Verá el historial de todas las nóminas ejecutadas

---

## Impuestos

### ¿Cómo se calcula el IR?

El IR se calcula sobre la base gravable (salario bruto menos deducciones antes de impuesto). El método exacto depende de la configuración:
- Porcentaje fijo
- Tabla progresiva (configurada como regla de cálculo)

### ¿El sistema considera los valores acumulados para el IR?

Sí. El sistema mantiene un registro de valores acumulados (AcumuladoAnual) que se actualiza con cada nómina. Esto permite cálculos progresivos correctos.

### ¿Qué deducciones van antes del IR?

Generalmente:
- INSS laboral
- Aportes a fondos de pensión
- Seguros médicos obligatorios

Configure estas deducciones con la opción "Antes de Impuesto" activada.

---

## Reportes y Auditoría

### ¿Qué información se guarda para auditoría?

El sistema registra:
- Quién creó/modificó cada registro
- Fecha y hora de cambios
- Detalle completo de cada nómina (incluye snapshot de datos del empleado)
- Tipo de cambio utilizado
- Historial de abonos a préstamos

### ¿Puedo exportar la información de nómina?

El sistema genera reportes visuales. Para exportación, consulte las funcionalidades de impresión o generación de PDF disponibles.

---

## Características Avanzadas

### ¿Qué son los campos personalizados?

Los campos personalizados permiten extender la información de empleados con datos adicionales específicos de su organización, como tipo de sangre, contactos de emergencia, o cualquier información que necesite registrar.

Para más información, consulte la [Guía de Campos Personalizados](../guia/campos-personalizados.md).

### ¿Qué son las reglas de cálculo?

Las reglas de cálculo son esquemas configurables para cálculos complejos como impuestos progresivos o seguridad social con topes. Permiten definir tablas de tramos y fórmulas estructuradas sin necesidad de programar.

Para más información, consulte la [Guía de Reglas de Cálculo](../guia/reglas-calculo.md).

### ¿Qué es el procesamiento en segundo plano?

Para nóminas grandes (más de 100 empleados por defecto), el sistema automáticamente procesa la nómina en segundo plano usando un sistema de colas. Esto evita que la interfaz se congele y proporciona feedback en tiempo real del progreso.

El umbral se puede ajustar con la variable de entorno `BACKGROUND_PAYROLL_THRESHOLD`.

Para más información, consulte la documentación del [Sistema de Colas](../queue_system.md) y [Procesamiento en Segundo Plano](../background-payroll-processing.md).

### ¿Cómo sé si mi nómina se está procesando en segundo plano?

Verá un mensaje que indica "La nómina está siendo calculada en segundo plano" y una barra de progreso mostrando cuántos empleados se han procesado del total. La página se actualiza automáticamente para mostrar el progreso.

### ¿Qué pasa si el procesamiento en segundo plano falla?

Si algunos empleados fallan al procesarse:
- El sistema continúa con los demás empleados
- Se registran los errores específicos por empleado
- Puede revisar los errores en el detalle de la nómina
- Los empleados exitosos mantienen sus cálculos

Si todo falla, puede intentar ejecutar la nómina nuevamente.

---

## Solución de Problemas

### Error: "La planilla no tiene empleados asignados"

1. Edite la planilla
2. En la sección Empleados, agregue al menos un empleado
3. Verifique que los empleados estén activos

### Error: "No se encontró tipo de cambio"

1. Navegue a **Configuración > Tipos de Cambio**
2. Cree un tipo de cambio para las monedas involucradas
3. Asegúrese de que la fecha sea anterior o igual a la fecha de cálculo

### Las deducciones no se aplican correctamente

1. Verifique la prioridad configurada
2. Revise si hay saldo disponible (las de baja prioridad se omiten)
3. Verifique las fechas de vigencia de la deducción
4. Revise las advertencias de la nómina

### El préstamo no se descuenta

1. Verifique que el estado del préstamo sea "Aprobado"
2. Verifique que tenga saldo pendiente > 0
3. Verifique que la planilla tenga "Aplicar Préstamos Automáticamente" activado
4. Revise la prioridad (puede omitirse por saldo insuficiente)

---

## Soporte

### ¿Dónde puedo reportar problemas?

Reporte problemas en el [repositorio de GitHub](https://github.com/williamjmorenor/coati/issues).

### ¿Hay documentación técnica disponible?

Esta documentación cubre el uso del sistema. Para documentación técnica de desarrollo, consulte el código fuente y los comentarios en el repositorio.
