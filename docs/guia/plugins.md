# Sistema de Plugins

## Objetivo y regla inquebrantable

GoERP Payroll debe permanecer como un motor de nómina agnóstico a cualquier jurisdicción. La adaptación a una jurisdicción específica debe residir **exclusivamente** en plugins instalables, sin modificar el código fuente del motor.

## Interacción con el Motor Genérico

### Principios Fundamentales

Los plugins deben interactuar con el motor usando **únicamente** las capacidades genéricas que este expone. El motor no conoce ni debe conocer conceptos específicos de ninguna jurisdicción.

**✅ Correcto:** Plugin usa características genéricas del motor
```json
{
  "formula": "horas_extra * tarifa_hora * recargo_legal",
  "inputs": [
    {"name": "horas_extra", "source": "novedad_HORAS_EXTRA"},
    {"name": "tarifa_hora", "source": "salario_base_por_hora"},
    {"name": "recargo_legal", "source": "constante_recargo"}
  ]
}
```

**❌ Incorrecto:** Solicitar que el motor agregue lógica específica
```python
# NO HACER: Pedir al motor que agregue código específico de Nicaragua
def _normalize_nicaragua_codes(codigo):
    if codigo.startswith("bmonic_"):
        return codigo[7:]  # Lógica específica de Nicaragua
```

### Capacidades Genéricas del Motor

El motor expone las siguientes capacidades que los plugins pueden usar:

#### 1. Mapeo de Fuentes de Entrada (Formula Input Source Mapping)

Permite usar nombres descriptivos en fórmulas mientras se mapean a variables técnicas del motor.

**Documentación completa:** Ver [Mapeo de Fuentes de Entrada](reglas-calculo.md#mapeo-de-fuentes-de-entrada-en-formulas)

**Ejemplo:**
```json
{
  "formula": "mi_variable_descriptiva * 2",
  "inputs": [
    {
      "name": "mi_variable_descriptiva",
      "source": "novedad_CODIGO_GENERICO",
      "type": "number"
    }
  ]
}
```

**Uso por plugins:**
- ✅ Definir nombres descriptivos en su propio idioma/contexto
- ✅ Mapear a variables genéricas del motor
- ✅ Mantener fórmulas legibles en su jurisdicción

#### 2. Sistema de Novedades Genérico

El motor expone todas las novedades como variables `novedad_CODIGO` donde CODIGO es el código definido por el implementador.

**Ejemplo de uso en plugin:**
```json
{
  "descripcion": "Bono de productividad según legislación local",
  "formula": "bono * factor_ajuste",
  "inputs": [
    {"name": "bono", "source": "novedad_BONO_PRODUCTIVIDAD"},
    {"name": "factor_ajuste", "source": "configuracion_factor_local"}
  ]
}
```

#### 3. Campos Personalizados

El motor permite definir campos personalizados en empleados que automáticamente se exponen como variables.

**Ejemplo:**
```json
{
  "campo_personalizado": "nivel_sindical",
  "tipo": "text",
  "valores_permitidos": ["basico", "intermedio", "avanzado"]
}
```

El plugin puede usar `nivel_sindical` en sus fórmulas sin que el motor conozca el concepto de sindicatos.

#### 4. Reglas de Cálculo Configurables

El motor proporciona:
- Fórmulas con expresiones matemáticas
- Tablas de búsqueda
- Cálculos por tramos (impuestos progresivos)
- Funciones de fecha y tiempo

Todas estas capacidades son **genéricas** y configurables.

### Antipatrones: ¿Qué NO Debe Hacer un Plugin?

#### ❌ Antipatrón 1: Solicitar Código Específico en el Motor

**Incorrecto:**
```python
# NO HACER: Agregar al motor
if plugin == "nicaragua":
    codigo_normalizado = _normalize_nicaragua_code(codigo)
```

**Correcto:**
```json
// En la configuración del plugin, usar mapeo
{
  "inputs": [
    {"name": "codigo_limpio", "source": "novedad_CODIGO_CON_PREFIJO"}
  ]
}
```

#### ❌ Antipatrón 2: Asumir Convenciones del Plugin en el Motor

**Incorrecto:**
```python
# NO HACER: El motor no debe conocer prefijos de plugins
if codigo.startswith("bmonic_"):  # Específico de Nicaragua
    return codigo[7:]
```

**Correcto:**
El plugin maneja sus propias convenciones en su espacio de configuración, no en el motor.

#### ❌ Antipatrón 3: Modificar el Comportamiento del Motor

**Incorrecto:**
Pedir que el motor cambie su comportamiento base para acomodar una jurisdicción.

**Correcto:**
Usar las capacidades genéricas del motor de manera creativa para lograr el objetivo.

### Guía para Desarrolladores de Plugins

#### Paso 1: Identificar Necesidades

Antes de desarrollar, identifique:
1. ¿Qué cálculos necesita realizar?
2. ¿Qué variables del motor necesita?
3. ¿Qué nombres descriptivos usará en su jurisdicción?

#### Paso 2: Mapear a Capacidades Genéricas

Para cada necesidad, encuentre la capacidad genérica correspondiente:

| Necesidad | Capacidad Genérica del Motor |
|-----------|------------------------------|
| Horas extra con nombre local | Mapeo de fuentes: `novedad_HORAS_EXTRA` |
| Impuesto progresivo | Reglas de cálculo por tramos |
| Bono por antigüedad | Funciones de fecha + fórmulas |
| Campo específico de país | Campos personalizados |
| Descuento específico | Sistema de deducciones genérico |

#### Paso 3: Configurar sin Modificar el Motor

**Ejemplo completo para plugin Nicaragua:**

```json
{
  "percepciones": [
    {
      "codigo": "HORAS_EXTRA_NIC",
      "nombre": "Horas Extra - Nicaragua",
      "descripcion": "Cálculo según Art. 58 Código Laboral Nicaragua",
      "tipo_formula": "formula",
      "formula": {
        "expression": "horas * tarifa * recargo",
        "inputs": [
          {
            "name": "horas",
            "source": "novedad_HORAS_EXTRA",
            "type": "number",
            "descripcion": "Horas extra del período"
          },
          {
            "name": "tarifa",
            "source": "salario_base_por_hora",
            "type": "number",
            "descripcion": "Tarifa base por hora"
          },
          {
            "name": "recargo",
            "source": "constante_recargo_he",
            "type": "number",
            "descripcion": "1.5 para horas extra ordinarias según ley"
          }
        ]
      }
    }
  ]
}
```

**Note que:**
- ✅ El motor no conoce "Nicaragua" ni "Art. 58"
- ✅ Usa variables genéricas: `novedad_*`, `salario_base_por_hora`
- ✅ Los nombres descriptivos están en el mapeo del plugin
- ✅ La lógica específica está en la configuración, no en código

### Solución de Problemas Comunes

#### Problema: "Necesito que el motor reconozca mi formato específico"

**❌ Solución incorrecta:** Pedir que se modifique el motor

**✅ Solución correcta:** Usar mapeo de fuentes

```json
{
  "inputs": [
    {"name": "mi_formato", "source": "variable_generica_del_motor"}
  ]
}
```

#### Problema: "El motor no tiene la función que necesito"

**❌ Solución incorrecta:** Pedir que se agregue función específica

**✅ Solución correcta:** 
1. Revisar si se puede lograr con combinación de funciones existentes
2. Si es verdaderamente genérico y útil para múltiples jurisdicciones, proponer como mejora del motor
3. Si es específico, implementar en el espacio del plugin

#### Problema: "Mis códigos de novedad tienen prefijos que el motor no entiende"

**❌ Solución incorrecta:** Pedir normalización de códigos en el motor

**✅ Solución correcta:** Usar mapeo de fuentes para traducir

```json
{
  "inputs": [
    {"name": "horas_extra", "source": "novedad_MI_PREFIJO_HORAS_EXTRA"}
  ]
}
```

### Verificación de Cumplimiento

Antes de liberar un plugin, verifique:

- [ ] ¿Mi plugin requiere modificaciones al código del motor? → **Debe ser NO**
- [ ] ¿Mi plugin usa solo capacidades genéricas documentadas? → **Debe ser SÍ**
- [ ] ¿Otra jurisdicción podría usar el motor sin mi plugin? → **Debe ser SÍ**
- [ ] ¿El motor puede funcionar sin conocer mi jurisdicción? → **Debe ser SÍ**

### Recursos Adicionales

- [Mapeo de Fuentes de Entrada - Documentación Completa](reglas-calculo.md#mapeo-de-fuentes-de-entrada-en-formulas)
- [Reglas de Cálculo](reglas-calculo.md)
- [Sistema de Novedades](nomina.md#novedades)
- [Campos Personalizados](campos-personalizados.md)
- [Contrato Social del Proyecto](../../SOCIAL_CONTRACT.md)

## Descubrimiento (no dinámico)

- Los plugins se detectan al iniciar la aplicación enumerando los paquetes instalados en el entorno de Python.
- El implementador debe:
  - instalar el paquete del plugin
  - reiniciar la aplicación

No existe “hot reload” de plugins.

## Nombre del paquete

El paquete instalable debe llamarse:

`goerp-payroll-plugin-XXXXXXXX`

Donde `XXXXXXXX` es el identificador del plugin.

## Módulo del plugin (contrato)

Cada plugin debe exponer un módulo importable con el nombre:

`goerp_payroll_plugin_XXXXXXXX`

Regla: el `XXXXXXXX` del módulo se deriva del nombre del paquete, reemplazando `-` por `_`.

Ejemplo:

- Paquete: `goerp-payroll-plugin-pa`
- Módulo: `goerp_payroll_plugin_pa`

## Ejemplo mínimo de estructura

Ejemplo para un plugin `goerp-payroll-plugin-gt` (Guatemala):

```text
goerp-payroll-plugin-gt/
  pyproject.toml
  README.md
  goerp_payroll_plugin_gt.py
```

El sistema descubrirá el paquete al reiniciar la app y lo registrará en `plugin_registry`.

## Blueprint (requerido)

Un plugin debe **al menos registrar un blueprint**.

El módulo del plugin debe definir la función:

- `register_blueprints(app)`

Esta función es llamada por la aplicación principal solo si el plugin está marcado como `active` en la base de datos.

### Ejemplo: `register_blueprints(app)`

```python
from flask import Blueprint, render_template

bp = Blueprint("plugin_gt", __name__, url_prefix="/gt")


@bp.route("/")
def index():
    return render_template("gt/index.html")


def register_blueprints(app):
    app.register_blueprint(bp)
```

## Menú principal

Si un plugin está instalado y marcado como activo, el sistema agrega una entrada al menú principal mediante un simple bucle:

```jinja2
{% for active_plugin in plugin_actives %}
  <!-- add_entry_in_main_menu -->
{% endfor %}
```

El plugin debe proponer el nombre de la entrada y el ícono. Para eso debe exponer uno de:

- `get_menu_entry()` que devuelve un `dict`
- o `MENU_ENTRY` como `dict`

Formato del `dict`:

- `label`: texto a mostrar
- `icon`: clase CSS del icono (por defecto se usa `bi bi-puzzle`)
- `url`: URL absoluta o relativa dentro del sitio (por ejemplo `/mi-plugin/`)

### Ejemplo: entrada de menú

```python
def get_menu_entry():
    return {
        "label": "Guatemala",
        "icon": "bi bi-geo-alt",
        "url": "/gt/",
    }
```

## Estado activo/inactivo (persistido)

El estado del plugin se almacena en base de datos en la tabla `plugin_registry`.

Reglas al inicio:

- Si se detecta un plugin nuevo instalado, se inserta como registro en la BD con `active = false`.
- Si en un redeployment un plugin aparece como `active = true` en BD pero no está instalado, el sistema lo marca inmediatamente como `active = false`.

## Interfaz gráfica

La aplicación expone una pantalla para listar plugins detectados en el entorno, y activar/desactivar su estado.

Ruta:

- `/plugins/`

Nota: al activar/desactivar, se recomienda reiniciar la aplicación para asegurar que los blueprints se registren de forma consistente.

## CLI (crítico): `payrollctl plugins`

La CLI incluye el grupo:

- `payrollctl plugins`

Y por cada plugin instalado expone los siguientes subcomandos:

- `payrollctl plugins XXXXXXXX init`
- `payrollctl plugins XXXXXXXX update`
- `payrollctl plugins XXXXXXXX enable`
- `payrollctl plugins XXXXXXXX disable`
- `payrollctl plugins XXXXXXXX status`
- `payrollctl plugins XXXXXXXX version`
- `payrollctl plugins XXXXXXXX info`
- `payrollctl plugins XXXXXXXX maintainer`
    Nota: por compatibilidad, también existe el alias `mantainer` (con n mal colocada).
- `payrollctl plugins XXXXXXXX contact`
- `payrollctl plugins XXXXXXXX demo_data`

Importante: `init`, `update` y demás subcomandos no aparecen directamente bajo `payrollctl plugins`, sino bajo el subcomando del plugin.

La jerarquía real es:

- `payrollctl plugins`
- `payrollctl plugins XXXXXXXX`
    - `init`, `update`, `enable`, `disable`, `status`, `version`, `info`, `maintainer`, `contact`
    - `demo_data`

### Ejemplos de `--help`

Si no hay plugins instalados en el entorno, `payrollctl plugins --help` no mostrará subcomandos de plugins.

```text
$ payrollctl plugins --help
Usage: payrollctl plugins [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  (sin plugins instalados)
```

Cuando sí hay plugins instalados (ejemplo: `goerp-payroll-plugin-gt`):

```text
$ payrollctl plugins --help
Usage: payrollctl plugins [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
    gt
```

Y el `--help` del plugin muestra `init` y `update`:

```text
$ payrollctl plugins gt --help
Usage: payrollctl plugins gt [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
    init
    update
    enable
    disable
    status
    version
    info
    maintainer
    contact
    demo_data
```

### init (función crítica)

El comando `init` es considerado **crítico** porque puede automatizar la preparación completa de una jurisdicción.

Al ejecutar `payrollctl plugins XXXXXXXX init`, el plugin puede:

- crear definiciones de deducciones
- crear definiciones de percepciones
- crear definiciones de prestaciones
- crear definiciones de planillas
- crear tablas adicionales en la base de datos
- crear definiciones de nómina (si el implementador requiere inicialización adicional)

Lo más importante: un plugin puede empaquetar **toda** la lógica de implementación de una jurisdicción, incluyendo la carga de catálogos base (percepciones, deducciones, prestaciones) y la configuración de planillas/tipos.

El módulo del plugin debe implementar:

- `init()`

Después de ejecutar `init()`, la aplicación ejecuta `db.create_all()` para crear las tablas definidas por el plugin (si el plugin definió modelos SQLAlchemy).

### Ejemplo: `init()` cargando percepciones, deducciones, prestaciones y planillas

Ejemplo orientativo (los campos exactos dependen del modelo y tu jurisdicción). La idea es que `init()` sea **idempotente**: si lo ejecutas 2 veces, no debe duplicar registros.

```python
from goerp_payroll.model import db, Percepcion, Deduccion, Prestacion, TipoPlanilla, Planilla


def _upsert_by_codigo(Model, codigo: str, **kwargs):
    existing = db.session.execute(db.select(Model).filter_by(codigo=codigo)).scalar_one_or_none()
    if existing is None:
        existing = Model()
        existing.codigo = codigo
        db.session.add(existing)
    for k, v in kwargs.items():
        setattr(existing, k, v)
    return existing


def init():
    # 1) Catálogo de percepciones
    _upsert_by_codigo(
        Percepcion,
        "SAL_BASE",
        nombre="Salario Base",
        descripcion="Sueldo ordinario",
        formula_tipo="monto_fijo",
        activo=True,
    )

    # 2) Catálogo de deducciones
    _upsert_by_codigo(
        Deduccion,
        "IGSS",
        nombre="Seguro Social",
        descripcion="Aporte del trabajador",
        formula_tipo="porcentaje",
        activo=True,
    )

    # 3) Catálogo de prestaciones (aportes patronales)
    _upsert_by_codigo(
        Prestacion,
        "PATRONAL_SS",
        nombre="Aporte patronal SS",
        descripcion="Aporte del patrono",
        formula_tipo="porcentaje",
        activo=True,
    )

    # 4) Tipos de planilla
    _upsert_by_codigo(
        TipoPlanilla,
        "MENSUAL",
        nombre="Mensual",
        descripcion="Planilla mensual",
        activo=True,
    )

    # 5) Planillas base (ejemplo; ajustar a tu esquema: empresa/moneda, etc.)
    # Si tu modelo de Planilla requiere FK (empresa_id, moneda_id),
    # obtén/crea esos registros primero y pásalos aquí.
    _upsert_by_codigo(
        Planilla,
        "PL_MENSUAL",
        nombre="Planilla Mensual",
        descripcion="Planilla principal",
        activo=True,
    )

    db.session.commit()
```

### Ejemplo: crear tablas propias del plugin

Si tu plugin define modelos SQLAlchemy adicionales (tablas nuevas), simplemente impórtalos en el módulo del plugin (para que se registren en el metadata) y deja que el comando ejecute `db.create_all()`.

Ejemplo (conceptual):

```python
from goerp_payroll.model import db, BaseTabla


class TablaJurisdiccion(db.Model, BaseTabla):
    __tablename__ = "gt_parametros"
    clave = db.Column(db.String(50), unique=True, nullable=False, index=True)
    valor = db.Column(db.String(200), nullable=False)
```

### update

El módulo del plugin debe implementar:

- `update()`

Se utiliza para aplicar actualizaciones de catálogo o cambios propios de la jurisdicción.

Después de ejecutar `update()`, la aplicación ejecuta `db.create_all()` para asegurar que tablas nuevas queden creadas.

### Ejemplo: `update()`

Usa `update()` para:

- agregar nuevos conceptos al catálogo
- corregir descripciones/códigos
- introducir nuevas planillas/tipos

```python
from goerp_payroll.model import db, Percepcion


def update():
    p = db.session.execute(db.select(Percepcion).filter_by(codigo="SAL_BASE")).scalar_one_or_none()
    if p is not None:
        p.descripcion = "Sueldo ordinario (actualizado)"
        db.session.commit()

### enable / disable

Marcan el plugin como activo o inactivo en la tabla `plugin_registry`.

- `enable` establece `active = true`. Requiere que el plugin esté instalado.
- `disable` establece `active = false`.

Tras `enable`, se recomienda reiniciar la aplicación para registrar los blueprints del plugin.

### status

Muestra el estado del plugin, incluyendo:

- `installed`: si el paquete está presente en el entorno
- `active`: si está habilitado en la base de datos
- `version`: versión detectada

Ejemplo:

```text
$ payrollctl plugins gt status
Estado del plugin 'gt':
    Installed: True
    Active: False
    Version: 1.0.0
```

### version

Imprime la versión del plugin (detectada via distribución o metadatos del módulo).

### info / mantainer / contact

Muestran metadatos del plugin si están disponibles en el módulo:

- `PLUGIN_INFO` (dict) o `INFO` (dict) con `description`, `maintainer`, `contact`, `version`
- o atributos sueltos: `MAINTAINER`, `CONTACT`, `__version__`

Si no hay descripción explícita, se usará el docstring del módulo.

### demo_data

Permite que el plugin cargue datos de demostración pensados para pruebas automáticas y ambientes de desarrollo.

- El módulo del plugin debe exponer una función `demo_data()` (o alternativamente `load_demo_data()`).
- La CLI invoca esta función y luego ejecuta `db.create_all()` para asegurar la existencia de tablas recientes.

Ejemplo de contrato en el plugin:

```python
def demo_data():
    from goerp_payroll.model import db, Empleado

    # Crear empleados de prueba idempotentemente
    if not db.session.execute(db.select(Empleado).limit(1)).first():
        e = Empleado()
        e.codigo = "EMP-DEMO-001"
        e.nombre = "Demo"
        e.apellido = "User"
        db.session.add(e)
        db.session.commit()
```

Uso:

```bash
payrollctl plugins XXXXXXXX demo_data
```
```

## Responsabilidad del implementador

Dentro del blueprint, el diseñador del plugin puede implementar todo lo que Python / Flask / JavaScript permitan; es responsabilidad del implementador.

---

# Guía Completa: Cómo Crear un Plugin desde Cero

Esta sección proporciona una guía paso a paso para crear, empaquetar y distribuir un plugin para GoERP Payroll.

## Paso 1: Estructura del Proyecto

Crea un nuevo directorio para tu plugin. El nombre del directorio puede ser cualquiera, pero el **nombre del paquete** debe seguir la convención `goerp-payroll-plugin-XXXXXXXX`, donde `XXXXXXXX` es un identificador descriptivo (generalmente el código de país ISO de 2 letras, como `gt`, `sv`, `pa`, etc., o un nombre descriptivo para plugins funcionales).

Para este ejemplo, crearemos un plugin para El Salvador (`goerp-payroll-plugin-sv`):

```bash
mkdir goerp-payroll-plugin-sv
cd goerp-payroll-plugin-sv
```

### Estructura de archivos recomendada

```text
goerp-payroll-plugin-sv/
├── pyproject.toml           # Configuración del paquete (obligatorio)
├── README.md                # Documentación del plugin (recomendado)
├── LICENSE                  # Licencia del plugin (recomendado)
├── goerp_payroll_plugin_sv/ # Módulo del plugin (obligatorio)
│   ├── __init__.py          # Punto de entrada del plugin
│   ├── models.py            # Modelos SQLAlchemy (opcional)
│   ├── routes.py            # Rutas del blueprint (opcional)
│   └── templates/           # Plantillas HTML (opcional)
│       └── sv/
│           └── index.html
└── tests/                   # Tests del plugin (recomendado)
    └── test_plugin.py
```

## Paso 2: Crear el archivo `pyproject.toml`

Este archivo define la configuración del paquete. Es **obligatorio** para que el plugin pueda ser instalado.

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "goerp-payroll-plugin-sv"
version = "1.0.0"
description = "Plugin de GoERP Payroll para El Salvador"
readme = "README.md"
authors = [
    {name = "Tu Nombre", email = "tu@email.com"}
]
license = {text = "Apache-2.0"}  # O la licencia de tu elección: MIT, BSD, GPL, etc.
requires-python = ">=3.11"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
]

dependencies = [
    # Dependencias específicas de tu plugin
    # GoERP Payroll ya debe estar instalado
]

[project.urls]
"Homepage" = "https://github.com/tu-usuario/goerp-payroll-plugin-sv"
"Bug Tracker" = "https://github.com/tu-usuario/goerp-payroll-plugin-sv/issues"
```

## Paso 3: Crear el módulo del plugin

Crea el directorio del módulo con el nombre correcto (convierte guiones a guiones bajos):

```bash
mkdir goerp_payroll_plugin_sv
```

### 3.1: Crear `__init__.py` (punto de entrada)

Este es el archivo **más importante**. Debe exponer las funciones que el sistema espera.

```python
# goerp_payroll_plugin_sv/__init__.py
"""
Plugin de GoERP Payroll para El Salvador.

Este plugin implementa las reglas de nómina específicas para El Salvador,
incluyendo ISSS, AFP, ISR, y otros conceptos locales.
"""

from flask import Blueprint, render_template

# ============================================================================
# BLUEPRINT (OBLIGATORIO)
# ============================================================================

bp = Blueprint(
    "plugin_sv",
    __name__,
    url_prefix="/sv",
    template_folder="templates"
)


@bp.route("/")
def index():
    """Página principal del plugin."""
    return render_template("sv/index.html")


@bp.route("/reportes")
def reportes():
    """Reportes específicos de El Salvador."""
    return render_template("sv/reportes.html")


def register_blueprints(app):
    """
    Función obligatoria que registra los blueprints del plugin.

    Args:
        app: Instancia de Flask
    """
    app.register_blueprint(bp)


# ============================================================================
# ENTRADA DE MENÚ (OBLIGATORIO)
# ============================================================================

def get_menu_entry():
    """
    Devuelve la entrada del menú para este plugin.

    Returns:
        dict: Diccionario con 'label', 'icon' y 'url'
    """
    return {
        "label": "El Salvador",
        "icon": "bi bi-geo-alt-fill",
        "url": "/sv/",
    }


# Alternativa: usar una constante en lugar de una función
# MENU_ENTRY = {
#     "label": "El Salvador",
#     "icon": "bi bi-geo-alt-fill",
#     "url": "/sv/",
# }
# Nota: Si defines MENU_ENTRY, no es necesario definir get_menu_entry()


# ============================================================================
# COMANDO INIT (OBLIGATORIO)
# ============================================================================

def init():
    """
    Inicializa el plugin: carga catálogos base, crea tablas, etc.

    Esta función se ejecuta cuando el administrador ejecuta:
        payrollctl plugins sv init

    Debe ser idempotente: ejecutarla varias veces no debe duplicar datos.
    """
    from goerp_payroll.model import (
        db,
        Percepcion,
        Deduccion,
        Prestacion,
        TipoPlanilla,
    )
    from goerp_payroll.log import log

    # Función auxiliar para upsert (asume que los modelos tienen campo 'codigo')
    # Adaptar según la estructura de tu modelo si usa otro campo como clave
    def _upsert_by_codigo(Model, codigo: str, **kwargs):
        existing = db.session.execute(
            db.select(Model).filter_by(codigo=codigo)
        ).scalar_one_or_none()

        if existing is None:
            existing = Model()
            existing.codigo = codigo
            db.session.add(existing)

        for k, v in kwargs.items():
            setattr(existing, k, v)

        return existing

    # 1) Percepciones (ingresos)
    _upsert_by_codigo(
        Percepcion,
        "SALARIO",
        nombre="Salario Base",
        descripcion="Salario ordinario mensual",
        formula_tipo="monto_fijo",
        activo=True,
    )

    _upsert_by_codigo(
        Percepcion,
        "BONO_INCENTIVO",
        nombre="Bono de Incentivo",
        descripcion="Bono adicional por desempeño",
        formula_tipo="monto_fijo",
        activo=True,
    )

    # 2) Deducciones
    _upsert_by_codigo(
        Deduccion,
        "ISSS",
        nombre="ISSS",
        descripcion="Instituto Salvadoreño del Seguro Social (3%)",
        formula_tipo="porcentaje",
        prioridad=1,
        activo=True,
    )

    _upsert_by_codigo(
        Deduccion,
        "AFP",
        nombre="AFP",
        descripcion="Administradora de Fondos de Pensiones (7.25%)",
        formula_tipo="porcentaje",
        prioridad=2,
        activo=True,
    )

    _upsert_by_codigo(
        Deduccion,
        "ISR",
        nombre="ISR",
        descripcion="Impuesto Sobre la Renta",
        formula_tipo="tabla_impuestos",
        prioridad=3,
        activo=True,
    )

    # 3) Prestaciones (aportes patronales)
    _upsert_by_codigo(
        Prestacion,
        "ISSS_PATRONAL",
        nombre="ISSS Patronal",
        descripcion="Aporte patronal al ISSS (7.5%)",
        formula_tipo="porcentaje",
        activo=True,
    )

    _upsert_by_codigo(
        Prestacion,
        "AFP_PATRONAL",
        nombre="AFP Patronal",
        descripcion="Aporte patronal a AFP (8.75%)",
        formula_tipo="porcentaje",
        activo=True,
    )

    # 4) Tipos de planilla
    _upsert_by_codigo(
        TipoPlanilla,
        "MENSUAL_SV",
        nombre="Mensual (El Salvador)",
        descripcion="Planilla mensual según legislación salvadoreña",
        periodicidad_dias=30,
        activo=True,
    )

    db.session.commit()

    log.info("Plugin 'sv' inicializado correctamente")
    log.info("  - Percepciones: 2")
    log.info("  - Deducciones: 3")
    log.info("  - Prestaciones: 2")
    log.info("  - Tipos de planilla: 1")


# ============================================================================
# COMANDO UPDATE (OBLIGATORIO)
# ============================================================================

def update():
    """
    Actualiza el plugin: aplica cambios a catálogos, añade nuevos conceptos, etc.

    Esta función se ejecuta cuando el administrador ejecuta:
        payrollctl plugins sv update

    Debe ser idempotente.
    """
    from goerp_payroll.model import db, Percepcion
    from goerp_payroll.log import log

    # Ejemplo: actualizar descripción de una percepción
    p = db.session.execute(
        db.select(Percepcion).filter_by(codigo="SALARIO")
    ).scalar_one_or_none()

    if p is not None:
        p.descripcion = "Salario ordinario mensual (actualizado)"
        db.session.commit()
        log.info("Plugin 'sv' actualizado correctamente")
    else:
        log.warning("Percepción 'SALARIO' no encontrada. Ejecute 'init' primero.")
```

### 3.2: Crear plantillas HTML (opcional)

Si tu plugin tiene interfaz web, crea las plantillas:

```bash
mkdir -p goerp_payroll_plugin_sv/templates/sv
```

```html
<!-- goerp_payroll_plugin_sv/templates/sv/index.html -->
{% extends "base.html" %}

{% block title %}El Salvador - GoERP Payroll{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1><i class="bi bi-geo-alt-fill"></i> Plugin de El Salvador</h1>

    <div class="alert alert-info">
        <strong>Plugin activo:</strong> Este plugin implementa las reglas de nómina
        específicas para El Salvador.
    </div>

    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Conceptos Configurados</h5>
                </div>
                <div class="card-body">
                    <ul>
                        <li>ISSS (3%)</li>
                        <li>AFP (7.25%)</li>
                        <li>ISR (Tabla progresiva)</li>
                        <li>Aportes patronales</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Acciones</h5>
                </div>
                <div class="card-body">
                    <a href="{{ url_for('plugin_sv.reportes') }}" class="btn btn-primary">
                        <i class="bi bi-file-earmark-text"></i> Reportes
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 3.3: Crear modelos adicionales (opcional)

Si tu plugin necesita tablas adicionales:

```python
# goerp_payroll_plugin_sv/models.py
"""
Modelos adicionales específicos del plugin de El Salvador.
"""

from goerp_payroll.model import db, BaseTabla


class ParametrosSV(db.Model, BaseTabla):
    """
    Tabla para almacenar parámetros específicos de El Salvador.
    """
    __tablename__ = "sv_parametros"

    clave = db.Column(db.String(50), unique=True, nullable=False, index=True)
    valor = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)

    def __repr__(self):
        return f"<ParametroSV {self.clave}={self.valor}>"


class TablasISR(db.Model, BaseTabla):
    """
    Tabla para almacenar tramos del ISR salvadoreño.
    """
    __tablename__ = "sv_tablas_isr"

    desde_monto = db.Column(db.Numeric(15, 2), nullable=False)
    hasta_monto = db.Column(db.Numeric(15, 2), nullable=True)
    porcentaje = db.Column(db.Numeric(5, 2), nullable=False)
    cuota_fija = db.Column(db.Numeric(15, 2), default=0)

    def __repr__(self):
        return f"<TablasISR {self.desde_monto}-{self.hasta_monto}>"
```

Para que las tablas se creen, impórtalas en `__init__.py`:

```python
# Agregar al inicio de goerp_payroll_plugin_sv/__init__.py
from .models import ParametrosSV, TablasISR  # noqa: F401
```

## Paso 4: Crear README.md

Documenta tu plugin para que otros usuarios sepan qué hace:

```markdown
# Plugin de GoERP Payroll para El Salvador

Plugin que implementa las reglas de nómina específicas para El Salvador.

## Características

- ✅ ISSS (Instituto Salvadoreño del Seguro Social)
- ✅ AFP (Administradora de Fondos de Pensiones)
- ✅ ISR (Impuesto Sobre la Renta)
- ✅ Aportes patronales
- ✅ Reportes locales

## Instalación

### Desde PyPI (cuando esté publicado)

```bash
pip install goerp-payroll-plugin-sv
```

### Desde repositorio local (para desarrollo)

```bash
# Desde el directorio del plugin
pip install -e .

# O desde archivo wheel
pip install dist/goerp-payroll-plugin-sv-1.0.0-py3-none-any.whl
```

## Configuración

1. Instalar el plugin (ver arriba)
2. Reiniciar la aplicación GoERP Payroll
3. Activar el plugin desde el panel de administración (`/plugins/`)
4. Inicializar el plugin:

```bash
payrollctl plugins sv init
```

5. Reiniciar la aplicación nuevamente

## Uso

Una vez activado, el plugin aparecerá en el menú principal. Desde ahí puedes:

- Ver los conceptos configurados
- Generar reportes específicos de El Salvador

## Actualización

Para aplicar actualizaciones al catálogo:

```bash
payrollctl plugins sv update
```

## Licencia

Apache 2.0
```

## Paso 5: Empaquetar el Plugin

### 5.1: Instalar herramientas de empaquetado

```bash
pip install build twine
```

### 5.2: Construir el paquete

Desde el directorio raíz del plugin:

```bash
python -m build
```

Esto generará dos archivos en el directorio `dist/`:
- `goerp-payroll-plugin-sv-1.0.0.tar.gz` (código fuente)
- `goerp-payroll-plugin-sv-1.0.0-py3-none-any.whl` (wheel)

## Paso 6: Instalar el Plugin

### Instalación en modo desarrollo

Para probar el plugin mientras lo desarrollas:

```bash
pip install -e .
```

### Instalación desde archivo local

```bash
pip install dist/goerp-payroll-plugin-sv-1.0.0-py3-none-any.whl
```

### Instalación desde repositorio

Si publicas tu plugin en PyPI o en un repositorio privado:

```bash
pip install goerp-payroll-plugin-sv
```

## Paso 7: Activar y Usar el Plugin

1. **Reiniciar GoERP Payroll**

   Después de instalar el plugin, reinicia la aplicación.

2. **Verificar que el plugin fue detectado**

   ```bash
   payrollctl plugins --help
   ```

   Deberías ver `sv` en la lista de comandos.

3. **Activar el plugin desde la interfaz web**

   - Navega a `/plugins/`
   - Encuentra el plugin `goerp-payroll-plugin-sv`
   - Haz clic en el botón de activación
   - Reinicia la aplicación

4. **Inicializar el plugin**

   ```bash
   payrollctl plugins sv init
   ```

5. **Verificar el menú**

   El plugin ahora debe aparecer en el menú principal de la aplicación.

## Paso 8: Pruebas del Plugin

### 8.1: Crear tests

```python
# tests/test_plugin.py
import pytest


def test_plugin_has_register_blueprints():
    """Verifica que el plugin expone register_blueprints."""
    import goerp_payroll_plugin_sv as plugin

    assert hasattr(plugin, "register_blueprints")
    assert callable(plugin.register_blueprints)


def test_plugin_has_get_menu_entry():
    """Verifica que el plugin expone get_menu_entry."""
    import goerp_payroll_plugin_sv as plugin

    assert hasattr(plugin, "get_menu_entry")
    assert callable(plugin.get_menu_entry)

    entry = plugin.get_menu_entry()
    assert "label" in entry
    assert "url" in entry
    assert entry["label"] == "El Salvador"


def test_plugin_has_init():
    """Verifica que el plugin expone init."""
    import goerp_payroll_plugin_sv as plugin

    assert hasattr(plugin, "init")
    assert callable(plugin.init)


def test_plugin_has_update():
    """Verifica que el plugin expone update."""
    import goerp_payroll_plugin_sv as plugin

    assert hasattr(plugin, "update")
    assert callable(plugin.update)
```

### 8.2: Ejecutar tests

```bash
pytest tests/
```

## Mejores Prácticas

### 1. Nombres de archivos y módulos

- **Nombre del paquete**: `goerp-payroll-plugin-XXXXXXXX` (guiones)
- **Nombre del módulo**: `goerp_payroll_plugin_XXXXXXXX` (guiones bajos)
- Los nombres deben ser **consistentes**

### 2. Versionado

Usa [Versionado Semántico](https://semver.org/):
- `1.0.0`: Primera versión estable
- `1.1.0`: Nuevas características (compatible hacia atrás)
- `1.0.1`: Corrección de bugs
- `2.0.0`: Cambios incompatibles

### 3. Idempotencia

Las funciones `init()` y `update()` deben ser **idempotentes**:
- Ejecutarlas varias veces no debe causar errores
- No debe duplicar datos
- Usa `upsert` en lugar de `insert`

### 4. Manejo de errores

```python
def init():
    try:
        # ... código de inicialización ...
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log.error(f"Error al inicializar: {e}")
        raise
```

### 5. Logging

Usa el sistema de logging de GoERP Payroll:

```python
from goerp_payroll.log import log

def init():
    log.info("Inicializando plugin sv")
    # ...
    log.info("Plugin sv inicializado correctamente")
```

### 6. Dependencias

Si tu plugin requiere bibliotecas adicionales, agrégalas en `pyproject.toml`:

```toml
dependencies = [
    "requests>=2.28.0",
    "pandas>=1.5.0",
]
```

### 7. Seguridad

- **No almacenes secretos** en el código
- Usa variables de entorno para configuración sensible
- Valida todos los inputs del usuario
- Usa las funciones de autorización de GoERP Payroll:

```python
from goerp_payroll.rbac import require_write_access

@bp.route("/admin")
@require_write_access()
def admin():
    # Solo usuarios con permisos pueden acceder
    pass
```

### 8. Internacionalización

Si tu plugin tendrá múltiples idiomas, usa el sistema i18n de GoERP Payroll:

```python
from goerp_payroll.i18n import _

@bp.route("/")
def index():
    mensaje = _("Bienvenido al plugin de El Salvador")
    return render_template("sv/index.html", mensaje=mensaje)
```

### 9. Documentación

- Documenta todas las funciones públicas
- Incluye ejemplos de uso
- Explica los conceptos específicos de tu jurisdicción
- Mantén el README actualizado

### 10. Testing

- Escribe tests para las funciones principales
- Prueba la integración con GoERP Payroll
- Verifica que `init()` y `update()` funcionen correctamente
- Prueba casos extremos y errores

## Distribución del Plugin

### Opción 1: Repositorio privado

Si el plugin es para uso interno:

```bash
# Instalar desde repositorio git
pip install git+https://github.com/tu-org/goerp-payroll-plugin-sv.git
```

### Opción 2: PyPI (público)

Para compartir el plugin con la comunidad:

1. Crea una cuenta en [PyPI](https://pypi.org/)

2. Configura tu autenticación:

   ```bash
   # Crear archivo ~/.pypirc
   # ⚠️ ADVERTENCIA: Protege este archivo (chmod 600 ~/.pypirc)
   # ⚠️ Nunca compartas tu token en repositorios públicos
   [pypi]
   username = __token__
   password = pypi-tu-token-aqui  # Token API de PyPI
   ```

   **Alternativa más segura**: Usar variables de entorno o keyring:

   ```bash
   # Usar variables de entorno
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-tu-token-aqui

   # O usar keyring (recomendado)
   pip install keyring
   keyring set https://upload.pypi.org/legacy/ __token__
   ```

3. Publica el plugin:

   ```bash
   python -m build
   twine upload dist/*
   ```

4. Instala desde PyPI:

   ```bash
   pip install goerp-payroll-plugin-sv
   ```

### Opción 3: Servidor privado de paquetes

Para organizaciones que necesitan un repositorio privado, considera usar:
- [devpi](https://devpi.net/)
- [PyPI Server](https://pypi.org/project/pypiserver/)
- [JFrog Artifactory](https://jfrog.com/artifactory/)
- [Nexus Repository](https://www.sonatype.com/products/nexus-repository)

## Solución de Problemas

### El plugin no aparece en `payrollctl plugins`

1. Verifica que el paquete esté instalado:
   ```bash
   pip list | grep goerp-payroll-plugin
   ```

2. Verifica el nombre del paquete:
   ```bash
   pip show goerp-payroll-plugin-sv
   ```

3. Reinicia la aplicación

### Error al ejecutar `init`

1. Verifica que GoERP Payroll esté instalado:
   ```bash
   pip show goerp-payroll
   ```

2. Verifica que la base de datos esté configurada

3. Revisa los logs de la aplicación

### El plugin no aparece en el menú

1. Verifica que el plugin esté **activo** en `/plugins/`
2. Reinicia la aplicación después de activarlo
3. Verifica que `get_menu_entry()` devuelva un diccionario válido

### Errores de importación

Verifica que el nombre del módulo sea correcto:
- Paquete: `goerp-payroll-plugin-sv` (guiones)
- Módulo: `goerp_payroll_plugin_sv` (guiones bajos)

## Resumen de Checklist

Al crear un plugin, asegúrate de tener:

- [ ] Nombre de paquete correcto: `goerp-payroll-plugin-XXXXXXXX`
- [ ] Nombre de módulo correcto: `goerp_payroll_plugin_XXXXXXXX`
- [ ] Archivo `pyproject.toml` configurado
- [ ] Función `register_blueprints(app)` implementada
- [ ] Función `get_menu_entry()` implementada (devuelve dict con label, icon, url)
- [ ] Función `init()` implementada e idempotente
- [ ] Función `update()` implementada e idempotente
- [ ] Blueprint con al menos una ruta
- [ ] README.md con documentación
- [ ] Tests básicos
- [ ] Manejo de errores apropiado

## Ejemplos de Plugins

Para inspirarte, algunos ejemplos de plugins podrían incluir:

- **Plugin de jurisdicción**: Guatemala, Panamá, Costa Rica, etc.
- **Plugin de integración**: Conectar con sistemas contables externos
- **Plugin de reportes**: Reportes específicos de una industria
- **Plugin de validaciones**: Reglas de negocio adicionales
- **Plugin de notificaciones**: Envío de correos, SMS, etc.

---

**¡Felicidades!** Ahora tienes todos los conocimientos para crear tu propio plugin de GoERP Payroll.
