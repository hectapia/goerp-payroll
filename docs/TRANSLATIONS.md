# Translation Management Guide

This document describes how to manage translations in the GoERP Payroll system.

## Overview

The system uses Flask-Babel for internationalization (i18n). Source strings are in **Spanish** and are translated to **English**.

Supported languages:
- `es` - Español (Spanish) - Source language
- `en` - English - Translation target

## Directory Structure

```
goerp_payroll/
├── translations/          # Translation files directory
│   ├── en/               # English translations
│   │   └── LC_MESSAGES/
│   │       ├── messages.po   # Editable translation catalog
│   │       └── messages.mo   # Compiled binary (auto-generated)
│   └── es/               # Spanish translations
│       └── LC_MESSAGES/
│           ├── messages.po   # Editable translation catalog
│           └── messages.mo   # Compiled binary (auto-generated)
├── babel.cfg             # Babel extraction configuration
└── messages.pot          # Translation template (source)
```

## Translation Workflow

### 1. Extract Translatable Strings (Create .pot template)

When you add new translatable strings to the code or templates, extract them to create/update the translation template:

```bash
# From the project root directory
pybabel extract -F babel.cfg -k _ -k _l -k _n:1,2 -o messages.pot .
```

**What this does:**
- Scans all Python files (`**.py`) and Jinja2 templates (`**/templates/**.html`)
- Looks for translation functions: `_()`, `_l()`, `_n()`
- Creates/updates `messages.pot` with all found strings

### 2. Initialize New Language (One-time only)

To add a new language (only needed once per language):

```bash
# Initialize Spanish catalog (already done)
pybabel init -i messages.pot -d goerp_payroll/translations -l es

# Initialize English catalog (already done)
pybabel init -i messages.pot -d goerp_payroll/translations -l en
```

**Note:** This step is only needed when adding a completely new language.

### 3. Update Translation Catalogs (After extracting strings)

After extracting new strings to `messages.pot`, update the language-specific `.po` files:

```bash
# Update Spanish catalog
pybabel update -i messages.pot -d goerp_payroll/translations -l es

# Update English catalog
pybabel update -i messages.pot -d goerp_payroll/translations -l en
```

**What this does:**
- Merges new strings from `messages.pot` into existing `.po` files
- Marks new strings as needing translation
- Preserves existing translations
- Marks removed strings as obsolete (but keeps them commented)

### 4. Translate Strings

Edit the `.po` files manually to add translations:

**For Spanish (es):**
```bash
# Edit: goerp_payroll/translations/es/LC_MESSAGES/messages.po
# Spanish is the source language, so msgstr should match msgid
```

**For English (en):**
```bash
# Edit: goerp_payroll/translations/en/LC_MESSAGES/messages.po
# Translate Spanish strings (msgid) to English (msgstr)
```

**Example `.po` file format:**
```po
# Spanish string (msgid) → English translation (msgstr)
msgid "Usuario"
msgstr "User"

msgid "Contraseña"
msgstr "Password"

msgid "Guardar"
msgstr "Save"
```

### 5. Compile Translations (Create .mo files)

After editing translations, compile them to binary `.mo` files:

```bash
# Compile all languages
pybabel compile -d goerp_payroll/translations

# Or compile specific language
pybabel compile -d goerp_payroll/translations -l en
pybabel compile -d goerp_payroll/translations -l es
```

**What this does:**
- Converts human-readable `.po` files to binary `.mo` files
- `.mo` files are used by the application at runtime
- Must be done before testing translations

**Important:** Always compile after editing `.po` files!

## Complete Workflow Example

When you modify code and add new translatable strings:

```bash
# 1. Extract new strings from source code
pybabel extract -F babel.cfg -k _ -k _l -k _n:1,2 -o messages.pot .

# 2. Update language catalogs
pybabel update -i messages.pot -d goerp_payroll/translations -l es
pybabel update -i messages.pot -d goerp_payroll/translations -l en

# 3. Edit the .po files to add translations
# For English: goerp_payroll/translations/en/LC_MESSAGES/messages.po
nano goerp_payroll/translations/en/LC_MESSAGES/messages.po

# 4. Compile to binary .mo files
pybabel compile -d goerp_payroll/translations

# 5. Restart the application to see changes
# (or just reload the page if using Flask debug mode)
```

## Translation Functions in Code

Use these functions to mark strings as translatable:

### Python Code

```python
from goerp_payroll.i18n import _, _l, _n

# Regular translation
message = _("Usuario creado exitosamente")

# With variable interpolation
message = _("Bienvenido %(name)s", name=user.nombre)

# Lazy translation (for forms and module-level strings)
field_label = _l("Nombre de usuario")

# Plural forms
message = _n("%(num)d empleado", "%(num)d empleados", count)
```

### Jinja2 Templates

```html
<!-- Simple translation -->
<h1>{{ _('Bienvenido') }}</h1>

<!-- With variable -->
<p>{{ _('Usuario: %(username)s', username=current_user.usuario) }}</p>

<!-- In attributes -->
<input type="text" placeholder="{{ _('Ingrese su nombre') }}">
```

## Configuration

### babel.cfg

The extraction configuration is in `babel.cfg`:

```ini
[python: **.py]
[jinja2: **/templates/**.html]
encoding = utf-8
```

### Flask-Babel Setup

In `goerp_payroll/__init__.py`:

```python
# Configure Flask-Babel
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"
babel.init_app(app, locale_selector=get_locale)
```

## Language Selection

### Default Language

The default language is **English** (`en`), but the initial language can be set using the `COATI_LANG` environment variable:

```bash
# Set initial language to Spanish
export COATI_LANG=es

# Set initial language to English (default)
export COATI_LANG=en
```

### Database Configuration

The user can change the language through the web interface at **Configuración → Configuración Global**. The selected language is stored in the `configuracion_global` table and cached for performance.

### Caching

Language settings are cached to avoid repeated database queries. The cache is automatically invalidated when the user changes the language.

## Troubleshooting

### Translations not appearing

1. **Check if .mo files exist:**
   ```bash
   ls -la goerp_payroll/translations/*/LC_MESSAGES/messages.mo
   ```

2. **Recompile translations:**
   ```bash
   pybabel compile -d goerp_payroll/translations
   ```

3. **Restart the application:**
   - In development, Flask should auto-reload
   - In production, restart the web server

### New strings not extracted

1. **Check babel.cfg paths are correct**
2. **Verify translation functions are used:** `_()`, `_l()`, `_n()`
3. **Re-run extraction command**

### Language not switching

1. **Check database:** Ensure `configuracion_global` table exists
2. **Check cache:** Language cache might need invalidation
3. **Check locale selector:** Verify `get_locale()` function in `__init__.py`

## Development Tips

1. **Always extract first:** Run `pybabel extract` before `pybabel update`
2. **Update, then translate:** Use `pybabel update` to merge new strings, then edit `.po` files
3. **Compile before testing:** Always run `pybabel compile` after editing `.po` files
4. **Use msgfmt for validation:** Check `.po` files for errors:
   ```bash
   msgfmt --check goerp_payroll/translations/en/LC_MESSAGES/messages.po
   ```

## Quick Reference

| Task | Command |
|------|---------|
| Extract strings | `pybabel extract -F babel.cfg -k _ -k _l -k _n:1,2 -o messages.pot .` |
| Update catalogs | `pybabel update -i messages.pot -d goerp_payroll/translations` |
| Compile translations | `pybabel compile -d goerp_payroll/translations` |
| Initialize new language | `pybabel init -i messages.pot -d goerp_payroll/translations -l <code>` |
| Check .po file | `msgfmt --check <path-to-messages.po>` |

## References

- [Flask-Babel Documentation](https://python-babel.github.io/flask-babel/)
- [Babel Documentation](http://babel.pocoo.org/en/latest/)
- [GNU gettext Manual](https://www.gnu.org/software/gettext/manual/)
