black goerp_payroll
ruff check goerp_payroll
flake8 goerp_payroll
pylint goerp_payroll -j 0
mypy goerp_payroll
pytest -n auto tests/
pytest -m validation -n auto tests/
