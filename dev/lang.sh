# Actualizar archivo de traducción
# Extraer nuevos textos
pybabel extract -F babel.cfg -o goerp_payroll/translations/messages.pot .

# Actualizar archivos de idioma
pybabel update -i goerp_payroll/translations/messages.pot -d goerp_payroll/translations

# Luego edita los .po y recompila
pybabel compile -d goerp_payroll/translations