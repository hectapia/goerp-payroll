# Requisitos del Sistema

Antes de instalar GoERP Payroll, asegúrese de que su sistema cumple con los siguientes requisitos.

## Requisitos de Software

### Python

GoERP Payroll requiere **Python 3.11 o superior**.

```bash
# Verificar versión de Python
python --version
# o
python3 --version
```

### Base de Datos

El sistema soporta las siguientes bases de datos:

| Base de Datos | Versión Mínima | Recomendado Para |
|---------------|----------------|------------------|
| SQLite        | 3.x            | Desarrollo y pruebas |
| PostgreSQL    | 13+            | Producción |
| MySQL/MariaDB | 8.0+ / 10.5+   | Producción |

!!! tip "Recomendación"
    Para entornos de producción, se recomienda usar PostgreSQL por su robustez y soporte para transacciones complejas.

### Dependencias del Sistema

Para algunas funcionalidades (como generación de PDFs), se requieren bibliotecas adicionales del sistema:

=== "Ubuntu/Debian"

    ```bash
    sudo apt-get update
    sudo apt-get install -y \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        shared-mime-info
    ```

=== "CentOS/RHEL"

    ```bash
    sudo yum install -y \
        pango \
        gdk-pixbuf2 \
        libffi-devel
    ```

=== "macOS"

    ```bash
    brew install pango gdk-pixbuf libffi
    ```

## Requisitos de Hardware

### Mínimos

| Componente | Especificación |
|------------|----------------|
| CPU        | 1 núcleo       |
| RAM        | 1 GB           |
| Almacenamiento | 10 GB      |

### Recomendados (Producción)

| Componente | Especificación |
|------------|----------------|
| CPU        | 2+ núcleos     |
| RAM        | 4 GB           |
| Almacenamiento | 50 GB (SSD) |

## Puertos de Red

El sistema utiliza los siguientes puertos por defecto:

| Servicio | Puerto | Configurable |
|----------|--------|--------------|
| Aplicación Web | 5000 | Sí (variable `PORT`) |
| PostgreSQL | 5432 | Sí |
| MySQL | 3306 | Sí |
| Redis (sesiones) | 6379 | Sí (opcional) |

## Variables de Entorno

Las siguientes variables de entorno son utilizadas por el sistema:

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `FLASK_ENV` | Entorno de ejecución (`development`/`production`) | Sí (producción) |
| `DATABASE_URL` | URI de conexión a la base de datos | Sí (producción) |
| `SECRET_KEY` | Clave secreta para sesiones | Sí (producción) |
| `ADMIN_USER` | Usuario administrador inicial | Sí (producción) |
| `ADMIN_PASSWORD` | Contraseña del administrador | Sí (producción) |
| `SESSION_REDIS_URL` | URL de Redis para sesiones | No |
| `REDIS_URL` | URL de Redis para cola | No |
| `QUEUE_ENABLED` | Habilita/deshabilita colas | No (default: `1`) |
| `COATI_QUEUE_PATH` | Ruta para cola en filesystem (Huey) | No |
| `BACKGROUND_PAYROLL_THRESHOLD` | Umbral de empleados para cola | No (default: `100`) |
| `MAX_CONTENT_LENGTH` | Límite de subida en bytes | No (default: `2097152`) |
| `PORT` | Puerto de la aplicación | No (default: 5000) |

!!! warning "Seguridad"
    En producción, **siempre** cambie las credenciales por defecto y establezca una `SECRET_KEY` segura.

## Navegadores Soportados

La interfaz web de GoERP Payroll es compatible con:

- Google Chrome 90+
- Mozilla Firefox 88+
- Microsoft Edge 90+
- Safari 14+

!!! note "JavaScript"
    El navegador debe tener JavaScript habilitado para el funcionamiento correcto de la aplicación.
