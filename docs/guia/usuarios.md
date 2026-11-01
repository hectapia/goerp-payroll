# Gestión de Usuarios

GoERP Payroll permite administrar usuarios con diferentes niveles de acceso al sistema.

## Acceder al Módulo

1. Inicie sesión como administrador
2. Navegue a **Configuración > Usuarios**

## Tipos de Usuario

El sistema soporta los siguientes tipos de usuario:

| Tipo | Descripción | Permisos |
|------|-------------|----------|
| **admin** | Administrador | Acceso completo a todas las funcionalidades |
| **hhrr** | Recursos Humanos | Gestión de personal y nóminas |
| **audit** | Auditoría | Acceso de solo lectura para auditoría |

## Crear Nuevo Usuario

1. Haga clic en **Nuevo Usuario**
2. Complete el formulario:

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| Usuario | Nombre de usuario para iniciar sesión | Sí |
| Contraseña | Contraseña (mínimo 6 caracteres) | Sí |
| Nombre | Nombre del usuario | No |
| Apellido | Apellido del usuario | No |
| Correo electrónico | Email del usuario | No |
| Tipo de usuario | Rol del usuario en el sistema | Sí |
| Activo | Si el usuario puede iniciar sesión | Sí |

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
