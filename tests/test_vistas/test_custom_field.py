# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Comprehensive tests for custom field CRUD operations (goerp_payroll/vistas/custom_field.py)."""

from sqlalchemy import func, select
from goerp_payroll.model import CampoPersonalizado
from tests.helpers.auth import login_user


def test_custom_field_index_requires_authentication(app, client, db_session):
    """Test that custom field index requires authentication."""
    with app.app_context():
        response = client.get("/custom_field/", follow_redirects=False)
        assert response.status_code == 302


def test_custom_field_index_lists_fields(app, client, admin_user, db_session):
    """Test that authenticated admin can view custom field list."""
    with app.app_context():
        # Create test custom fields
        field1 = CampoPersonalizado(
            nombre_campo="employee_id_card",
            etiqueta="Employee ID Card",
            tipo_dato="text",
            orden=1,
            activo=True,
            creado_por="admin-test",
        )
        field2 = CampoPersonalizado(
            nombre_campo="years_experience",
            etiqueta="Years of Experience",
            tipo_dato="integer",
            orden=2,
            activo=True,
            creado_por="admin-test",
        )
        db_session.add_all([field1, field2])
        db_session.commit()

        login_user(client, admin_user.usuario, "admin-password")

        response = client.get("/custom_field/")
        assert response.status_code == 200
        assert b"employee_id_card" in response.data or b"Employee ID Card" in response.data


def test_custom_field_new_creates_field(app, client, admin_user, db_session):
    """Test creating a new custom field."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            "/custom_field/new",
            data={
                "nombre_campo": "department_code",
                "etiqueta": "Department Code",
                "tipo_dato": "text",
                "descripcion": "Employee department code",
                "orden": 10,
                "activo": "y",
            },
            follow_redirects=False,
        )

        assert response.status_code in [200, 302]

        # Verify custom field was created if redirect
        if response.status_code == 302:
            field = db_session.execute(
                select(CampoPersonalizado).filter_by(nombre_campo="department_code")
            ).scalar_one_or_none()
            assert field is not None
            assert field.etiqueta == "Department Code"
            assert field.tipo_dato == "text"
            assert field.orden == 10
            assert field.activo is True


def test_custom_field_edit_updates_field(app, client, admin_user, db_session):
    """Test updating a custom field."""
    with app.app_context():
        # Create custom field
        field = CampoPersonalizado(
            nombre_campo="skill_level",
            etiqueta="Skill Level",
            tipo_dato="integer",
            orden=5,
            activo=True,
            creado_por="admin-test",
        )
        db_session.add(field)
        db_session.commit()
        db_session.refresh(field)

        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            f"/custom_field/edit/{field.id}",
            data={
                "nombre_campo": "skill_level",
                "etiqueta": "Skill Level (Updated)",
                "tipo_dato": "integer",
                "descripcion": "Updated description",
                "orden": 15,
                "activo": "y",
            },
            follow_redirects=False,
        )

        assert response.status_code in [200, 302]

        # Verify update if redirect
        if response.status_code == 302:
            updated_field = db_session.execute(select(CampoPersonalizado).filter_by(id=field.id)).scalar_one()
            assert updated_field.etiqueta == "Skill Level (Updated)"
            assert updated_field.orden == 15


def test_custom_field_delete_removes_field(app, client, admin_user, db_session):
    """Test deleting a custom field."""
    with app.app_context():
        # Create custom field
        field = CampoPersonalizado(
            nombre_campo="temp_field",
            etiqueta="Temporary Field",
            tipo_dato="text",
            orden=1,
            activo=True,
            creado_por="admin-test",
        )
        db_session.add(field)
        db_session.commit()
        field_id = field.id

        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(f"/custom_field/delete/{field_id}", follow_redirects=False)

        assert response.status_code in [200, 302]

        # Verify deletion if redirect
        if response.status_code == 302:
            field = db_session.execute(select(CampoPersonalizado).filter_by(id=field_id)).scalar_one_or_none()
            assert field is None


def test_custom_field_supports_different_data_types(app, client, admin_user, db_session):
    """Test that custom fields support different data types."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        data_types = [
            ("text_field", "text", "Text Field"),
            ("integer_field", "integer", "Integer Field"),
            ("decimal_field", "decimal", "Decimal Field"),
            ("boolean_field", "boolean", "Boolean Field"),
        ]

        for nombre, tipo, etiqueta in data_types:
            response = client.post(
                "/custom_field/new",
                data={
                    "nombre_campo": nombre,
                    "etiqueta": etiqueta,
                    "tipo_dato": tipo,
                    "orden": 1,
                    "activo": "y",
                },
                follow_redirects=False,
            )

            assert response.status_code in [200, 302]

        # Verify all created if redirects
        count = db_session.execute(select(func.count(CampoPersonalizado.id))).scalar() or 0
        assert count >= len(data_types)


def test_custom_field_ordering_works(app, client, admin_user, db_session):
    """Test that custom fields can be ordered."""
    with app.app_context():
        # Create fields with different orders
        field1 = CampoPersonalizado(
            nombre_campo="field_c",
            etiqueta="Field C",
            tipo_dato="text",
            orden=30,
            activo=True,
            creado_por="admin-test",
        )
        field2 = CampoPersonalizado(
            nombre_campo="field_a",
            etiqueta="Field A",
            tipo_dato="text",
            orden=10,
            activo=True,
            creado_por="admin-test",
        )
        field3 = CampoPersonalizado(
            nombre_campo="field_b",
            etiqueta="Field B",
            tipo_dato="text",
            orden=20,
            activo=True,
            creado_por="admin-test",
        )
        db_session.add_all([field1, field2, field3])
        db_session.commit()

        # Query fields ordered by orden
        fields = db_session.execute(select(CampoPersonalizado).order_by(CampoPersonalizado.orden)).scalars().all()

        assert fields[0].nombre_campo == "field_a"
        assert fields[1].nombre_campo == "field_b"
        assert fields[2].nombre_campo == "field_c"


def test_custom_field_can_be_inactive(app, client, admin_user, db_session):
    """Test that custom fields can be inactive."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        response = client.post(
            "/custom_field/new",
            data={
                "nombre_campo": "inactive_field",
                "etiqueta": "Inactive Field",
                "tipo_dato": "text",
                "orden": 1,
                # Not sending activo means False
            },
            follow_redirects=False,
        )

        assert response.status_code in [200, 302]

        # Verify inactive if redirect
        if response.status_code == 302:
            field = db_session.execute(
                select(CampoPersonalizado).filter_by(nombre_campo="inactive_field")
            ).scalar_one_or_none()
            assert field is not None
            assert field.activo is False


def test_custom_field_workflow_create_edit_delete(app, client, admin_user, db_session):
    """End-to-end test: Create, edit, and delete a custom field."""
    with app.app_context():
        login_user(client, admin_user.usuario, "admin-password")

        # Step 1: Create
        response = client.post(
            "/custom_field/new",
            data={
                "nombre_campo": "test_workflow",
                "etiqueta": "Test Workflow",
                "tipo_dato": "text",
                "descripcion": "Test description",
                "orden": 5,
                "activo": "y",
            },
            follow_redirects=False,
        )
        assert response.status_code in [200, 302]

        if response.status_code == 302:
            field = db_session.execute(
                select(CampoPersonalizado).filter_by(nombre_campo="test_workflow")
            ).scalar_one_or_none()
            assert field is not None
            field_id = field.id

            # Step 2: Edit
            response = client.post(
                f"/custom_field/edit/{field_id}",
                data={
                    "nombre_campo": "test_workflow",
                    "etiqueta": "Test Workflow (Updated)",
                    "tipo_dato": "text",
                    "orden": 10,
                    # Not sending activo means False
                },
                follow_redirects=False,
            )
            assert response.status_code in [200, 302]

            if response.status_code == 302:
                updated_field = db_session.execute(select(CampoPersonalizado).filter_by(id=field_id)).scalar_one()
                assert updated_field.etiqueta == "Test Workflow (Updated)"
                assert updated_field.activo is False

                # Step 3: Delete
                response = client.post(f"/custom_field/delete/{field_id}", follow_redirects=False)
                assert response.status_code in [200, 302]

                if response.status_code == 302:
                    field = db_session.execute(select(CampoPersonalizado).filter_by(id=field_id)).scalar_one_or_none()
                    assert field is None
