# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.

from __future__ import annotations

from datetime import date

import pytest

from goerp_payroll.formula_engine import EXAMPLE_IR_NICARAGUA_SCHEMA
from goerp_payroll.model import ReglaCalculo
from tests.helpers.auth import login_user


@pytest.mark.validation
def test_calculation_rule_create_and_save_schema(app, client, admin_user, db_session):
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        resp = client.post(
            "/calculation-rule/new",
            data={
                "codigo": "IR_VAL",
                "nombre": "IR Validation",
                "descripcion": "Test rule",
                "jurisdiccion": "Nicaragua",
                "moneda_referencia": "NIO",
                "version": "1.0.0",
                "tipo_regla": "tax",
                "vigente_desde": date.today().isoformat(),
                "activo": "y",
                "submit": "Guardar",
            },
            follow_redirects=False,
        )

        assert resp.status_code == 302

        rule = db_session.query(ReglaCalculo).filter(ReglaCalculo.codigo == "IR_VAL").one_or_none()
        assert rule is not None

        # Save schema via API
        resp = client.post(f"/calculation-rule/api/save-schema/{rule.id}", json={"schema": EXAMPLE_IR_NICARAGUA_SCHEMA})
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload is not None
        assert payload.get("success") is True

        # Test schema execution endpoint
        resp = client.post(
            f"/calculation-rule/api/test-schema/{rule.id}",
            json={"schema": EXAMPLE_IR_NICARAGUA_SCHEMA, "inputs": {}},
        )
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload is not None
        assert payload.get("success") is True


@pytest.mark.validation
def test_calculation_rule_delete(app, client, admin_user, db_session):
    with app.app_context():
        rule = ReglaCalculo(
            codigo="DEL_VAL",
            nombre="Delete Validation",
            version="1.0.0",
            tipo_regla="tax",
            vigente_desde=date.today(),
            activo=True,
            esquema_json={},
            creado_por="test",
        )
        db_session.add(rule)
        db_session.commit()

        login_user(client, admin_user.usuario, "admin-password")

        resp = client.post(f"/calculation-rule/delete/{rule.id}", follow_redirects=False)
        assert resp.status_code == 302

        deleted = db_session.get(ReglaCalculo, rule.id)
        assert deleted is None


@pytest.mark.validation
def test_calculation_rule_edit_schema(app, client, admin_user, db_session):
    """Test the edit_schema GET endpoint."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="EDIT_SCHEMA",
            nombre="Edit Schema Test",
            version="1.0.0",
            tipo_regla="tax",
            vigente_desde=date.today(),
            activo=True,
            esquema_json={"test": "data"},
            creado_por="test",
        )
        db_session.add(rule)
        db_session.commit()

        login_user(client, admin_user.usuario, "admin-password")

        # Test successful GET request to edit_schema
        resp = client.get(f"/calculation-rule/edit-schema/{rule.id}")
        assert resp.status_code == 200
        assert b"Edit Schema Test" in resp.data

        # Test with non-existent rule ID
        resp = client.get("/calculation-rule/edit-schema/nonexistent-id", follow_redirects=False)
        assert resp.status_code == 302
        assert resp.location.endswith("/calculation-rule/")


@pytest.mark.validation
def test_calculation_rule_duplicate(app, client, admin_user, db_session):
    """Test the duplicate POST endpoint."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="DUP_TEST",
            nombre="Duplicate Test",
            descripcion="Test rule for duplication",
            jurisdiccion="Nicaragua",
            moneda_referencia="NIO",
            version="1.0.0",
            tipo_regla="tax",
            vigente_desde=date.today(),
            activo=True,
            esquema_json={"test": "data"},
            creado_por="test",
        )
        db_session.add(rule)
        db_session.commit()

        login_user(client, admin_user.usuario, "admin-password")

        # Test successful duplication
        resp = client.post(f"/calculation-rule/duplicate/{rule.id}", follow_redirects=False)
        assert resp.status_code == 302
        assert "/calculation-rule/edit-schema/" in resp.location

        # Verify the new rule was created with incremented version
        duplicated_rules = db_session.query(ReglaCalculo).filter(ReglaCalculo.codigo == "DUP_TEST").all()
        assert len(duplicated_rules) == 2

        # Find the duplicated rule (not the original)
        duplicated_rule = [r for r in duplicated_rules if r.id != rule.id][0]
        assert duplicated_rule.version == "1.0.1"
        assert duplicated_rule.activo is False  # New version starts inactive
        assert duplicated_rule.nombre == rule.nombre
        assert duplicated_rule.descripcion == rule.descripcion
        assert duplicated_rule.jurisdiccion == rule.jurisdiccion
        assert duplicated_rule.moneda_referencia == rule.moneda_referencia
        assert duplicated_rule.tipo_regla == rule.tipo_regla
        assert duplicated_rule.esquema_json == {"test": "data"}
        assert duplicated_rule.creado_por == admin_user.usuario

        # Test with non-existent rule ID
        resp = client.post("/calculation-rule/duplicate/nonexistent-id", follow_redirects=False)
        assert resp.status_code == 302
        assert resp.location.endswith("/calculation-rule/")


@pytest.mark.validation
def test_calculation_rule_duplicate_invalid_version(app, client, admin_user, db_session):
    """Test the duplicate endpoint with invalid version format."""
    with app.app_context():
        rule = ReglaCalculo(
            codigo="DUP_INVALID",
            nombre="Duplicate Invalid Version",
            descripcion="Test rule with invalid version",
            jurisdiccion="Nicaragua",
            moneda_referencia="NIO",
            version="invalid",
            tipo_regla="tax",
            vigente_desde=date.today(),
            activo=True,
            esquema_json={"test": "data"},
            creado_por="test",
        )
        db_session.add(rule)
        db_session.commit()

        login_user(client, admin_user.usuario, "admin-password")

        # Test duplication with invalid version format
        resp = client.post(f"/calculation-rule/duplicate/{rule.id}", follow_redirects=False)
        assert resp.status_code == 302

        # Verify the new rule was created with appended version
        duplicated_rules = db_session.query(ReglaCalculo).filter(ReglaCalculo.codigo == "DUP_INVALID").all()
        assert len(duplicated_rules) == 2

        # Find the duplicated rule
        duplicated_rule = [r for r in duplicated_rules if r.id != rule.id][0]
        assert duplicated_rule.version == "invalid.1"
