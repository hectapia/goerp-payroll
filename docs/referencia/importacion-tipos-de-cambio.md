# Importación de Tipos de Cambio desde Excel

La aplicación permite importar múltiples tipos de cambio desde un archivo Excel, lo que facilita la carga masiva de tasas de conversión entre diferentes monedas.

## Formato del Archivo Excel

El archivo Excel debe contener las siguientes columnas en orden:

1. **Fecha**: Fecha del tipo de cambio
   - Formatos soportados: `YYYY-MM-DD` o `DD/MM/YYYY`
   - Ejemplo: `2024-01-15` o `15/01/2024`

2. **Moneda Base**: Código de la moneda origen
   - Debe ser un código de moneda válido registrado en el sistema (ej: `USD`, `NIO`, `EUR`)
   - No distingue entre mayúsculas y minúsculas

3. **Moneda Destino**: Código de la moneda destino
   - Debe ser un código de moneda válido registrado en el sistema
   - No distingue entre mayúsculas y minúsculas

4. **Tipo de Cambio**: Tasa de conversión
   - Puede tener hasta 4 decimales (el sistema soporta hasta 10 decimales)
   - Debe ser un número positivo mayor que cero
   - Ejemplo: `36.5423`, `1.0951`

## Estructura del Archivo

```
| Fecha      | Moneda Base | Moneda Destino | Tipo de Cambio |
|------------|-------------|----------------|----------------|
| 2024-01-15 | USD         | NIO            | 36.5423        |
| 2024-01-16 | USD         | NIO            | 36.5550        |
| 2024-01-17 | USD         | NIO            | 36.5678        |
| 2024-01-15 | EUR         | USD            | 1.0951         |
| 2024-01-16 | EUR         | USD            | 1.0965         |
```

## Características

- **Validación de datos**: El sistema valida cada fila antes de importarla
- **Actualización automática**: Si un tipo de cambio ya existe para la misma fecha y par de monedas, se actualiza con el nuevo valor
- **Reporte de errores**: Se muestran errores detallados para filas con datos inválidos
- **Transaccional**: Si ocurre un error crítico, no se importa ningún dato (se hace rollback)
- **Primera fila como encabezado**: La primera fila del archivo debe contener los encabezados de las columnas y será ignorada durante la importación

## Cómo Importar

1. Navegue a **Tipos de Cambio** en el menú principal
2. Haga clic en el botón **"Importar desde Excel"**
3. Seleccione su archivo Excel (.xlsx o .xls)
4. Haga clic en **"Importar"**
5. Revise el resumen de importación que muestra:
   - Cantidad de tipos de cambio creados
   - Cantidad de tipos de cambio actualizados
   - Errores encontrados (si los hay)

## Validaciones

El sistema valida:

- Formato del archivo (debe ser .xlsx o .xls)
- Existencia de las monedas en el sistema
- Formato de la fecha
- Tipo de cambio válido (número positivo)
- Que no falten columnas requeridas

## Errores Comunes

1. **"Moneda no encontrada"**: La moneda especificada no existe en el sistema. Debe crear la moneda primero en el módulo de **Monedas**.

2. **"Fecha inválida"**: El formato de la fecha no es reconocido. Use `YYYY-MM-DD` o `DD/MM/YYYY`.

3. **"Tasa debe ser mayor que cero"**: El tipo de cambio debe ser un número positivo.

4. **"Formato incorrecto"**: La fila no tiene las 4 columnas requeridas.

## Notas Importantes

- Las monedas deben estar registradas y activas en el sistema antes de importar tipos de cambio
- Los tipos de cambio se registran con el usuario que realiza la importación
- Si un tipo de cambio ya existe (misma fecha, moneda origen y destino), se actualiza en lugar de crear uno nuevo
- La precisión de hasta 4 decimales es importante para conversiones exactas de moneda
