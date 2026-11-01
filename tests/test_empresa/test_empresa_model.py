# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for Empresa (Company) model."""

from sqlalchemy import func, select
import pytest
from sqlalchemy.exc import IntegrityError

from goerp_payroll.model import Empresa
from tests.factories.company_factory import create_company


def test_create_empresa_with_factory(app, db_session):
    """
    Test creating a company using factory.

    Setup:
        - Clean database

    Action:
        - Create empresa with factory

    Verification:
        - Empresa exists with correct attributes
    """
    with app.app_context():
        empresa = create_company(db_session, codigo="EMP001", razon_social="Test Company S.A.", ruc="J0123456789")

        assert empresa.id is not None
        assert empresa.codigo == "EMP001"
        assert empresa.razon_social == "Test Company S.A."
        assert empresa.ruc == "J0123456789"
        assert empresa.activo is True


def test_empresa_unique_codigo(app, db_session):
    """
    Test that empresa codigo must be unique.

    Setup:
        - Create first empresa

    Action:
        - Try to create second empresa with same codigo

    Verification:
        - IntegrityError is raised
    """
    with app.app_context():
        create_company(db_session, codigo="EMP_UNIQUE_1", razon_social="Company 1", ruc="J0123456780")

        with pytest.raises(IntegrityError):
            create_company(db_session, codigo="EMP_UNIQUE_1", razon_social="Company 2", ruc="J9876543210")


def test_empresa_unique_ruc(app, db_session):
    """
    Test that empresa RUC must be unique.

    Setup:
        - Create first empresa

    Action:
        - Try to create second empresa with same RUC

    Verification:
        - IntegrityError is raised
    """
    with app.app_context():
        create_company(db_session, codigo="EMP_RUC_1", razon_social="Company 1", ruc="J0123456781")

        with pytest.raises(IntegrityError):
            create_company(db_session, codigo="EMP_RUC_2", razon_social="Company 2", ruc="J0123456781")


def test_empresa_with_optional_fields(app, db_session):
    """
    Test creating empresa with optional fields.

    Setup:
        - Clean database

    Action:
        - Create empresa with all optional fields

    Verification:
        - All fields are stored correctly
    """
    with app.app_context():
        empresa = create_company(
            db_session,
            codigo="EMP002",
            razon_social="Full Company S.A.",
            ruc="J0123456782",
            nombre_comercial="Full Co.",
            direccion="123 Main St",
            telefono="555-1234",
            correo="info@fullco.com",
        )

        assert empresa.nombre_comercial == "Full Co."
        assert empresa.direccion == "123 Main St"
        assert empresa.telefono == "555-1234"
        assert empresa.correo == "info@fullco.com"


def test_multiple_empresas_can_be_created(app, db_session):
    """
    Test creating multiple companies.

    Setup:
        - Clean database

    Action:
        - Create multiple empresas

    Verification:
        - All exist with unique IDs
    """
    with app.app_context():
        empresa1 = create_company(db_session, "EMP_MULTI_1", "Company 1", "J0001")
        empresa2 = create_company(db_session, "EMP_MULTI_2", "Company 2", "J0002")
        empresa3 = create_company(db_session, "EMP_MULTI_3", "Company 3", "J0003")

        assert empresa1.id != empresa2.id
        assert empresa2.id != empresa3.id
        assert empresa1.id != empresa3.id

        # Verify all exist in database
        count = db_session.execute(select(func.count(Empresa.id))).scalar() or 0
        assert count == 3


def test_empresa_can_be_inactive(app, db_session):
    """
    Test creating inactive empresa.

    Setup:
        - Clean database

    Action:
        - Create empresa with activo=False

    Verification:
        - Empresa is inactive
    """
    with app.app_context():
        empresa = create_company(
            db_session, codigo="EMP_INACTIVE", razon_social="Inactive Company", ruc="J9999999999", activo=False
        )

        assert empresa.activo is False
