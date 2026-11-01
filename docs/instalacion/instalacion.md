# Instalación

Esta guía le ayudará a instalar GoERP Payroll en su sistema.

## Instalación Rápida (Desarrollo)

Para un entorno de desarrollo local, siga estos pasos:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/williamjmorenor/coati.git
cd coati
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
# Instalar dependencias de producción
pip install -r requirements.txt

# Instalar dependencias de desarrollo (opcional)
pip install -r development.txt
```

### 4. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`.

!!! success "Credenciales por Defecto"
    - **Usuario**: `coati-admin`
    - **Contraseña**: `coati-admin`

## Instalación para Producción

Para un entorno de producción, se recomienda usar una base de datos robusta y un servidor WSGI adecuado.

### 1. Preparar el Servidor

```bash
# Crear usuario dedicado
sudo useradd -m -s /bin/bash coati
sudo su - coati

# Clonar repositorio
git clone https://github.com/williamjmorenor/coati.git
cd coati
```

### 2. Configurar Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

=== "PostgreSQL"

    ```bash
    # Instalar PostgreSQL
    sudo apt-get install postgresql postgresql-contrib

    # Crear base de datos
    sudo -u postgres createuser coati_user
    sudo -u postgres createdb coati_db -O coati_user
    sudo -u postgres psql -c "ALTER USER coati_user WITH PASSWORD 'tu_contraseña_segura';"
    ```

    ```bash
    # Configurar variable de entorno
    export DATABASE_URL="postgresql://coati_user:tu_contraseña_segura@localhost:5432/coati_db"
    ```

=== "MySQL"

    ```bash
    # Instalar MySQL
    sudo apt-get install mysql-server

    # Crear base de datos
    sudo mysql -e "CREATE DATABASE coati_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    sudo mysql -e "CREATE USER 'coati_user'@'localhost' IDENTIFIED BY 'tu_contraseña_segura';"
    sudo mysql -e "GRANT ALL PRIVILEGES ON coati_db.* TO 'coati_user'@'localhost';"
    sudo mysql -e "FLUSH PRIVILEGES;"
    ```

    ```bash
    # Configurar variable de entorno
    export DATABASE_URL="mysql+mysqlconnector://coati_user:tu_contraseña_segura@localhost/coati_db"
    ```

### 4. Configurar Variables de Entorno

Cree un archivo `.env` o configure las variables directamente:

```bash
export DATABASE_URL="postgresql://coati_user:contraseña@localhost:5432/coati_db"
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export ADMIN_USER="admin"
export ADMIN_PASSWORD="tu_contraseña_segura"
export MAX_CONTENT_LENGTH=2097152  # ~2 MB (~1000 filas Excel típicas)
export PORT=5000
```

!!! warning "Seguridad"
    Nunca commit el archivo `.env` al repositorio. Asegúrese de que `.env` está en `.gitignore`.

### 5. Configurar Servicio Systemd

El repositorio incluye archivos de servicio systemd de ejemplo en el directorio `systemd/`:

- `goerp-payroll.service`: Servicio principal de la aplicación web
- `goerp-payroll-worker.service`: Worker Dramatiq para procesamiento en segundo plano

#### Opción A: Instalación Completa (con procesamiento en segundo plano)

Si desea habilitar el procesamiento de planillas grandes en segundo plano, necesita **ambos** servicios y Redis:

```bash
# Instalar Redis
sudo apt-get install redis-server
sudo systemctl enable redis
sudo systemctl start redis

# Copiar archivos de servicio
sudo cp systemd/goerp-payroll.service /etc/systemd/system/
sudo cp systemd/goerp-payroll-worker.service /etc/systemd/system/

# Editar variables de entorno en ambos archivos
sudo nano /etc/systemd/system/goerp-payroll.service
sudo nano /etc/systemd/system/goerp-payroll-worker.service

# Cambiar al menos:
# - DATABASE_URL
# - SECRET_KEY
# - REDIS_URL
# - ADMIN_USER y ADMIN_PASSWORD

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar e iniciar servicios (worker primero)
sudo systemctl enable goerp-payroll-worker
sudo systemctl enable goerp-payroll
sudo systemctl start goerp-payroll-worker
sudo systemctl start goerp-payroll

# Verificar estado
sudo systemctl status goerp-payroll-worker
sudo systemctl status goerp-payroll
```

#### Opción B: Instalación Básica (sin procesamiento en segundo plano)

Si no necesita procesamiento en segundo plano, puede instalar solo el servicio principal:

```bash
# Copiar y editar el archivo de servicio principal
sudo cp systemd/goerp-payroll.service /etc/systemd/system/

# Editar el archivo y cambiar QUEUE_ENABLED=0
sudo nano /etc/systemd/system/goerp-payroll.service

# Cambiar:
# Environment="QUEUE_ENABLED=0"

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar e iniciar el servicio
sudo systemctl enable goerp-payroll
sudo systemctl start goerp-payroll

# Verificar estado
sudo systemctl status goerp-payroll
```

!!! info "Procesamiento en Segundo Plano"
    El worker Dramatiq es **requerido** cuando:
    
    - `QUEUE_ENABLED=1`
    - Redis está disponible
    - Las planillas tienen más empleados que `BACKGROUND_PAYROLL_THRESHOLD` (default: 100)
    
    Si no se cumple alguna condición, el cálculo se ejecuta sincrónicamente.

Para más detalles sobre la configuración de systemd, consulte [systemd/README.md](../../systemd/README.md).

### 6. Configurar Proxy Inverso (Nginx)

```bash
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/coati
```

```nginx
server {
    listen 80;
    server_name tu_dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/coati /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Configurar HTTPS (Recomendado)

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu_dominio.com
```

## Verificar la Instalación

Después de la instalación, verifique que todo funciona correctamente:

1. Acceda a la aplicación en su navegador
2. Inicie sesión con las credenciales configuradas
3. Verifique que puede acceder a todas las secciones del menú

!!! tip "Primeros Pasos"
    Continúe con la [Configuración Inicial](configuracion.md) para preparar el sistema para su uso.
