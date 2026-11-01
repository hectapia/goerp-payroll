# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Comprehensive tests for report management routes (goerp_payroll/vistas/report.py)."""

from goerp_payroll.enums import TipoUsuario
from tests.helpers.auth import login_user


def test_report_index_requires_authentication(app, client, db_session):
    """Test that report index requires authentication."""
    with app.app_context():
        response = client.get("/report/", follow_redirects=False)
        assert response.status_code == 302


def test_report_admin_index_requires_authentication(app, client, db_session):
    """Test that admin report index requires authentication."""
    with app.app_context():
        response = client.get("/report/admin", follow_redirects=False)
        assert response.status_code == 302


def test_report_admin_index_requires_admin_role(app, client, db_session):
    """Test that admin report page requires admin role."""
    with app.app_context():
        from tests.factories.user_factory import create_user

        # Create non-admin user
        hhrr_user = create_user(db_session, "hruser", "password", tipo=TipoUsuario.HHRR)
        login_user(client, hhrr_user.usuario, "password")

        response = client.get("/report/admin", follow_redirects=False)
        # Should not allow access
        assert response.status_code in [302, 403]


def test_report_admin_index_success(app, client, db_session, admin_user):
    """Test that admin user can access admin report index."""
    with app.app_context():
        from goerp_payroll.enums import ReportStatus, ReportType
        from goerp_payroll.model import Report

        # Create a test report
        report = Report(
            name="Test Report",
            description="A test report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Access admin index
        response = client.get("/report/admin")
        assert response.status_code == 200


def test_report_admin_index_with_filters(app, client, db_session, admin_user):
    """Test that admin index supports filtering."""
    with app.app_context():
        from goerp_payroll.enums import ReportStatus, ReportType
        from goerp_payroll.model import Report

        # Create test reports with different attributes
        report1 = Report(
            name="Employee Report",
            description="Employee report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="emp_report",
            category="employee",
        )
        report2 = Report(
            name="Payroll Report",
            description="Payroll report",
            type=ReportType.CUSTOM,
            status=ReportStatus.DISABLED,
            base_entity="Nomina",
            category="payroll",
        )
        db_session.add(report1)
        db_session.add(report2)
        db_session.commit()

        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Test category filter
        response = client.get("/report/admin?category=employee")
        assert response.status_code == 200

        # Test type filter
        response = client.get("/report/admin?type=system")
        assert response.status_code == 200

        # Test status filter
        response = client.get("/report/admin?status=enabled")
        assert response.status_code == 200


def test_report_execute_form_not_found(app, client, db_session, admin_user):
    """Test execute form with non-existent report."""
    with app.app_context():
        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Try to access non-existent report
        response = client.get("/report/nonexistent/execute", follow_redirects=True)
        assert response.status_code == 200


def test_report_execute_form_success(app, client, db_session, admin_user):
    """Test execute form displays correctly."""
    with app.app_context():
        from goerp_payroll.enums import ReportStatus, ReportType, TipoUsuario
        from goerp_payroll.model import Report, ReportRole

        # Create a report
        report = Report(
            name="Test Report",
            description="Test description",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        # Add permissions for admin
        perm = ReportRole(report_id=report.id, role=TipoUsuario.ADMIN, can_view=True, can_execute=True, can_export=True)
        db_session.add(perm)
        db_session.commit()

        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Access execute form
        response = client.get(f"/report/{report.id}/execute")
        assert response.status_code == 200


def test_report_run_not_found(app, client, db_session, admin_user):
    """Test running a non-existent report."""
    with app.app_context():
        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Try to run non-existent report
        response = client.post("/report/nonexistent/run", json={}, follow_redirects=False)
        assert response.status_code == 404


def test_report_export_not_found(app, client, db_session, admin_user):
    """Test exporting a non-existent report."""
    with app.app_context():
        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Try to export non-existent report
        response = client.post("/report/nonexistent/export/csv", json={}, follow_redirects=False)
        assert response.status_code == 404


def test_report_toggle_status_not_found(app, client, db_session, admin_user):
    """Test toggling status of non-existent report."""
    with app.app_context():
        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Try to toggle non-existent report
        response = client.post("/report/nonexistent/toggle-status", follow_redirects=True)
        assert response.status_code == 200


def test_report_toggle_status_success(app, client, db_session, admin_user):
    """Test toggling report status."""
    with app.app_context():
        from goerp_payroll.enums import ReportStatus, ReportType
        from goerp_payroll.model import Report

        # Create a report
        report = Report(
            name="Test Report",
            description="Test description",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        initial_status = report.status

        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Toggle status
        response = client.post(f"/report/{report.id}/toggle-status", follow_redirects=True)
        assert response.status_code == 200

        # Verify status changed
        db_session.refresh(report)
        assert report.status != initial_status


def test_report_permissions_form_not_found(app, client, db_session, admin_user):
    """Test permissions form with non-existent report."""
    with app.app_context():
        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Try to access permissions for non-existent report
        response = client.get("/report/nonexistent/permissions", follow_redirects=True)
        assert response.status_code == 200


def test_report_permissions_form_success(app, client, db_session, admin_user):
    """Test permissions form displays correctly."""
    with app.app_context():
        from goerp_payroll.enums import ReportStatus, ReportType
        from goerp_payroll.model import Report

        # Create a report
        report = Report(
            name="Test Report",
            description="Test description",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Access permissions form
        response = client.get(f"/report/{report.id}/permissions")
        assert response.status_code == 200


def test_report_update_permissions_not_found(app, client, db_session, admin_user):
    """Test updating permissions for non-existent report."""
    with app.app_context():
        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Try to update permissions for non-existent report
        response = client.post("/report/nonexistent/permissions", data={}, follow_redirects=True)
        assert response.status_code == 200


def test_report_update_permissions_success(app, client, db_session, admin_user):
    """Test updating report permissions."""
    with app.app_context():
        from goerp_payroll.enums import ReportStatus, ReportType, TipoUsuario
        from goerp_payroll.model import Report

        # Create a report
        report = Report(
            name="Test Report",
            description="Test description",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Update permissions
        response = client.post(
            f"/report/{report.id}/permissions",
            data={
                f"{TipoUsuario.ADMIN}_can_view": "on",
                f"{TipoUsuario.ADMIN}_can_execute": "on",
                f"{TipoUsuario.ADMIN}_can_export": "on",
                f"{TipoUsuario.HHRR}_can_view": "on",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200


def test_report_detail_not_found(app, client, db_session, admin_user):
    """Test report detail with non-existent report."""
    with app.app_context():
        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Try to access non-existent report detail
        response = client.get("/report/nonexistent", follow_redirects=True)
        assert response.status_code == 200


def test_report_detail_success(app, client, db_session, admin_user):
    """Test report detail displays correctly."""
    with app.app_context():
        from goerp_payroll.enums import ReportStatus, ReportType, TipoUsuario
        from goerp_payroll.model import Report, ReportRole

        # Create a report
        report = Report(
            name="Test Report",
            description="Test description",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        # Add permissions for admin
        perm = ReportRole(report_id=report.id, role=TipoUsuario.ADMIN, can_view=True, can_execute=True, can_export=True)
        db_session.add(perm)
        db_session.commit()

        # Login as admin
        login_user(client, admin_user.usuario, "admin-password")

        # Access report detail
        response = client.get(f"/report/{report.id}")
        assert response.status_code == 200
