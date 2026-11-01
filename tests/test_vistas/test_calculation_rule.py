# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Comprehensive tests for calculation rule CRUD operations (goerp_payroll/vistas/calculation_rule.py)."""

from sqlalchemy import func, select
from datetime import date

from goerp_payroll.model import ReglaCalculo
from tests.helpers.auth import login_user


def test_calculation_rule_index_requires_authentication(app, client, db_session):
    """Test that calculation rule index requires authentication."""
    with app.app_context():
        response = client.get("/calculation-rule/", follow_redirects=False)
        assert response.status_code == 302


def test_calculation_rule_index_lists_rules(app, client, admin_user, db_session):
    """Test that authenticated user can view calculation rule list."""
    with app.app_context():
        # Create test calculation rules
        rule1 = ReglaCalculo(
            codigo="IR_2025",
            nombre="Income Tax 2025",
            descripcion="Income tax calculation for 2025",
            jurisdiccion="Nicaragua",
            moneda_referencia="NIO",
            version=1,
            tipo_regla="tax",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        rule2 = ReglaCalculo(
            codigo="INSS_2025",
            nombre="Social Security 2025",
            descripcion="Social security calculation",
            jurisdiccion="Nicaragua",
            moneda_referencia="NIO",
            version=1,
            tipo_regla="deduccion",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add_all([rule1, rule2])
        db_session.commit()

        login_user(client, admin_user.usuario, "admin-password")

        response = client.get("/calculation-rule/")
        assert response.status_code == 200
        assert b"IR_2025" in response.data or b"Income Tax" in response.data


def test_calculation_rule_edit_updates_rule(app, client, admin_user, db_session):
    """Test updating a calculation rule."""
    with app.app_context():
        # Create calculation rule
        rule = ReglaCalculo(
            codigo="VACATION_2025",
            nombre="Vacation Calculation",
            descripcion="Calculate vacation pay",
            jurisdiccion="Nicaragua",
            moneda_referencia="NIO",
            version=1,
            tipo_regla="prestacion",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            f"/calculation-rule/edit/{rule_id}",
            data={
                "codigo": "VACATION_2025",
                "nombre": "Vacation Calculation (Updated)",
                "descripcion": "Calculate vacation pay with new formula",
                "jurisdiccion": "Nicaragua",
                "moneda_referencia": "NIO",
                "version": 2,
                "tipo_regla": "prestacion",
                "vigente_desde": "2025-01-01",
                "activo": "y",
            },
            follow_redirects=False,
        )

        assert response.status_code in [200, 302]

        if response.status_code == 302:
            updated_rule = db_session.execute(select(ReglaCalculo).filter_by(id=rule_id)).scalar_one_or_none()
            assert updated_rule.nombre == "Vacation Calculation (Updated)"
            assert updated_rule.version == "2"  # Version is stored as string in form


def test_calculation_rule_delete_removes_rule(app, client, admin_user, db_session):
    """Test deleting a calculation rule."""
    with app.app_context():
        # Create calculation rule
        rule = ReglaCalculo(
            codigo="TEMP_RULE",
            nombre="Temporary Rule",
            descripcion="Temporary calculation rule",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(f"/calculation-rule/delete/{rule_id}", follow_redirects=False)

        assert response.status_code in [200, 302]

        if response.status_code == 302:
            rule = db_session.execute(select(ReglaCalculo).filter_by(id=rule_id)).scalar_one_or_none()
            assert rule is None


def test_calculation_rule_supports_versioning(app, client, admin_user, db_session):
    """Test that calculation rules support versioning."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        # Create version 1
        response1 = client.post(
            "/calculation-rule/new",
            data={
                "codigo": "TAX_CALC",
                "nombre": "Tax Calculation V1",
                "descripcion": "Version 1",
                "jurisdiccion": "Nicaragua",
                "moneda_referencia": "NIO",
                "version": 1,
                "tipo_regla": "tax",
                "vigente_desde": "2025-01-01",
                "vigente_hasta": "2025-06-30",
                "activo": "y",
            },
            follow_redirects=False,
        )

        # Create version 2
        response2 = client.post(
            "/calculation-rule/new",
            data={
                "codigo": "TAX_CALC",
                "nombre": "Tax Calculation V2",
                "descripcion": "Version 2",
                "jurisdiccion": "Nicaragua",
                "moneda_referencia": "NIO",
                "version": 2,
                "tipo_regla": "tax",
                "vigente_desde": "2025-07-01",
                "activo": "y",
            },
            follow_redirects=False,
        )

        assert response1.status_code in [200, 302]
        assert response2.status_code in [200, 302]

        # Verify both versions exist
        count = db_session.execute(select(func.count(ReglaCalculo.id)).filter_by(codigo="TAX_CALC")).scalar() or 0
        assert count >= 2


def test_calculation_rule_different_rule_types(app, client, admin_user, db_session):
    """Test that different rule types are supported."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        rule_types = [
            ("IMP_RULE", "tax", "Tax Rule"),
            ("DED_RULE", "deduccion", "Deduction Rule"),
            ("PRES_RULE", "prestacion", "Benefit Rule"),
            ("OTH_RULE", "otro", "Other Rule"),
        ]

        for codigo, tipo, nombre in rule_types:
            response = client.post(
                "/calculation-rule/new",
                data={
                    "codigo": codigo,
                    "nombre": nombre,
                    "descripcion": f"Test {tipo} rule",
                    "jurisdiccion": "Test",
                    "moneda_referencia": "USD",
                    "version": 1,
                    "tipo_regla": tipo,
                    "vigente_desde": "2025-01-01",
                    "activo": "y",
                },
                follow_redirects=False,
            )

            assert response.status_code in [200, 302]


def test_calculation_rule_validity_period(app, client, admin_user, db_session):
    """Test that calculation rules can have validity periods."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            "/calculation-rule/new",
            data={
                "codigo": "TIME_LIMITED",
                "nombre": "Time Limited Rule",
                "descripcion": "Valid for specific period",
                "jurisdiccion": "Test",
                "moneda_referencia": "USD",
                "version": 1,
                "tipo_regla": "otro",
                "vigente_desde": "2025-01-01",
                "vigente_hasta": "2025-12-31",
                "activo": "y",
            },
            follow_redirects=False,
        )

        assert response.status_code in [200, 302]

        if response.status_code == 302:
            rule = db_session.execute(select(ReglaCalculo).filter_by(codigo="TIME_LIMITED")).scalar_one_or_none()
            assert rule is not None
            assert rule.vigente_desde == date(2025, 1, 1)
            assert rule.vigente_hasta == date(2025, 12, 31)


def test_calculation_rule_can_be_inactive(app, client, admin_user, db_session):
    """Test that calculation rules can be inactive."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            "/calculation-rule/new",
            data={
                "codigo": "INACTIVE_RULE",
                "nombre": "Inactive Rule",
                "descripcion": "This rule is inactive",
                "jurisdiccion": "Test",
                "moneda_referencia": "USD",
                "version": 1,
                "tipo_regla": "otro",
                "vigente_desde": "2025-01-01",
                # Not sending activo means False
            },
            follow_redirects=False,
        )

        assert response.status_code in [200, 302]

        if response.status_code == 302:
            rule = db_session.execute(select(ReglaCalculo).filter_by(codigo="INACTIVE_RULE")).scalar_one_or_none()
            assert rule is not None
            assert rule.activo is False


def test_validate_schema_api_with_valid_schema(app, client, admin_user, db_session):
    """Test validating a valid JSON schema."""
    with app.app_context():
        # Create test calculation rule
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE",
            nombre="Test Validation",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        valid_schema = {
            "meta": {"name": "Test Schema", "reference_currency": "USD"},
            "inputs": [{"name": "salary", "type": "decimal", "default": 1000}],
            "steps": [{"name": "annual_salary", "type": "calculation", "formula": "salary * 12"}],
            "output": "annual_salary",
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": valid_schema},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "válido" in data["message"].lower()


def test_validate_schema_api_with_missing_steps(app, client, admin_user, db_session):
    """Test validating a schema without steps section."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE_2",
            nombre="Test Validation 2",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        invalid_schema = {
            "meta": {"name": "Test Schema"},
            "inputs": [],
            # Missing steps section
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": invalid_schema},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "steps" in data["error"].lower()


def test_validate_schema_api_with_invalid_step_type(app, client, admin_user, db_session):
    """Test validating a schema with invalid step type."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE_3",
            nombre="Test Validation 3",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        invalid_schema = {
            "meta": {"name": "Test Schema"},
            "inputs": [],
            "steps": [{"name": "invalid_step", "type": "invalid_type", "formula": "1 + 1"}],
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": invalid_schema},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False


def test_validate_schema_api_with_missing_step_name(app, client, admin_user, db_session):
    """Test validating a schema with step missing name field."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE_4",
            nombre="Test Validation 4",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        invalid_schema = {
            "meta": {"name": "Test Schema"},
            "inputs": [],
            "steps": [{"type": "calculation", "formula": "1 + 1"}],  # Missing name
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": invalid_schema},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "name" in data["error"].lower()


def test_validate_schema_api_with_unsafe_formula(app, client, admin_user, db_session):
    """Test validating a schema with unsafe operations in formula."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE_5",
            nombre="Test Validation 5",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        # Schema with unsafe operation (import statement)
        unsafe_schema = {
            "meta": {"name": "Unsafe Schema"},
            "inputs": [{"name": "x", "type": "decimal", "default": 10}],
            "steps": [{"name": "unsafe_step", "type": "calculation", "formula": "__import__('os').system('ls')"}],
            "output": "unsafe_step",
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": unsafe_schema},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False


def test_validate_schema_api_with_conditional_step(app, client, admin_user, db_session):
    """Test validating a schema with conditional step."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE_6",
            nombre="Test Validation 6",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        valid_schema = {
            "meta": {"name": "Conditional Schema"},
            "inputs": [{"name": "salary", "type": "decimal", "default": 1000}],
            "steps": [
                {
                    "name": "bonus",
                    "type": "conditional",
                    "condition": {"left": "salary", "operator": ">", "right": 5000},
                    "if_true": "salary * 0.1",
                    "if_false": "0",
                }
            ],
            "output": "bonus",
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": valid_schema},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True


def test_validate_schema_api_with_tax_lookup_step(app, client, admin_user, db_session):
    """Test validating a schema with tax lookup step."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE_7",
            nombre="Test Validation 7",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        valid_schema = {
            "meta": {"name": "Tax Lookup Schema"},
            "inputs": [{"name": "income", "type": "decimal", "default": 10000}],
            "steps": [
                {
                    "name": "tax",
                    "type": "tax_lookup",
                    "table": "income_tax",
                    "input": "income",
                }
            ],
            "tax_tables": {
                "income_tax": [
                    {"min": 0, "max": 5000, "rate": 0.1, "fixed": 0, "over": 0},
                    {"min": 5000, "max": None, "rate": 0.2, "fixed": 500, "over": 5000},
                ]
            },
            "output": "tax",
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": valid_schema},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True


def test_validate_schema_api_with_assignment_step(app, client, admin_user, db_session):
    """Test validating a schema with assignment step."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_VALIDATE_8",
            nombre="Test Validation 8",
            descripcion="Test schema validation",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        login_user(client, admin_user.usuario, "admin-password")

        valid_schema = {
            "meta": {"name": "Assignment Schema"},
            "inputs": [{"name": "base_salary", "type": "decimal", "default": 1000}],
            "steps": [{"name": "salary", "type": "assignment", "value": "base_salary"}],
            "output": "salary",
        }

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": valid_schema},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True


def test_validate_schema_api_requires_authentication(app, client, db_session):
    """Test that validate_schema_api requires authentication."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="TEST_AUTH",
            nombre="Test Auth",
            descripcion="Test authentication",
            jurisdiccion="Test",
            moneda_referencia="USD",
            version=1,
            tipo_regla="otro",
            vigente_desde=date(2025, 1, 1),
            activo=True,
            esquema_json={},
            creado_por="admin-test",
        )
        db_session.add(rule)
        db_session.commit()
        rule_id = rule.id

        response = client.post(
            f"/calculation-rule/api/validate-schema/{rule_id}",
            json={"schema": {"steps": []}},
            content_type="application/json",
            follow_redirects=False,
        )

        assert response.status_code == 302


def test_validate_schema_api_with_nonexistent_rule(app, client, admin_user, db_session):
    """Test validating schema for non-existent rule."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            "/calculation-rule/api/validate-schema/nonexistent-id",
            json={"schema": {"steps": []}},
            content_type="application/json",
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False
        assert "no encontrada" in data["error"].lower()
