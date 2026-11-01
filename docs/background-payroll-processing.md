# Background Payroll Processing

## Overview

This feature enables automatic background processing of large payrolls to prevent UI freezing and provide real-time feedback to users during lengthy calculations.

## When is Background Processing Used?

Background processing is automatically triggered when **all** conditions are met:
- `QUEUE_ENABLED` is active
- Redis is available and the selected queue driver is Dramatiq
- A planilla has more employees than the configured threshold
- Default threshold: **100 employees**
- Threshold is configurable via environment variable

## Configuration

### Setting the Threshold

You can adjust the threshold based on your system's performance:

```bash
# For systems with complex formulas or slower performance
export BACKGROUND_PAYROLL_THRESHOLD=50

# For high-performance systems
export BACKGROUND_PAYROLL_THRESHOLD=200

# Default (if not set)
# BACKGROUND_PAYROLL_THRESHOLD=100
```

### Configuration File

You can also set it in your configuration file (`goerp-payroll.conf`):

```ini
BACKGROUND_PAYROLL_THRESHOLD = 75
```

## User Experience

### 1. Initiating Payroll Calculation

When a user executes a payroll for a planilla with more than the threshold number of employees:

1. The system creates a nomina record with status **"calculando"**
2. The background task is queued (Dramatiq + Redis)
3. User is redirected to the nomina detail page
4. A flash message informs the user: *"La nómina está siendo calculada en segundo plano. Se procesarán X empleados."*

### 2. Progress Monitoring

The nomina detail page shows:

#### Progress Indicator
- **Spinner animation** to show the system is active
- **Progress bar** showing percentage complete
- **Employee counters**:
  - Total employees
  - Employees processed
  - Employees with errors

#### Current Activity
- Alert showing which employee is currently being calculated
- Updates every 3 seconds

#### Activity Log
- Scrollable log showing:
  - "Calculando empleado N/Total: Employee Name"
  - "✓ Completado: Employee Name - Neto: $X,XXX.XX"
  - "✗ Error: Employee Name - Error message"
- Auto-scrolls to show latest activity
- Manual scroll is preserved (user can review earlier entries)

### 3. Completion

When calculation completes:
- Page automatically refreshes
- Status changes to **"generado"** (or **"error"** if critical failure)
- User can review results, approve, and apply the nomina

### 4. Error Handling

If some employees fail to process:
- Nomina status: **"generado"** (if majority succeeded) or **"error"** (if all failed)
- Warning alert shows number of employees with errors
- Expandable details list all errors
- Successfully calculated employees are saved

## Technical Details

> Note: No fallback to Huey is used. If Redis is unavailable, payroll calculation remains synchronous.

### Database Schema

New fields added to `Nomina` table:

```python
total_empleados              # Total number of employees
empleados_procesados         # Number processed so far
empleados_con_error          # Number that failed
errores_calculo             # Dict of employee_id: error_message
procesamiento_en_background  # Boolean flag
log_procesamiento           # List of activity log entries
empleado_actual             # Name of employee currently being processed
```

### Nomina States

New states in `NominaEstado` enum:
- `CALCULANDO`: Currently being calculated in background
- `ERROR`: Critical error during calculation
- `GENERADO`: Successfully generated (existing)
- `APROBADO`: Approved (existing)
- `APLICADO`: Applied/paid (existing)

### API Endpoint

`GET /planilla/<planilla_id>/nomina/<nomina_id>/progreso`

Returns JSON:
```json
{
  "estado": "calculando",
  "total_empleados": 150,
  "empleados_procesados": 75,
  "empleados_con_error": 2,
  "progreso_porcentaje": 50,
  "empleado_actual": "Juan Pérez",
  "log_procesamiento": [
    {
      "timestamp": "2024-01-15T10:30:45Z",
      "empleado": "María García",
      "status": "success",
      "message": "✓ Completado: María García - Neto: C$ 15,234.50"
    },
    ...
  ],
  "errores_calculo": {
    "empleado_id_1": "Error message"
  },
  "procesamiento_en_background": true
}
```

### Background Task

`process_large_payroll` task:
- Processes employees sequentially
- Updates database after each employee
- Logs progress in real-time
- Handles individual employee errors gracefully
- Continues processing remaining employees even if some fail

## Performance Considerations

### Threshold Selection

Choose your threshold based on:

1. **Formula Complexity**: Complex formulas (tax calculations, multiple deductions) → lower threshold (25-50)
2. **Server Performance**: 
   - Shared/low-spec servers → lower threshold (50-75)
   - Dedicated/high-spec servers → higher threshold (150-200)
3. **Database Performance**: Slower databases → lower threshold
4. **User Patience**: Expected wait time should not exceed 2-3 seconds for synchronous processing

### Monitoring

Monitor these metrics to optimize threshold:
- Average time per employee calculation
- Total time for payroll runs
- Database connection pool usage
- Queue worker performance

## Troubleshooting

### Nomina Stuck in "Calculando" State

**Causes:**
- Queue worker not running
- Background task crashed
- Database connection lost

**Solutions:**
1. Check queue worker status
2. Check application logs for errors
3. Manually check progress via API endpoint
4. If stuck, recalculate nomina (will restart process)

### High Error Rate

**Causes:**
- Invalid employee data
- Missing required configuration (exchange rates, tax tables)
- Formula errors

**Solutions:**
1. Review error messages in `errores_calculo`
2. Fix data issues
3. Recalculate nomina

### Slow Processing

**Causes:**
- Complex formulas
- Slow database
- Insufficient resources

**Solutions:**
1. Lower threshold to use background processing earlier
2. Optimize formulas
3. Add database indexes
4. Scale up server resources
5. Consider parallel processing (for very large payrolls)

## Best Practices

1. **Test Threshold**: Test with your typical payroll size to find optimal threshold
2. **Monitor Performance**: Regularly review processing times
3. **Review Logs**: Check activity logs for patterns in errors
4. **User Communication**: Train users on what to expect during background processing
5. **Database Maintenance**: Keep database optimized for best performance

## Future Enhancements

Possible improvements:
- Parallel processing (multiple employees simultaneously)
- Email notifications when calculation completes
- Pause/resume capability
- Priority queues for urgent payrolls
- Historical performance metrics
- Automatic threshold adjustment based on performance
