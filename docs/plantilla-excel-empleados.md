# Plantilla Excel y Google Sheets para Carga Masiva de Empleados

## Descripción General

GoERP Payroll incorpora un sistema de **Carga Masiva de Empleados** mediante plantillas en formato **Microsoft Excel (`.xlsx`)** y **Valores Separados por Comas (`.csv`)**, diseñado para ser 100% compatible con **Google Sheets** y herramientas de hojas de cálculo modernas.

Esta funcionalidad está restringida **únicamente a usuarios con rol Administrador (`admin`)** para salvaguardar la integridad de la base de datos y la gobernanza de accesos.

---

## Acceso al Módulo

1. Inicie sesión con una cuenta de rol **Administrador**.
2. Navegue a **Personal > Empleados**.
3. En la barra superior, haga clic en el botón **Carga Masiva** (identificado con el icono de hoja de cálculo).
4. También puede acceder directamente a la URL: `/employee/bulk-upload`.

---

## Estructura de la Plantilla

El archivo descargable oficial (`plantilla_empleados_googlesheets.xlsx`) contiene **3 hojas estructuradas**:

### Hoja 1: `Empleados` (Datos Principales)

Contiene **34 columnas** organizadas temáticamente. Los encabezados en color **Azul GoERP** corresponden a campos obligatorios (`*`), mientras que los encabezados en color **Gris Pizarra** corresponden a campos opcionales.

| # | Columna | Tipo | Requerido | Descripción | Ejemplo |
|---|---------|------|-----------|-------------|---------|
| 1 | `codigo_empleado` | Texto | No | Código único interno (si se deja vacío, el sistema lo genera automáticamente) | `EMP-001` |
| 2 | `primer_nombre` | Texto | **Sí** | Primer nombre del empleado | `Juan` |
| 3 | `segundo_nombre` | Texto | No | Segundo nombre | `Carlos` |
| 4 | `primer_apellido` | Texto | **Sí** | Primer apellido (paterno) | `Pérez` |
| 5 | `segundo_apellido` | Texto | No | Segundo apellido (materno) | `López` |
| 6 | `tipo_identificacion` | Texto | No | Código del tipo de documento: `id_card`, `passport`, `residence_card`, `other` | `id_card` |
| 7 | `identificacion_personal` | Texto | **Sí** | Número único de cédula, DNI o pasaporte | `001-010190-0001A` |
| 8 | `fecha_nacimiento` | Fecha | No | Fecha de nacimiento en formato `YYYY-MM-DD` | `1990-01-15` |
| 9 | `genero` | Texto | No | Código de género: `male` (Masculino), `female` (Femenino), `other` (Otro) | `male` |
| 10 | `nacionalidad` | Texto | No | Nacionalidad o país de origen | `Nicaragüense` |
| 11 | `tipo_sangre` | Texto | No | Grupo sanguíneo: `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-` | `O+` |
| 12 | `estado_civil` | Texto | No | Estado civil: `single`, `married`, `divorced`, `widowed`, `common_law` | `single` |
| 13 | `codigo_empresa` | Texto | **Sí** | Código de la empresa activa a la que pertenecerá el empleado | `MHE` |
| 14 | `fecha_alta` | Fecha | **Sí** | Fecha de ingreso / contratación en formato `YYYY-MM-DD` | `2024-01-15` |
| 15 | `fecha_baja` | Fecha | No | Fecha de salida en formato `YYYY-MM-DD` (dejar vacío si está activo) | `2024-12-31` |
| 16 | `tipo_contrato` | Texto | No | Modalidad: `permanent`, `temporary`, `project_based`, `internship` | `permanent` |
| 17 | `cargo` | Texto | No | Título del puesto o cargo laboral | `Analista de Nómina` |
| 18 | `area` | Texto | No | Departamento o área funcional | `Recursos Humanos` |
| 19 | `centro_costos` | Texto | No | Centro de costos para contabilidad | `CC-101` |
| 20 | `salario_base` | Numérico | **Sí** | Salario base mensual pactado (formato decimal: `0.00`) | `1200.00` |
| 21 | `codigo_moneda` | Texto | **Sí** | Código ISO de la moneda pactada (e.g., `USD`, `NIO`, `CRC`, `MXN`) | `USD` |
| 22 | `activo` | Booleano | No | Estado del empleado: `SI`, `NO`, `1`, `0`, `TRUE`, `FALSE` (por defecto `SI`) | `SI` |
| 23 | `correo` | Texto | No | Correo electrónico de contacto institucional o personal | `juan.perez@empresa.com` |
| 24 | `telefono` | Texto | No | Número telefónico de contacto | `+505 8888-9999` |
| 25 | `direccion` | Texto | No | Dirección de domicilio | `Calle Central #123` |
| 26 | `banco` | Texto | No | Nombre de la entidad bancaria para dispersión | `Banco BAC` |
| 27 | `numero_cuenta_bancaria` | Texto | No | Número de cuenta o cuenta CLABE / IBAN | `987654321012` |
| 28 | `id_seguridad_social` | Texto | No | Número de seguro social (e.g. INSS, CCSS, IMSS) | `INSS-7890123` |
| 29 | `id_fiscal` | Texto | No | Identificación tributaria (RUC, RFC, NIT) | `001-010190-0001A` |
| 30 | `salario_acumulado` | Numérico | No | Salario acumulado fiscal previo si la implementación es a mitad de año | `0.00` |
| 31 | `impuesto_acumulado` | Numérico | No | IR o impuesto retenido acumulado previo si es implementación a mitad de año | `0.00` |
| 32 | `ultimo_salario_1` | Numérico | No | Salario del mes inmediatamente anterior (para cálculos de indemnización) | `1200.00` |
| 33 | `ultimo_salario_2` | Numérico | No | Salario de dos meses antes | `1200.00` |
| 34 | `ultimo_salario_3` | Numérico | No | Salario de tres meses antes | `1200.00` |

---

### Hoja 2: `Catalogos_Referencia`

Incluye los códigos canónicos admitidos por el sistema para evitar inconsistencias ortográficas:

- **Tipo de Documento**: `id_card` (Cédula/DNI), `passport` (Pasaporte), `residence_card` (Carnet de Residente), `other` (Otro).
- **Género**: `male` (Masculino), `female` (Femenino), `other` (Otro).
- **Tipo de Contrato**: `permanent` (Indefinido), `temporary` (Temporal), `project_based` (Por Obra), `internship` (Prácticas).
- **Estado Civil**: `single` (Soltero/a), `married` (Casado/a), `divorced` (Divorciado/a), `widowed` (Viudo/a), `common_law` (Unión Libre).
- **Tipo de Sangre**: `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-`.
- **Monedas**: Códigos ISO oficiales (`USD`, `NIO`, `CRC`, `MXN`, `EUR`, etc.).

---

### Hoja 3: `Instrucciones`

Contiene una guía rápida para el usuario sobre cómo descargar, diligenciar y exportar la hoja desde Google Sheets o Excel.

---

## Uso con Google Sheets

1. **Descargar la plantilla**: En la pantalla de carga masiva, haga clic en **Descargar Plantilla Excel (.xlsx)** o **Descargar Plantilla CSV (.csv)**.
2. **Abrir Google Drive / Google Sheets**:
   - Vaya a [sheets.google.com](https://sheets.google.com).
   - Cree una hoja en blanco y seleccione **Archivo > Importar > Subir**.
   - Arrastre el archivo `.xlsx` descargado.
3. **Completar la información**:
   - Ingrese los datos a partir de la fila 2 (puede reemplazar o eliminar las filas de ejemplo).
   - Respete el formato de fecha `YYYY-MM-DD` (ejemplo: `2024-05-15`).
4. **Descargar desde Google Sheets**:
   - Vaya a **Archivo > Descargar > Microsoft Excel (.xlsx)** o **Valores separados por comas (.csv)**.
5. **Subir a GoERP Payroll**:
   - Ingrese a `/employee/bulk-upload`.
   - Seleccione o arrastre el archivo generado y haga clic en **Procesar Carga Masiva**.

---

## Normalización Inteligente de Monedas

Para prevenir fallos por errores tipográficos comunes en los códigos de moneda, el cargador masivo normaliza automáticamente los siguientes términos:

| Valor Ingresado en Hoja | Código ISO Normalizado | Moneda Resultante |
|-------------------------|------------------------|-------------------|
| `MNX`, `PESO`, `PESOS` | `MXN` | Peso Mexicano |
| `DOLAR`, `DOLARES` | `USD` | Dólar Estadounidense |
| `CORDOBA`, `CORDOBAS` | `NIO` | Córdoba Nicaragüense |
| `COLON`, `COLONES` | `CRC` | Colón Costarricense |

---

## Validaciones y Manejo de Errores

El proceso valida cada fila de forma atómica y reporta los resultados con retroalimentación detallada:

1. **Campos Requeridos**: Si falta el nombre, apellido, identificación personal, código de empresa o salario base, se indica el número de fila exacto.
2. **Empresa Válida**: El `codigo_empresa` debe coincidir con una empresa activa en el sistema.
3. **Moneda Válida**: La moneda debe estar activa en el catálogo maestro.
4. **Actualización o Creación**:
   - Si el `codigo_empleado` o `identificacion_personal` ya existe en la empresa, el sistema **actualiza** los datos del empleado existente.
   - Si no existe, se **crea** un nuevo registro de empleado.
5. **Transaccionalidad**: Los registros válidos se confirman por lote. Si ocurre un fallo crítico de base de datos, se ejecuta reversión automática (`rollback`) y se informa el error al administrador.
