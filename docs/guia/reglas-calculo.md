# Reglas de Cálculo

Las reglas de cálculo son un componente avanzado que permite configurar cálculos complejos utilizando esquemas estructurados. Son especialmente útiles para implementar cálculos de impuestos progresivos, seguridad social y otros cálculos basados en tablas o tramos.

## ¿Qué son las Reglas de Cálculo?

Las reglas de cálculo son configuraciones que definen cómo realizar cálculos complejos basados en:

- **Tablas de tramos**: Para impuestos progresivos o cálculos escalonados
- **Límites y umbrales**: Para aplicar diferentes fórmulas según rangos
- **Tasas variables**: Para cálculos que cambian según el monto base

## Casos de Uso Comunes

### Impuesto sobre la Renta (IR)

El IR en Nicaragua es un impuesto progresivo con diferentes tramos:

```
Tramo 1: C$ 0 - 100,000 → Exento
Tramo 2: C$ 100,000 - 200,000 → 15%
Tramo 3: C$ 200,000 - 350,000 → 20%
Tramo 4: C$ 350,000+ → 25%
```

### INSS (Seguro Social)

Cálculo de aportes a la seguridad social con topes:

- Tasa laboral: 7%
- Tasa patronal: 22.5%
- Tope máximo: C$ 100,000

### Otros Usos

- Bonos escalonados por antigüedad
- Comisiones progresivas por ventas
- Descuentos por volumen
- Cualquier cálculo basado en tablas o tramos

## Componentes de una Regla de Cálculo

### Información Básica

- **Código**: Identificador único (ej: `IR_NICARAGUA`)
- **Nombre**: Nombre descriptivo (ej: "Impuesto sobre la Renta Nicaragua")
- **Versión**: Versión de la regla (permite mantener historial)
- **Descripción**: Explicación del propósito de la regla
- **Activa**: Indica si la regla está en uso

### Esquema JSON

El esquema define la estructura del cálculo. Ejemplo para IR:

```json
{
  "tipo": "tramos",
  "tramos": [
    {
      "desde": 0,
      "hasta": 100000,
      "tasa": 0,
      "base_fija": 0
    },
    {
      "desde": 100000,
      "hasta": 200000,
      "tasa": 0.15,
      "base_fija": 0
    },
    {
      "desde": 200000,
      "hasta": 350000,
      "tasa": 0.20,
      "base_fija": 15000
    },
    {
      "desde": 350000,
      "hasta": null,
      "tasa": 0.25,
      "base_fija": 45000
    }
  ]
}
```

## Crear una Regla de Cálculo

### Método 1: Formulario Manual

1. Acceda a **Configuración** → **Reglas de Cálculo**
2. Haga clic en **Nueva Regla de Cálculo**
3. Complete los campos:
   - **Código**: Use un código descriptivo único
   - **Nombre**: Nombre que verán los usuarios
   - **Descripción**: Explique el propósito y uso
   - **Esquema JSON**: Pegue o escriba el esquema
   - **Versión**: Inicie en 1
   - **Activa**: Marque para activar la regla
4. Haga clic en **Guardar**

### Método 2: Editor de Esquemas (Recomendado)

1. Acceda a **Configuración** → **Reglas de Cálculo**
2. Haga clic en **Nueva Regla de Cálculo**
3. Use el **Editor de Esquemas** visual:
   - Seleccione el tipo de esquema (tramos, tabla, fórmula)
   - Configure los parámetros usando el formulario visual
   - El sistema genera automáticamente el JSON
4. Guarde la regla

!!! tip "Ventajas del Editor Visual"
    El editor de esquemas valida automáticamente la estructura, previene errores de sintaxis y proporciona una interfaz más intuitiva.

## Funciones de Fecha

El motor de fórmulas soporta funciones para trabajar con fechas, permitiendo cálculos basados en antigüedad, períodos de tiempo y comparaciones de fechas.

### Funciones Disponibles

#### `days_between(fecha_inicio, fecha_fin)`

Calcula el número de días entre dos fechas.

**Sintaxis:**
```
days_between(fecha_inicio, fecha_fin)
```

**Parámetros:**
- `fecha_inicio`: Fecha inicial (formato ISO: YYYY-MM-DD o campo de fecha)
- `fecha_fin`: Fecha final (formato ISO: YYYY-MM-DD o campo de fecha)

**Retorna:** Número de días (entero positivo si fecha_fin > fecha_inicio)

**Ejemplo:**
```json
{
  "tipo": "formula",
  "formula": "days_between(fecha_ingreso, hoy) / 365",
  "descripcion": "Años de antigüedad del empleado"
}
```

#### `max_date(fecha1, fecha2, ...)`

Retorna la fecha más reciente de las fechas proporcionadas.

**Sintaxis:**
```
max_date(fecha1, fecha2, fecha3, ...)
```

**Parámetros:**
- `fecha1, fecha2, ...`: Dos o más fechas a comparar

**Retorna:** La fecha más reciente

**Ejemplo:**
```json
{
  "tipo": "formula",
  "formula": "days_between(max_date(ultima_promocion, fecha_ingreso), hoy)",
  "descripcion": "Días desde último cambio relevante"
}
```

#### `min_date(fecha1, fecha2, ...)`

Retorna la fecha más antigua de las fechas proporcionadas.

**Sintaxis:**
```
min_date(fecha1, fecha2, fecha3, ...)
```

**Parámetros:**
- `fecha1, fecha2, ...`: Dos o más fechas a comparar

**Retorna:** La fecha más antigua

**Ejemplo:**
```json
{
  "tipo": "formula",
  "formula": "days_between(min_date(fecha_contrato, fecha_ingreso), hoy)",
  "descripcion": "Antigüedad basada en primera relación laboral"
}
```

### Casos de Uso con Fechas

#### Bono por Antigüedad Basado en Años

```json
{
  "tipo": "formula",
  "descripcion": "Bono escalonado según años completos de servicio",
  "formula": "if(years >= 10, 3000, if(years >= 5, 2000, if(years >= 3, 1000, if(years >= 1, 500, 0))))",
  "variables": {
    "years": "days_between(fecha_ingreso, hoy) / 365"
  }
}
```

#### Ajuste Proporcional por Días Trabajados

```json
{
  "tipo": "formula",
  "descripcion": "Salario proporcional según días trabajados en el mes",
  "formula": "(salario_base / dias_mes) * dias_trabajados",
  "variables": {
    "dias_trabajados": "days_between(fecha_ingreso, fin_mes)"
  }
}
```

#### Comparación de Fechas para Elegibilidad

```json
{
  "tipo": "formula",
  "descripcion": "Bono solo para empleados con más de 6 meses",
  "formula": "if(days_between(fecha_ingreso, hoy) >= 180, monto_bono, 0)"
}
```

### Tipos de Entrada en Fórmulas

Además de valores numéricos (Decimal), el motor de fórmulas acepta:

#### Fechas
- Formato ISO: `"2024-01-15"`
- Campos de empleado: `fecha_ingreso`, `fecha_nacimiento`
- Fecha actual del sistema: `hoy` (variable especial)

#### Cadenas de Texto (Strings)
- Para comparaciones: `"ACTIVO"`, `"INACTIVO"`
- Para campos de texto: `tipo_contrato`, `departamento`

**Ejemplo con múltiples tipos:**
```json
{
  "tipo": "formula",
  "descripcion": "Bono especial para gerentes con más de 2 años",
  "formula": "if(cargo == 'GERENTE' and days_between(fecha_ingreso, hoy) > 730, 5000, 0)"
}
```

!!! warning "Formato de Fechas"
    Las fechas deben estar en formato ISO (YYYY-MM-DD). Otros formatos pueden causar errores de cálculo.

!!! tip "Variables de Fecha del Sistema"
    El sistema proporciona variables especiales como `hoy` (fecha actual) y `fin_mes` (último día del mes de cálculo) que se actualizan automáticamente.

## Tipos de Esquemas

### Esquema de Tramos

Para cálculos progresivos como impuestos:

```json
{
  "tipo": "tramos",
  "tramos": [
    {
      "desde": valor_minimo,
      "hasta": valor_maximo,
      "tasa": porcentaje_decimal,
      "base_fija": monto_fijo_base
    }
  ]
}
```

**Parámetros:**

- `desde`: Límite inferior del tramo (inclusive)
- `hasta`: Límite superior del tramo (exclusive, `null` para ilimitado)
- `tasa`: Tasa a aplicar en el tramo (como decimal: 0.15 = 15%)
- `base_fija`: Monto fijo a sumar al cálculo del tramo

### Esquema de Tabla

Para búsqueda directa de valores:

```json
{
  "tipo": "tabla",
  "filas": [
    {
      "clave": "valor_busqueda",
      "resultado": valor_retornar
    }
  ]
}
```

### Esquema de Fórmula

Para cálculos con fórmula directa:

```json
{
  "tipo": "formula",
  "formula": "monto * 0.07",
  "tope_maximo": 7000,
  "tope_minimo": 0
}
```

## Mapeo de Fuentes de Entrada en Fórmulas (Formula Input Source Mapping)

### ¿Qué es el Mapeo de Fuentes?

El mapeo de fuentes de entrada (input source mapping) es una característica del motor de fórmulas que permite a las configuraciones y plugins definir **alias claros y descriptivos** para variables del motor, sin necesidad de modificar el código del motor.

Esta característica es **fundamental para mantener el motor agnóstico a la jurisdicción**, ya que permite que plugins de diferentes países usen sus propias convenciones de nombres mientras interactúan con las variables genéricas del motor.

### ¿Por Qué es Importante?

**Problema sin mapeo de fuentes:**
- El motor expone variables con nombres técnicos como `novedad_HORAS_EXTRA`
- Las fórmulas deben usar estos nombres exactos, haciendo las configuraciones difíciles de leer
- Los plugins no pueden usar nombres descriptivos en su propio contexto

**Solución con mapeo de fuentes:**
- Las fórmulas pueden usar nombres descriptivos y legibles
- Los plugins pueden definir sus propias convenciones de nombres
- El motor traduce automáticamente entre nombres descriptivos y nombres técnicos
- **El motor permanece completamente agnóstico** - no conoce ni entiende los nombres específicos de cada jurisdicción

### Cómo Funciona

El mapeo se define en el campo `inputs` de una fórmula, donde cada entrada especifica:

- `name`: El nombre descriptivo que se usará en la fórmula
- `source`: La variable técnica del motor que proporciona el valor
- `type`: El tipo de dato (opcional, para documentación)

**Ejemplo básico:**

```json
{
  "tipo": "formula",
  "formula": "horas_extra * tarifa_hora * 1.5",
  "inputs": [
    {
      "name": "horas_extra",
      "source": "novedad_HORAS_EXTRA",
      "type": "number"
    },
    {
      "name": "tarifa_hora",
      "source": "salario_base_por_hora",
      "type": "number"
    }
  ]
}
```

En este ejemplo:
- La fórmula usa `horas_extra` (nombre descriptivo)
- El motor busca el valor en `novedad_HORAS_EXTRA` (variable técnica)
- La fórmula es más legible y mantenible

### Notación con Puntos (Dotted Notation)

El mapeo soporta notación con puntos para mayor flexibilidad:

```json
{
  "tipo": "formula",
  "formula": "horas_extra * 2",
  "inputs": [
    {
      "name": "horas_extra",
      "source": "novedad.HORAS_EXTRA",
      "type": "number"
    }
  ]
}
```

**Comportamiento:**
1. El motor intenta buscar la variable completa `novedad.HORAS_EXTRA`
2. Si no existe, extrae la última parte después del punto: `HORAS_EXTRA`
3. Busca esta variable en el contexto de cálculo

Esto permite:
- Documentar la procedencia de las variables (namespace conceptual)
- Mantener compatibilidad con diferentes convenciones de nombres
- Facilitar la migración entre versiones de configuración

### Variables Disponibles en el Motor

El motor expone las siguientes variables genéricas que pueden ser mapeadas:

#### Variables de Salario
- `salario_base`: Salario base del empleado
- `salario_mensual`: Salario mensualizado
- `salario_bruto`: Salario bruto del período
- `salario_neto`: Salario neto después de deducciones

#### Variables de Período
- `dias_trabajados`: Días trabajados en el período
- `dias_mes`: Días totales del mes
- `hoy`: Fecha actual del sistema

#### Variables de Empleado
- `fecha_ingreso`: Fecha de ingreso del empleado
- `fecha_nacimiento`: Fecha de nacimiento
- Variables de campos personalizados definidos por el implementador

#### Variables de Novedades
- `novedad_CODIGO`: Valor de una novedad específica (donde CODIGO es el código de la novedad)
- Ejemplo: `novedad_BONO_PRODUCTIVIDAD`, `novedad_DESCUENTO_PRESTAMO`

#### Variables Acumuladas
- `salario_acumulado`: Salario acumulado en el año fiscal
- `impuesto_acumulado`: Impuesto retenido acumulado
- `periodos_procesados`: Número de períodos procesados

#### Variables de Cálculo
- `total_percepciones`: Total de percepciones calculadas
- `total_deducciones`: Total de deducciones calculadas

### Ejemplo Completo: Plugin Nicaragua

Un plugin de Nicaragua puede usar el mapeo para mantener sus propias convenciones mientras usa las capacidades genéricas del motor:

**Configuración del plugin (JSON):**
```json
{
  "codigo": "CALC_HORAS_EXTRA_NIC",
  "nombre": "Cálculo de Horas Extra - Nicaragua",
  "tipo": "formula",
  "formula": "horas_extra * (salario_hora * recargo_ley)",
  "inputs": [
    {
      "name": "horas_extra",
      "source": "novedad_HORAS_EXTRA",
      "type": "number",
      "descripcion": "Horas extra reportadas por el sistema de asistencia"
    },
    {
      "name": "salario_hora",
      "source": "salario_base_por_hora",
      "type": "number",
      "descripcion": "Salario base dividido por horas mensuales"
    },
    {
      "name": "recargo_ley",
      "source": "constante_recargo_he",
      "type": "number",
      "descripcion": "Recargo del 50% según Código Laboral Nicaragua"
    }
  ]
}
```

**Lo que hace el motor:**
1. Lee la fórmula: `horas_extra * (salario_hora * recargo_ley)`
2. Busca el mapeo de `horas_extra` → encuentra `novedad_HORAS_EXTRA`
3. Busca el mapeo de `salario_hora` → encuentra `salario_base_por_hora`
4. Busca el mapeo de `recargo_ley` → encuentra `constante_recargo_he`
5. Evalúa la fórmula usando estos valores

**Ventajas:**
- ✅ El motor no conoce conceptos específicos de Nicaragua
- ✅ La fórmula es legible en español y contexto nicaragüense
- ✅ El plugin puede cambiar sus convenciones sin modificar el motor
- ✅ Otros países pueden usar sus propias convenciones

### Ejemplo: Plugin con Múltiples Países

Diferentes plugins pueden usar el mismo motor con sus propias convenciones:

**Plugin Guatemala:**
```json
{
  "formula": "tiempo_extra * pago_hora * factor_legal",
  "inputs": [
    {
      "name": "tiempo_extra",
      "source": "novedad_HORAS_EXTRA"
    },
    {
      "name": "pago_hora",
      "source": "salario_base_por_hora"
    },
    {
      "name": "factor_legal",
      "source": "constante_recargo_he"
    }
  ]
}
```

**Plugin Panamá:**
```json
{
  "formula": "horas_adicionales * tarifa_ordinaria * multiplicador_ley",
  "inputs": [
    {
      "name": "horas_adicionales",
      "source": "novedad_HORAS_EXTRA"
    },
    {
      "name": "tarifa_ordinaria",
      "source": "salario_base_por_hora"
    },
    {
      "name": "multiplicador_ley",
      "source": "constante_recargo_he"
    }
  ]
}
```

Ambos plugins usan las **mismas variables del motor** (`novedad_HORAS_EXTRA`, `salario_base_por_hora`), pero cada uno usa su propia terminología en las fórmulas.

### Mejores Prácticas para Plugins

#### 1. Use Nombres Descriptivos en su Contexto

```json
// ❌ No recomendado: usar nombres técnicos del motor
{
  "formula": "novedad_HORAS_EXTRA * salario_base_por_hora"
}

// ✅ Recomendado: usar nombres descriptivos para su jurisdicción
{
  "formula": "horas_extra * tarifa_hora",
  "inputs": [
    {"name": "horas_extra", "source": "novedad_HORAS_EXTRA"},
    {"name": "tarifa_hora", "source": "salario_base_por_hora"}
  ]
}
```

#### 2. Documente sus Mapeos

```json
{
  "inputs": [
    {
      "name": "horas_extra",
      "source": "novedad_HORAS_EXTRA",
      "type": "number",
      "descripcion": "Horas extra reportadas conforme Art. 123 del Código Laboral",
      "ejemplo": "10.5"
    }
  ]
}
```

#### 3. Use Notación con Puntos para Claridad

```json
{
  "inputs": [
    {
      "name": "bono_productividad",
      "source": "novedad.BONO_PRODUCTIVIDAD"
    },
    {
      "name": "dias_mes",
      "source": "periodo.dias_mes"
    }
  ]
}
```

La notación con puntos ayuda a documentar de dónde viene cada valor, aunque el motor solo usa la parte final.

#### 4. Mantenga Consistencia en su Plugin

Use los mismos nombres de variables a lo largo de todas las fórmulas de su plugin para facilitar el mantenimiento.

### Preguntas Frecuentes

**P: ¿Puedo mapear una misma fuente a múltiples nombres?**  
R: Sí, puede crear múltiples mapeos para la misma variable:

```json
{
  "inputs": [
    {"name": "salario", "source": "salario_base"},
    {"name": "sueldo", "source": "salario_base"}
  ]
}
```

**P: ¿Qué pasa si el source no existe?**  
R: El motor simplemente no crea el mapeo. La variable `name` no estará disponible en la fórmula, lo que podría causar un error de evaluación si se usa.

**P: ¿Puedo usar mapeo con tablas y tramos?**  
R: Sí, el mapeo funciona con todos los tipos de esquemas (formula, tramos, tabla).

**P: ¿El mapeo afecta el rendimiento?**  
R: No significativamente. El mapeo se realiza una vez por empleado durante el cálculo de nómina.

### Contratos y Garantías del Motor

**El motor garantiza:**
- ✅ Las variables genéricas (como `salario_base`, `novedad_*`) siempre estarán disponibles
- ✅ El mapeo es consistente y predecible
- ✅ Los nombres de variables del motor no cambiarán sin aviso previo
- ✅ El motor NO interpretará ni validará los nombres que usted elija para sus mapeos

**El motor NO garantiza:**
- ❌ Que sus nombres personalizados sean únicos entre diferentes plugins
- ❌ Que sus convenciones de nombres sean compatibles con otros plugins
- ❌ Validación semántica de sus nombres (solo sintaxis JSON)

### Integración con Plugins: Responsabilidades

**Responsabilidad del Motor:**
- Exponer variables genéricas y bien documentadas
- Procesar el mapeo de fuentes correctamente
- Mantener el contrato de variables estable

**Responsabilidad del Plugin:**
- Definir sus propios mapeos de fuentes
- Documentar sus convenciones de nombres
- Mantener compatibilidad con las variables del motor
- No depender de comportamientos no documentados

**Responsabilidad del Implementador:**
- Entender las variables disponibles en el motor
- Configurar los mapeos según las necesidades de su jurisdicción
- Probar las fórmulas con datos reales antes de producción

## Versionado de Reglas

Las reglas de cálculo soportan versionado para mantener historial:

### ¿Por qué Versionar?

- Los impuestos y contribuciones cambian con el tiempo
- Necesita mantener cálculos históricos correctos
- Permite auditar cambios en las reglas

### Crear una Nueva Versión

1. En la lista de reglas, encuentre la regla a versionar
2. Haga clic en **Copiar** o **Nueva Versión**
3. Incremente el número de versión
4. Realice los cambios necesarios en el esquema
5. Active la nueva versión
6. Desactive la versión anterior (opcional)

!!! note "Versiones Activas"
    Solo una versión de cada regla (mismo código) debe estar activa a la vez. El sistema usa la versión activa más reciente para nuevos cálculos.

## Usar Reglas en Deducciones

Para usar una regla de cálculo en una deducción:

1. Cree o edite una deducción
2. En **Fórmula**, seleccione el tipo **Regla de Cálculo**
3. Seleccione la regla de cálculo de la lista
4. Configure el origen del monto base (ej: salario bruto)
5. Guarde la deducción

El sistema aplicará automáticamente la regla al calcular la nómina.

## Validación de Esquemas

El sistema valida automáticamente los esquemas JSON:

### Errores Comunes

❌ **Sintaxis JSON inválida**
```json
{
  "tipo": "tramos"
  "tramos": []  // Falta coma
}
```

✅ **Sintaxis correcta**
```json
{
  "tipo": "tramos",
  "tramos": []
}
```

❌ **Tramos superpuestos**
```json
{
  "tramos": [
    {"desde": 0, "hasta": 100000},
    {"desde": 50000, "hasta": 150000}  // Se superpone con anterior
  ]
}
```

✅ **Tramos continuos**
```json
{
  "tramos": [
    {"desde": 0, "hasta": 100000},
    {"desde": 100000, "hasta": 150000}
  ]
}
```

## Ejemplos Completos

### Ejemplo 1: IR Nicaragua 2024

```json
{
  "tipo": "tramos",
  "descripcion": "Impuesto sobre la Renta Nicaragua 2024",
  "tramos": [
    {
      "desde": 0,
      "hasta": 100000,
      "tasa": 0,
      "base_fija": 0,
      "descripcion": "Exento"
    },
    {
      "desde": 100000,
      "hasta": 200000,
      "tasa": 0.15,
      "base_fija": 0,
      "descripcion": "15% sobre exceso de C$ 100,000"
    },
    {
      "desde": 200000,
      "hasta": 350000,
      "tasa": 0.20,
      "base_fija": 15000,
      "descripcion": "C$ 15,000 + 20% sobre exceso de C$ 200,000"
    },
    {
      "desde": 350000,
      "hasta": null,
      "tasa": 0.25,
      "base_fija": 45000,
      "descripcion": "C$ 45,000 + 25% sobre exceso de C$ 350,000"
    }
  ]
}
```

### Ejemplo 2: INSS con Tope

```json
{
  "tipo": "formula",
  "descripcion": "INSS Laboral 7% con tope de C$ 100,000",
  "formula": "min(monto, 100000) * 0.07",
  "tope_maximo": 7000,
  "tope_minimo": 0
}
```

### Ejemplo 3: Bono por Antigüedad

```json
{
  "tipo": "tabla",
  "descripcion": "Bono mensual según años de antigüedad",
  "filas": [
    {"años": "0-1", "monto": 0},
    {"años": "1-3", "monto": 500},
    {"años": "3-5", "monto": 1000},
    {"años": "5-10", "monto": 2000},
    {"años": "10+", "monto": 3000}
  ]
}
```

## Mejores Prácticas

### Documentación

- Use descripciones claras y detalladas
- Incluya la fecha de vigencia en la descripción
- Documente la fuente legal o regulatoria

### Códigos

- Use códigos descriptivos: `IR_NIC_2024`, `INSS_LABORAL`
- Incluya el año en códigos de reglas que cambian frecuentemente
- Sea consistente con la nomenclatura

### Testing

- Pruebe la regla con varios montos antes de activarla
- Verifique casos límite (0, valores en fronteras de tramos)
- Compare resultados con cálculos manuales conocidos

### Mantenimiento

- Revise las reglas anualmente o cuando cambien las leyes
- Mantenga versiones históricas inactivas para auditoría
- Documente cambios entre versiones

## Solución de Problemas

### La regla no se aplica

- Verifique que la regla esté marcada como **Activa**
- Confirme que la deducción/percepción usa la regla correcta
- Revise que el monto base sea el correcto

### Resultados incorrectos

- Valide el esquema JSON con el editor visual
- Verifique que los tramos no se superpongan
- Confirme que las tasas estén en formato decimal (0.15, no 15)
- Pruebe con montos conocidos

### Error de validación

- Revise la sintaxis JSON (comas, llaves, corchetes)
- Verifique que todos los campos requeridos estén presentes
- Use el editor visual para generar esquemas válidos

## Seguridad

- Solo usuarios administrativos pueden crear o modificar reglas
- Los cambios en reglas activas pueden afectar cálculos de nómina
- Pruebe cambios en un entorno de desarrollo primero

## Soporte

Para asistencia adicional con reglas de cálculo:

- Revise las [preguntas frecuentes](../referencia/faq.md)
- Consulte el [glosario](../referencia/glosario.md) para términos específicos
- Contacte al equipo de soporte con ejemplos específicos

---

!!! info "Característica Avanzada"
    Las reglas de cálculo son una característica avanzada. Para la mayoría de los casos simples, las fórmulas directas en percepciones y deducciones son suficientes.
