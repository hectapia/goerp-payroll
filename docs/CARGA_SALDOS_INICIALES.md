# Carga de Saldos Iniciales de Vacaciones

## Descripción General

Esta funcionalidad permite cargar los saldos de vacaciones acumulados por los empleados al momento de implementar el sistema. Es esencial para empresas que ya tienen empleados con vacaciones devengadas antes de comenzar a usar GoERP Payroll.

## Casos de Uso

### 1. Empresas Pequeñas (< 20 empleados)
**Solución**: Formulario Individual

- Navegue a **Vacaciones → Dashboard → Carga Individual**
- Ingrese un empleado a la vez
- Ideal para correcciones o cargas puntuales

### 2. Empresas Medianas y Grandes (20+ empleados)
**Solución**: Carga Masiva desde Excel

- Prepare un archivo Excel con los datos
- Navegue a **Vacaciones → Dashboard → Carga Masiva (Excel)**
- Procese todos los empleados en una sola operación
- Obtenga un reporte detallado de éxitos y errores

## Formato de Excel

### Estructura del Archivo

| Columna | Campo                | Tipo              | Requerido | Ejemplo            |
|---------|---------------------|-------------------|-----------|-------------------|
| A       | Código Empleado     | Texto             | Sí        | EMP001            |
| B       | Saldo Inicial       | Número decimal    | Sí        | 15.5              |
| C       | Fecha de Corte      | Fecha (DD/MM/YYYY)| Sí        | 31/12/2024        |
| D       | Observaciones       | Texto             | No        | Saldo inicial 2024|

### Ejemplo de Archivo Excel

```
EMP001    15.5    31/12/2024    Saldo inicial al implementar sistema
EMP002    20.0    31/12/2024    Vacaciones acumuladas 2024
EMP003    8.75    31/12/2024    
EMP004    12.0    31/12/2024    Empleado con 2 años de antigüedad
```

**Nota**: La primera fila debe contener datos (no encabezados).
**Límite de carga**: El archivo está limitado a ~1000 filas por carga (configurable vía `MAX_CONTENT_LENGTH`).

## Validaciones del Sistema

### Validaciones Automáticas

El sistema valida automáticamente:

1. ✅ **Empleado existe**: El código de empleado debe corresponder a un empleado activo
2. ✅ **Cuenta de vacaciones existe**: El empleado debe tener una cuenta de vacaciones activa
3. ✅ **Cuenta sin movimientos**: La cuenta no debe tener entradas previas en el ledger
4. ✅ **Formato de fecha**: La fecha debe estar en formato DD/MM/YYYY
5. ✅ **Saldo válido**: El saldo debe ser un número positivo o cero

### Mensajes de Error Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Empleado XXX no encontrado" | El código no existe o está inactivo | Verificar código o activar empleado |
| "No tiene cuenta de vacaciones activa" | Falta crear la cuenta | Crear cuenta en Vacaciones → Cuentas |
| "Ya tiene movimientos registrados" | La cuenta tiene historial | Solo se permiten saldos iniciales en cuentas nuevas |
| "Formato de fecha inválido" | Fecha incorrecta | Usar formato DD/MM/YYYY |

## Proceso de Implementación Recomendado

### Paso 1: Preparación (Antes de Cargar Saldos)

1. Cree las políticas de vacaciones necesarias
2. Cree las cuentas de vacaciones para todos los empleados activos
3. Verifique que todas las cuentas estén correctamente asociadas a sus políticas

### Paso 2: Preparar Datos

1. Compile la información de saldos de vacaciones de su sistema anterior
2. Determine la fecha de corte (típicamente: fecha de go-live del sistema)
3. Prepare el archivo Excel siguiendo el formato especificado
4. Revise los datos para evitar errores

### Paso 3: Ejecutar Carga

**Opción A - Individual:**
```
Dashboard → Carga Individual
→ Seleccionar empleado
→ Ingresar saldo y fecha
→ Guardar
```

**Opción B - Masiva:**
```
Dashboard → Carga Masiva (Excel)
→ Subir archivo Excel
→ Revisar reporte de resultados
→ Corregir errores si los hay
→ Re-ejecutar con empleados fallidos
```

### Paso 4: Verificación

1. Revise el reporte de carga (éxitos vs errores)
2. Verifique algunas cuentas manualmente:
   - Navegue a **Vacaciones → Cuentas**
   - Abra una cuenta
   - Verifique que el balance coincida con el saldo cargado
   - Revise el historial del ledger (debe tener una entrada de tipo ADJUSTMENT)

## Características Técnicas

### Registro en el Libro Mayor (Ledger)

Cada carga de saldo inicial crea una entrada inmutable en el ledger:

- **Tipo**: `ADJUSTMENT`
- **Fuente**: `initial_balance` (individual) o `initial_balance_bulk` (masiva)
- **Cantidad**: El saldo inicial especificado
- **Fecha**: La fecha de corte proporcionada
- **Usuario**: El administrador que realizó la carga
- **Observaciones**: Las notas proporcionadas

### Principio de Inmutabilidad

El sistema respeta el principio:

```
Balance Actual = SUMA(todas las entradas del ledger)
```

Por lo tanto:
- No se puede "editar" un saldo inicial
- Para corregir, debe crear un nuevo ajuste
- El balance siempre es auditable y rastreable

### Trazabilidad y Auditoría

Toda carga queda registrada con:
- ✅ Usuario que realizó la operación
- ✅ Fecha y hora de la operación
- ✅ Fuente de los datos (individual/Excel)
- ✅ Observaciones del usuario

## Limitaciones

### Restricciones del Sistema

1. **Solo para cuentas nuevas**: No se puede cargar saldo inicial si la cuenta ya tiene movimientos
2. **Una sola vez**: Idealmente, la carga inicial se hace una sola vez durante la implementación
3. **Requiere cuenta activa**: El empleado debe tener una cuenta de vacaciones creada previamente

### Correcciones Post-Carga

Si necesita corregir un saldo inicial después de cargarlo:

1. **Opción A - Ajuste Manual**:
   - Use la funcionalidad de ajustes en el módulo de vacaciones
   - Cree un ajuste positivo o negativo según sea necesario
   - Documente bien la razón del ajuste

2. **Opción B - Reconstruir** (solo si no hay más movimientos):
   - Contacte al administrador del sistema
   - Elimine la cuenta y recréela
   - Vuelva a cargar el saldo inicial correcto

## Soporte y Troubleshooting

### Problemas Comunes

**1. "El archivo Excel no se procesa"**
- Verifique que sea .xlsx o .xls
- Asegúrese de que la primera fila contenga datos (no encabezados)
- Revise que las columnas estén en el orden correcto

**2. "Muchos errores al cargar"**
- Exporte el reporte de errores
- Corrija los datos problemáticos
- Cree un nuevo Excel solo con los registros fallidos
- Re-ejecute la carga

**3. "Balance no coincide"**
- Verifique el historial del ledger
- Confirme que no haya movimientos adicionales
- Use la suma del ledger como fuente de verdad

### Contacto

Para soporte adicional:
- Documentación técnica: `docs/modulo-vacaciones.md`
- Guía de usuario: `docs/guia/vacaciones.md`
- Repositorio: https://github.com/williamjmorenor/coati
- Issues: https://github.com/williamjmorenor/coati/issues

## Ejemplos Prácticos

### Ejemplo 1: Empresa Pequeña (10 empleados)

**Escenario**: Empresa con 10 empleados implementando el sistema el 1 de enero de 2025.

**Proceso**:
1. Cree 10 cuentas de vacaciones
2. Use el formulario individual para cada empleado
3. Fecha de corte: 31/12/2024
4. Verificación: Revise cada cuenta manualmente

**Tiempo estimado**: 15-20 minutos

### Ejemplo 2: Empresa Mediana (150 empleados)

**Escenario**: Empresa manufacturera con 150 empleados, migración desde sistema legacy.

**Proceso**:
1. Exporte datos del sistema anterior
2. Transforme a formato Excel requerido
3. Valide datos (códigos de empleado, formatos)
4. Use carga masiva
5. Revise reporte de errores
6. Corrija y re-ejecute para registros fallidos

**Tiempo estimado**: 1-2 horas (incluyendo preparación)

### Ejemplo 3: Consolidado Multi-País (500+ empleados)

**Escenario**: Holding con operaciones en Nicaragua, Costa Rica y Guatemala.

**Proceso**:
1. Cree políticas por país/planilla
2. Cree cuentas asociadas a cada política
3. Prepare Excel por país (facilita troubleshooting)
4. Ejecute carga masiva por país
5. Consolide reportes de resultados
6. Gestione errores país por país

**Tiempo estimado**: 3-4 horas (incluyendo preparación y validación)

## Checklist de Implementación

- [ ] Políticas de vacaciones creadas y configuradas
- [ ] Cuentas de vacaciones creadas para todos los empleados
- [ ] Datos de saldos iniciales compilados y validados
- [ ] Fecha de corte definida
- [ ] Archivo Excel preparado (si aplica carga masiva)
- [ ] Carga ejecutada exitosamente
- [ ] Reporte de errores revisado y corregido
- [ ] Verificación de muestra realizada
- [ ] Documentación de la carga guardada para auditoría
- [ ] Usuarios informados sobre el nuevo sistema

---

**Versión**: 1.0  
**Última actualización**: Diciembre 2024  
**Autor**: GoERP Payroll Development Team
