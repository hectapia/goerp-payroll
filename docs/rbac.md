# Control de Acceso Basado en Roles (RBAC)

## Descripción General

El sistema GoERP Payroll implementa un sistema completo de Control de Acceso Basado en Roles (RBAC) para garantizar que los usuarios solo puedan acceder a las funcionalidades apropiadas según su rol.

## Tipos de Usuario

El sistema soporta tres tipos de usuario, cada uno con diferentes niveles de acceso:

### Admin (Administrador)

**Descripción**: Usuario con acceso completo a todas las funcionalidades del sistema.

**Permisos**:
- ✅ Crear, editar y eliminar empresas
- ✅ Crear, editar y eliminar usuarios
- ✅ Acceso completo a empleados
- ✅ Acceso completo a préstamos y adelantos
- ✅ Acceso completo a planillas (nóminas)
- ✅ Acceso completo a deducciones, percepciones y prestaciones
- ✅ Acceso completo a todas las configuraciones del sistema

**Casos de uso**:
- Configuración inicial del sistema
- Gestión de usuarios y permisos
- Creación de empresas
- Supervisión general del sistema

### HHRR (Recursos Humanos)

**Descripción**: Usuario con acceso completo a la gestión de personal y nóminas.

**Permisos**:
- ✅ Ver empresas (solo lectura)
- ❌ Crear, editar o eliminar empresas
- ❌ Gestionar usuarios
- ✅ Acceso completo a empleados (crear, editar, eliminar)
- ✅ Acceso completo a préstamos y adelantos
- ✅ Acceso completo a planillas (nóminas)
- ✅ Acceso completo a deducciones, percepciones y prestaciones
- ✅ Configurar y ejecutar nóminas
- ✅ Gestionar novedades de nómina

**Casos de uso**:
- Gestión diaria de empleados
- Procesamiento de nóminas
- Aprobación de préstamos
- Configuración de deducciones y percepciones

### Audit (Auditoría)

**Descripción**: Usuario con acceso de solo lectura para fines de auditoría.

**Permisos**:
- ✅ Ver todas las empresas
- ✅ Ver todos los empleados
- ✅ Ver todas las planillas y nóminas
- ✅ Ver deducciones, percepciones y prestaciones
- ✅ Ver préstamos y adelantos
- ✅ Exportar reportes y datos
- ❌ Crear, editar o eliminar cualquier registro
- ❌ Ejecutar nóminas
- ❌ Aprobar préstamos

**Casos de uso**:
- Auditorías internas
- Revisión de procesos de nómina
- Verificación de datos
- Generación de reportes de auditoría

## Implementación Técnica

### Decoradores RBAC

El sistema implementa tres decoradores principales para controlar el acceso:

#### `@require_role(*roles)`

Restringe el acceso a usuarios con roles específicos.

```python
from goerp_payroll.rbac import require_role
from goerp_payroll.enums import TipoUsuario

@app.route("/empresa/new")
@require_role(TipoUsuario.ADMIN)
def create_company():
    # Solo administradores pueden crear empresas
    pass

@app.route("/employee/new")
@require_role(TipoUsuario.ADMIN, TipoUsuario.HHRR)
def create_employee():
    # Admin y HHRR pueden crear empleados
    pass
```

#### `@require_read_access()`

Permite acceso de lectura a todos los usuarios autenticados. Los usuarios audit solo pueden leer, mientras que admin y hhrr también pueden modificar datos.

```python
from goerp_payroll.rbac import require_read_access

@app.route("/employee/")
@require_read_access()
def list_employees():
    # Todos los usuarios autenticados pueden ver la lista
    pass
```

#### `@require_write_access()`

Restringe las operaciones de escritura (crear, editar, eliminar) solo a usuarios admin y hhrr. Los usuarios audit son denegados.

```python
from goerp_payroll.rbac import require_write_access

@app.route("/employee/new", methods=["POST"])
@require_write_access()
def create_employee():
    # Solo admin y hhrr pueden crear empleados
    # Audit será denegado con error 403
    pass
```

### Funciones de Ayuda

El módulo `rbac.py` también proporciona funciones de ayuda para verificar roles:

```python
from goerp_payroll.rbac import is_admin, is_hhrr, is_audit, can_write

# Verificar si el usuario actual es admin
if is_admin():
    # Lógica para administradores
    pass

# Verificar si el usuario puede escribir
if can_write():
    # Mostrar botones de edición
    pass
```

## Matriz de Permisos

| Funcionalidad | Admin | HHRR | Audit |
|--------------|-------|------|-------|
| **Empresas** |
| Ver lista | ✅ | ✅ | ✅ |
| Crear | ✅ | ❌ | ❌ |
| Editar | ✅ | ❌ | ❌ |
| Eliminar | ✅ | ❌ | ❌ |
| **Usuarios** |
| Ver lista | ✅ | ❌ | ❌ |
| Crear | ✅ | ❌ | ❌ |
| Editar | ✅ | ❌ | ❌ |
| Eliminar | ✅ | ❌ | ❌ |
| **Empleados** |
| Ver lista | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ❌ |
| Editar | ✅ | ✅ | ❌ |
| Eliminar | ✅ | ✅ | ❌ |
| **Préstamos** |
| Ver lista | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ❌ |
| Aprobar | ✅ | ✅ | ❌ |
| Pagar | ✅ | ✅ | ❌ |
| **Planillas/Nóminas** |
| Ver lista | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ❌ |
| Editar | ✅ | ✅ | ❌ |
| Ejecutar | ✅ | ✅ | ❌ |
| Ver detalles | ✅ | ✅ | ✅ |
| **Deducciones/Percepciones/Prestaciones** |
| Ver lista | ✅ | ✅ | ✅ |
| Crear | ✅ | ✅ | ❌ |
| Editar | ✅ | ✅ | ❌ |
| Eliminar | ✅ | ✅ | ❌ |
| **Configuración** |
| Monedas | ✅ | ✅ | ✅ (solo lectura) |
| Tipos de cambio | ✅ | ✅ | ✅ (solo lectura) |
| Campos personalizados | ✅ | ✅ | ✅ (solo lectura) |
| Reglas de cálculo | ✅ | ✅ | ✅ (solo lectura) |

## Mensajes de Error

Cuando un usuario intenta acceder a una funcionalidad para la cual no tiene permisos, el sistema muestra mensajes apropiados:

- **403 Forbidden**: "No tiene permisos para acceder a esta funcionalidad."
- **403 Forbidden (Audit)**: "No tiene permisos para modificar datos. Su rol es de solo lectura."
- **Redirect a login**: "Favor iniciar sesión para acceder al sistema." (para usuarios no autenticados)

## Mejores Prácticas

### Para Desarrolladores

1. **Siempre use decoradores RBAC**: No confíe solo en ocultar elementos de UI. Siempre proteja las rutas con decoradores apropiados.

2. **Use `@require_read_access()` para vistas de lista/detalle**: Permite que usuarios audit vean los datos.

3. **Use `@require_write_access()` para operaciones de escritura**: Protege contra modificaciones no autorizadas.

4. **Use `@require_role()` para funcionalidades específicas**: Por ejemplo, solo admin puede gestionar empresas y usuarios.

5. **Valide permisos en templates**: Use las funciones de ayuda para mostrar/ocultar botones de acción.

```jinja2
{% if current_user.tipo in ['admin', 'hhrr'] %}
    <a href="{{ url_for('employee.edit', id=employee.id) }}" class="btn btn-primary">
        Editar
    </a>
{% endif %}
```

### Para Administradores

1. **Asigne roles apropiados**: Revise cuidadosamente los permisos antes de asignar roles.

2. **Use cuentas audit para revisiones**: Cree cuentas audit específicas para auditores externos o internos.

3. **Monitoree el campo `ultimo_acceso`**: Rastree cuándo los usuarios acceden al sistema.

4. **Cambie credenciales por defecto**: En producción, siempre cambie las credenciales por defecto del administrador.

5. **Revise logs de acceso**: Periódicamente revise los logs para detectar intentos de acceso no autorizado.

## Seguridad

El sistema RBAC implementa las siguientes medidas de seguridad:

1. **Control a nivel de ruta**: Todas las rutas están protegidas con decoradores RBAC.

2. **Validación en backend**: Los permisos se validan en el servidor, no solo en el cliente.

3. **Mensajes de error genéricos**: Se evita revelar información sensible en mensajes de error.

4. **Registro de accesos**: El campo `ultimo_acceso` registra el último acceso del usuario.

5. **Separación de responsabilidades**: Cada rol tiene permisos claramente definidos.

## Testing

El sistema incluye 50 tests automatizados que verifican todos los escenarios RBAC:

```bash
# Ejecutar tests RBAC
pytest tests/test_rbac.py -v

# Ejecutar todos los tests
pytest tests/ -v
```

Los tests verifican:
- Acceso correcto para cada rol
- Denegación apropiada de permisos
- Funcionalidad de decoradores
- Mensajes de error correctos

## Migración de Usuarios Existentes

Si ya tiene usuarios en el sistema sin el campo `tipo` configurado, ejecute:

```python
from goerp_payroll.model import Usuario, db
from goerp_payroll.enums import TipoUsuario

# Asignar tipo admin a usuarios existentes
usuarios = Usuario.query.filter_by(tipo=None).all()
for usuario in usuarios:
    usuario.tipo = TipoUsuario.ADMIN  # o el rol apropiado
    db.session.commit()
```

## Preguntas Frecuentes

**P: ¿Puede un usuario tener múltiples roles?**  
R: No, cada usuario tiene un único rol (tipo). Si necesita permisos mixtos, use el rol HHRR que tiene la mayoría de permisos de gestión.

**P: ¿Los usuarios audit pueden exportar datos?**  
R: Sí, los usuarios audit pueden exportar datos para auditorías, pero no pueden modificarlos.

**P: ¿Puedo crear roles personalizados?**  
R: Actualmente el sistema soporta tres roles fijos. Para roles personalizados, necesitaría extender el sistema.

**P: ¿Qué sucede si no hay administradores?**  
R: El sistema crea automáticamente un usuario admin por defecto al iniciar.

**P: ¿Cómo cambio el rol de un usuario?**  
R: Solo los administradores pueden editar usuarios y cambiar sus roles desde la interfaz de gestión de usuarios.
