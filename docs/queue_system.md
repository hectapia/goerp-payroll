# Queue System

## Resumen

El sistema de colas de GoERP Payroll usa **Dramatiq + Redis** para ejecutar tareas en segundo plano.

No existe fallback a Huey. Si Redis no está disponible, el selector retorna `NoopQueueDriver` y las operaciones sensibles (como cálculo de planilla) deben ejecutarse en modo síncrono.

## Backends soportados

### 1. Dramatiq + Redis

Backend soportado para procesamiento en segundo plano.

Requisitos:
- `dramatiq[redis]`
- `redis`
- `REDIS_URL` accesible desde la aplicación y workers

### 2. NoopQueueDriver

Driver de degradación controlada.

Uso:
- tests
- entornos sin Redis
- escenarios donde background no está disponible

`NoopQueueDriver` **no procesa tareas en background**.

## Selección de driver (`goerp_payroll/queue/selector.py`)

Reglas de selección:

1. Si está en entorno de test (`TESTING`, pytest, etc.) → `NoopQueueDriver`
2. Si `REDIS_URL`/`CACHE_REDIS_URL` responde ping y Dramatiq inicializa → `DramatiqDriver`
3. En cualquier otro caso → `NoopQueueDriver`

`force_backend` solo acepta `"dramatiq"`.

## Variables de entorno

```bash
# Habilita/deshabilita uso de cola desde la app
QUEUE_ENABLED=1

# URL de Redis para Dramatiq
REDIS_URL=redis://localhost:6379/0

# Umbral de empleados para activar cálculo de planilla en background
BACKGROUND_PAYROLL_THRESHOLD=100
```

## Workers

Iniciar workers Dramatiq:

```bash
dramatiq goerp_payroll.queue.tasks --threads 8 --processes 4
```

## Integración con planillas

Para cálculo de planillas, el background solo debe usarse cuando se cumpla:

- `QUEUE_ENABLED=true`
- Redis disponible
- Driver seleccionado = `DramatiqDriver`
- cantidad de empleados > `BACKGROUND_PAYROLL_THRESHOLD`

Si no se cumple, el flujo debe permanecer síncrono.

## Troubleshooting

### Redis no disponible

Síntoma:
- el sistema no encola tareas
- el driver activo es Noop

Acciones:
1. Verificar Redis en ejecución
2. Verificar `REDIS_URL`
3. Verificar conectividad desde app/worker
4. Reiniciar worker Dramatiq

### Worker inactivo

Síntoma:
- tareas encoladas sin avance

Acciones:
1. Levantar worker Dramatiq
2. Revisar logs de worker
3. Validar que use el mismo `REDIS_URL` que la app
