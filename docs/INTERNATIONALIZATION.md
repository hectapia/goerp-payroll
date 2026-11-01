# Internationalization (i18n) Implementation

## Overview

The GoERP Payroll system now supports multiple languages through Flask-Babel integration. This document describes the implementation and how to use the internationalization features.

## Supported Languages

- **Spanish (es)** - Source language
- **English (en)** - Default language for new installations

## Features

### 1. Database-Stored Language Configuration

Language preference is stored in the `configuracion_global` table, allowing persistent configuration across sessions.

### 2. Environment Variable Support

Set the initial language using the `COATI_LANG` environment variable:

```bash
# Use English (default)
export COATI_LANG=en

# Use Spanish
export COATI_LANG=es
```

The environment variable is only used during initial setup when no configuration exists in the database.

### 3. Performance-Optimized Caching

Language settings are cached in memory to avoid repeated database queries:

- **Thread-safe**: Uses locks to ensure safe concurrent access
- **Automatic invalidation**: Cache is cleared when language is changed
- **Non-blocking**: Gracefully handles database unavailability

### 4. User-Friendly Web Interface

Users can change the language through the web interface:

1. Navigate to **Configuración → Configuración Global**
2. Select desired language from dropdown
3. Click "Guardar Cambios"
4. Changes take effect immediately (no restart required)

## Architecture

### Components

```
goerp_payroll/
├── model.py                    # ConfiguracionGlobal database model
├── locale_config.py            # Language configuration and caching
├── __init__.py                 # Flask-Babel integration
├── i18n.py                     # Translation helper functions
├── translations/               # Translation files
│   ├── en/LC_MESSAGES/
│   │   ├── messages.po        # English translations
│   │   └── messages.mo        # Compiled English
│   └── es/LC_MESSAGES/
│       ├── messages.po        # Spanish translations
│       └── messages.mo        # Compiled Spanish
└── vistas/
    └── configuracion.py       # Configuration views
```

### Database Model

```python
class ConfiguracionGlobal(database.Model, BaseTabla):
    """Global configuration settings."""
    __tablename__ = "configuracion_global"
    
    idioma = database.Column(
        database.String(10), nullable=False, default="en"
    )
```

### Caching Implementation

The language setting is cached using a module-level variable with thread-safe access:

```python
_language_cache = None
_cache_lock = Lock()

def get_language_from_db() -> str:
    """Get language with caching."""
    global _language_cache
    
    with _cache_lock:
        if _language_cache is not None:
            return _language_cache
    
    # Query database and update cache
    ...
```

### Flask-Babel Integration

```python
def get_locale():
    """Locale selector for Flask-Babel."""
    try:
        from goerp_payroll.locale_config import get_language_from_db
        return get_language_from_db()
    except Exception:
        return "en"  # Fallback

# Configure Babel
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"
babel.init_app(app, locale_selector=get_locale)
```

## Usage

### In Python Code

```python
from goerp_payroll.i18n import _, _l, _n

# Simple translation
message = _("Usuario creado exitosamente")

# With variable interpolation
message = _("Bienvenido %(name)s", name=user.nombre)

# Lazy translation (for forms)
field_label = _l("Nombre de usuario")

# Plural forms
count = 5
message = _n("%(num)d empleado", "%(num)d empleados", count)
```

### In Jinja2 Templates

```html
<!-- Simple translation -->
<h1>{{ _('Bienvenido') }}</h1>

<!-- With variable -->
<p>{{ _('Usuario: %(username)s', username=current_user.usuario) }}</p>

<!-- In attributes -->
<input placeholder="{{ _('Ingrese su nombre') }}">
```

### Programmatically Change Language

```python
from goerp_payroll.locale_config import set_language_in_db

# Change to English
set_language_in_db("en")

# Change to Spanish
set_language_in_db("es")
```

## Translation Management

For developers managing translations, see [TRANSLATIONS.md](./TRANSLATIONS.md) for detailed instructions on:

- Extracting translatable strings
- Updating translation catalogs
- Compiling translations
- Adding new languages

## Testing

Tests are configured to use Spanish as the default language:

```python
# In tests/conftest.py
os.environ["COATI_LANG"] = "es"
```

This ensures tests run with Spanish strings, matching the source language.

## Performance Considerations

1. **Cache Hit Rate**: After the first database query, subsequent requests use the cached value
2. **Cache Invalidation**: Only occurs when language is explicitly changed via `set_language_in_db()`
3. **Thread Safety**: Multiple threads can safely access the cached value simultaneously
4. **Graceful Degradation**: If database is unavailable, falls back to default English

## Troubleshooting

### Language not changing

1. Check that `.mo` files are compiled:
   ```bash
   pybabel compile -d goerp_payroll/translations
   ```

2. Verify database configuration:
   ```python
   from goerp_payroll.model import ConfiguracionGlobal, db
   config = db.session.query(ConfiguracionGlobal).first()
   print(config.idioma if config else "Not configured")
   ```

3. Clear cache manually if needed:
   ```python
   from goerp_payroll.locale_config import invalidate_language_cache
   invalidate_language_cache()
   ```

### Translations not appearing

1. Ensure `.mo` files exist in `goerp_payroll/translations/*/LC_MESSAGES/`
2. Check that Flask-Babel is properly initialized
3. Verify translation strings are marked with `_()` function
4. Restart application if using production server

## Security

- Language selection is validated against supported languages list
- Invalid language codes are rejected with `ValueError`
- Thread-safe implementation prevents race conditions
- No SQL injection risk (uses SQLAlchemy ORM)

## Future Enhancements

Potential improvements for future versions:

- Add more languages (French, Portuguese, etc.)
- Per-user language preferences (override global setting)
- Browser language detection for initial setup
- Translation progress tracking UI
- Crowdsourced translation platform integration

## References

- [Flask-Babel Documentation](https://python-babel.github.io/flask-babel/)
- [Translation Management Guide](./TRANSLATIONS.md)
- [Issue #XX - Completar soporte para internacionalización](https://github.com/williamjmorenor/coati/issues/XX)
