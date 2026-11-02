# Gestión de Usuarios

GoERP Payroll permite administrar usuarios con diferentes niveles de acceso al sistema.

## Acceder al Módulo

1. Inicie sesión como administrador
2. Navegue a **Configuración > Usuarios**

## Tipos de Usuario

El sistema soporta los siguientes tipos de usuario:

| Tipo | Descripción | Permisos y Alcance |
|------|-------------|---------------------|
| **admin** | Administrador | Acceso total al sistema, gestión de empresas y usuarios, y carga masiva de empleados. |
| **hhrr** | Recursos Humanos | Gestión de personal y nóminas **exclusivamente de su propia empresa**. El usuario debe estar registrado como empleado activo en la empresa para poder operar. |
| **audit** | Auditoría | Acceso de solo lectura para auditoría en las empresas asignadas. |

!!! important "Requisito para Usuarios de Recursos Humanos (`hhrr`)"
    Todo usuario con perfil de Recursos Humanos **debe existir como empleado activo de la empresa que va a gestionar** (registrado con el mismo correo electrónico o nombre completo). La aplicación limita automáticamente su visibilidad únicamente a su empresa empleadora, impidiendo que gestione o visualice colaboradores de otras empresas.

## Crear Nuevo Usuario

1. Haga clic en **Nuevo Usuario**
2. Complete el formulario:

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| Usuario | Nombre de usuario para iniciar sesión | Sí |
| Contraseña | Contraseña (mínimo 6 caracteres) | Sí |
| Nombre | Nombre del usuario | No |
| Apellido | Apellido del usuario | No |
| Correo electrónico | Email del usuario (usado para vincular con su ficha de empleado) | No |
| Tipo de usuario | Rol del usuario en el sistema (`admin`, `hhrr`, `audit`) | Sí |
| Activo | Si el usuario puede iniciar sesión | Sí |
| Empresas asignadas | Empresas a las que el usuario tiene acceso (para usuarios de auditoría o complementarios) | No |

3. Haga clic en **Guardar**

!!! warning "Seguridad de Contraseñas"
    Las contraseñas se almacenan de forma segura usando el algoritmo Argon2. Nunca se almacenan en texto plano.

## Editar Usuario

1. En la lista de usuarios, haga clic en el usuario que desea editar
2. Modifique los campos necesarios
3. Haga clic en **Guardar**

!!! info "Cambiar Contraseña"
    Para cambiar la contraseña de un usuario, ingrese la nueva contraseña en el campo correspondiente. Si deja el campo vacío, la contraseña no cambiará.

## Desactivar Usuario

Para desactivar un usuario sin eliminarlo:

1. Edite el usuario
2. Desmarque la casilla **Activo**
3. Haga clic en **Guardar**

El usuario no podrá iniciar sesión mientras esté desactivado.

## Buenas Prácticas

### Seguridad

- Use contraseñas fuertes (mínimo 12 caracteres, combinando letras, números y símbolos)
- No comparta credenciales entre usuarios
- Desactive usuarios que ya no necesiten acceso
- Cambie la contraseña del administrador después de la instalación

### Gestión de Accesos

- Asigne el tipo de usuario más restrictivo posible
- Use el tipo `audit` para usuarios que solo necesitan consultar información
- Use el tipo `hhrr` para el personal de recursos humanos
- Reserve el tipo `admin` para administradores del sistema

## Ejemplo de Configuración

Una configuración típica podría incluir:

```
Usuarios
├── admin (admin) - Administrador del sistema
├── maria.rh (hhrr) - Encargada de Recursos Humanos
├── juan.rh (hhrr) - Asistente de Recursos Humanos
└── carlos.audit (audit) - Auditor externo
```

## Solución de Problemas

### "Usuario o contraseña incorrectos"

- Verifique que el usuario esté activo
- Verifique que está usando el nombre de usuario correcto
- Intente restablecer la contraseña

### "No autorizado"

- Verifique que el usuario tiene el tipo correcto para la acción
- Contacte al administrador para ajustar permisos
