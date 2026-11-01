# Campos Personalizados

Los campos personalizados permiten extender la información de los empleados con datos adicionales específicos a las necesidades de su organización.

## ¿Qué son los Campos Personalizados?

Los campos personalizados son atributos adicionales que puede definir para almacenar información específica de empleados que no está incluida en los campos estándar del sistema. Por ejemplo:

- Número de licencia de conducir
- Tipo de sangre
- Talla de uniforme
- Alergias
- Contacto de emergencia
- Número de cuenta bancaria secundaria
- Cualquier otro dato relevante para su organización

## Tipos de Campos

El sistema soporta diferentes tipos de campos personalizados:

- **Texto**: Para información alfanumérica general
- **Número**: Para valores numéricos
- **Fecha**: Para fechas específicas
- **Booleano**: Para valores verdadero/falso (Sí/No)
- **Lista de opciones**: Para seleccionar de un conjunto predefinido de valores

## Gestión de Campos Personalizados

### Crear un Campo Personalizado

1. Acceda al menú **Configuración** → **Campos Personalizados**
2. Haga clic en **Nuevo Campo Personalizado**
3. Complete la información:
   - **Nombre**: Nombre descriptivo del campo (ej: "Tipo de Sangre")
   - **Código**: Identificador único interno (ej: "tipo_sangre")
   - **Tipo de Campo**: Seleccione el tipo apropiado
   - **Orden**: Orden de visualización en el formulario
   - **Requerido**: Marque si el campo es obligatorio
   - **Visible**: Marque si el campo debe mostrarse en el formulario
   - **Descripción**: Ayuda o instrucciones para el usuario
   - **Opciones**: Si es lista de opciones, defina los valores (separados por comas)
4. Haga clic en **Guardar**

### Editar un Campo Personalizado

1. En la lista de campos personalizados, haga clic en **Editar** junto al campo deseado
2. Modifique la información necesaria
3. Haga clic en **Actualizar**

!!! warning "Precaución"
    Cambiar el tipo de un campo que ya tiene datos puede causar pérdida de información. Asegúrese de que el nuevo tipo sea compatible con los datos existentes.

### Eliminar un Campo Personalizado

1. En la lista de campos personalizados, haga clic en **Eliminar** junto al campo deseado
2. Confirme la eliminación

!!! danger "Advertencia"
    Al eliminar un campo personalizado, se perderán todos los datos almacenados en ese campo para todos los empleados. Esta acción no se puede deshacer.

## Uso en Empleados

Una vez creados los campos personalizados:

1. Al crear o editar un empleado, verá una sección de **Campos Personalizados**
2. Complete los campos según sea necesario
3. Los campos marcados como requeridos deben completarse para poder guardar el empleado

## Orden de Visualización

Los campos personalizados se muestran en el formulario de empleados según el valor del campo **Orden**. Los campos con menor número de orden aparecen primero.

Para reorganizar los campos:

1. Edite cada campo personalizado
2. Asigne el número de orden deseado
3. Guarde los cambios

## Campos Visibles vs. Ocultos

Puede marcar campos como **No Visibles** para:

- Mantener datos históricos sin mostrarlos en el formulario
- Ocultar temporalmente campos que no se están usando
- Datos que solo deben ser visibles en ciertos contextos

Los campos ocultos mantienen sus valores, pero no se muestran en el formulario de empleados.

## Mejores Prácticas

### Nomenclatura de Códigos

Use códigos descriptivos y consistentes:

- Use minúsculas y guiones bajos: `tipo_sangre`, `numero_licencia`
- Evite caracteres especiales o espacios
- Sea descriptivo pero conciso

### Organización de Campos

- Agrupe campos relacionados usando números de orden consecutivos
- Coloque los campos más importantes primero
- Use descripciones claras para ayudar a los usuarios

### Listas de Opciones

Para campos de tipo lista:

- Defina todas las opciones posibles separadas por comas: `A+, A-, B+, B-, O+, O-, AB+, AB-`
- Sea consistente con el formato (mayúsculas, abreviaciones, etc.)
- Evite opciones demasiado largas

### Campos Requeridos

Marque como requeridos solo los campos realmente necesarios para evitar frustración de usuarios.

## Ejemplos de Uso

### Información Médica

```
Nombre: Tipo de Sangre
Código: tipo_sangre
Tipo: Lista de opciones
Opciones: A+, A-, B+, B-, O+, O-, AB+, AB-
Requerido: No
Orden: 1
```

### Información de Contacto

```
Nombre: Contacto de Emergencia
Código: contacto_emergencia
Tipo: Texto
Requerido: Sí
Orden: 2

Nombre: Teléfono de Emergencia
Código: telefono_emergencia
Tipo: Texto
Requerido: Sí
Orden: 3
```

### Información Bancaria

```
Nombre: Banco Secundario
Código: banco_secundario
Tipo: Texto
Requerido: No
Orden: 10

Nombre: Cuenta Bancaria Secundaria
Código: cuenta_bancaria_secundaria
Tipo: Texto
Requerido: No
Orden: 11
```

## Limitaciones

- Los campos personalizados solo están disponibles para empleados
- No se pueden usar en fórmulas de cálculo de nómina (use campos estándar o novedades para eso)
- El número máximo recomendado de campos personalizados es 20 para mantener un formulario manejable

## Seguridad

- Solo usuarios con permisos administrativos pueden crear, editar o eliminar campos personalizados
- Todos los usuarios con acceso a empleados pueden ver y editar los valores de campos personalizados visibles
- Los datos de campos personalizados se almacenan de forma segura en la base de datos

## Soporte

Para obtener ayuda adicional sobre campos personalizados, consulte el [Glosario](../referencia/glosario.md) o la sección de [Preguntas Frecuentes](../referencia/faq.md).
