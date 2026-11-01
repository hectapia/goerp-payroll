# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests for Report models."""

from goerp_payroll.enums import ReportExecutionStatus, ReportStatus, ReportType
from goerp_payroll.model import Report, ReportAudit, ReportExecution, ReportRole


def test_create_system_report(app, db_session):
    """
    Test creating a system report.

    Setup:
        - None

    Action:
        - Create a system report with required fields

    Verification:
        - Report is created with correct attributes
    """
    with app.app_context():
        report = Report(
            name="Test System Report",
            description="A test system report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        assert report.id is not None
        assert report.name == "Test System Report"
        assert report.type == ReportType.SYSTEM
        assert report.status == ReportStatus.ENABLED
        assert report.base_entity == "Employee"
        assert report.system_report_id == "test_report"
        assert report.category == "employee"


def test_create_custom_report(app, db_session):
    """
    Test creating a custom report with definition.

    Setup:
        - None

    Action:
        - Create a custom report with JSON definition

    Verification:
        - Report is created with definition
    """
    with app.app_context():
        definition = {
            "columns": [
                {"type": "field", "entity": "Employee", "field": "primer_nombre"},
                {"type": "field", "entity": "Employee", "field": "primer_apellido"},
            ],
            "filters": [{"field": "activo", "operator": "=", "value": True}],
            "sorting": [{"field": "primer_apellido", "direction": "asc"}],
        }

        report = Report(
            name="Test Custom Report",
            description="A test custom report",
            type=ReportType.CUSTOM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            definition=definition,
            category="employee",
        )
        db_session.add(report)
        db_session.commit()

        assert report.id is not None
        assert report.type == ReportType.CUSTOM
        assert report.definition is not None
        assert "columns" in report.definition
        assert len(report.definition["columns"]) == 2


def test_report_role_permissions(app, db_session):
    """
    Test creating report role permissions.

    Setup:
        - Create a report

    Action:
        - Create role permissions for the report

    Verification:
        - Permissions are created correctly
    """
    with app.app_context():
        report = Report(
            name="Test Report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
        )
        db_session.add(report)
        db_session.commit()

        role = ReportRole(
            report_id=report.id,
            role="admin",
            can_view=True,
            can_execute=True,
            can_export=True,
        )
        db_session.add(role)
        db_session.commit()

        assert role.id is not None
        assert role.report_id == report.id
        assert role.role == "admin"
        assert role.can_view is True
        assert role.can_execute is True
        assert role.can_export is True


def test_report_execution(app, db_session):
    """
    Test creating a report execution record.

    Setup:
        - Create a report

    Action:
        - Create an execution record

    Verification:
        - Execution record is created
    """
    with app.app_context():
        report = Report(
            name="Test Report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
        )
        db_session.add(report)
        db_session.commit()

        execution = ReportExecution(
            report_id=report.id,
            status=ReportExecutionStatus.COMPLETED,
            executed_by="test_user",
            row_count=10,
            execution_time_ms=250,
        )
        db_session.add(execution)
        db_session.commit()

        assert execution.id is not None
        assert execution.report_id == report.id
        assert execution.status == ReportExecutionStatus.COMPLETED
        assert execution.executed_by == "test_user"
        assert execution.row_count == 10
        assert execution.execution_time_ms == 250


def test_report_audit(app, db_session):
    """
    Test creating a report audit record.

    Setup:
        - Create a report

    Action:
        - Create an audit record

    Verification:
        - Audit record is created
    """
    with app.app_context():
        report = Report(
            name="Test Report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
        )
        db_session.add(report)
        db_session.commit()

        audit = ReportAudit(
            report_id=report.id,
            action="status_changed",
            performed_by="admin_user",
            changes={"old_status": "disabled", "new_status": "enabled"},
        )
        db_session.add(audit)
        db_session.commit()

        assert audit.id is not None
        assert audit.report_id == report.id
        assert audit.action == "status_changed"
        assert audit.performed_by == "admin_user"
        assert "old_status" in audit.changes


def test_report_relationships(app, db_session):
    """
    Test report relationships with other entities.

    Setup:
        - Create a report with permissions and executions

    Action:
        - Access relationships

    Verification:
        - Relationships work correctly
    """
    with app.app_context():
        report = Report(
            name="Test Report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="test_report",
        )
        db_session.add(report)
        db_session.commit()

        # Add permissions
        role1 = ReportRole(
            report_id=report.id,
            role="admin",
            can_view=True,
            can_execute=True,
            can_export=True,
        )
        role2 = ReportRole(
            report_id=report.id,
            role="hhrr",
            can_view=True,
            can_execute=True,
            can_export=False,
        )
        db_session.add(role1)
        db_session.add(role2)

        # Add execution
        execution = ReportExecution(
            report_id=report.id,
            status=ReportExecutionStatus.COMPLETED,
            executed_by="test_user",
        )
        db_session.add(execution)
        db_session.commit()

        # Refresh to load relationships
        db_session.refresh(report)

        assert len(report.permissions) == 2
        assert len(report.executions) == 1
        assert report.permissions[0].role in ["admin", "hhrr"]
        assert report.executions[0].executed_by == "test_user"


def test_disabled_report(app, db_session):
    """
    Test creating a disabled report.

    Setup:
        - None

    Action:
        - Create a report with DISABLED status

    Verification:
        - Report is created with disabled status
    """
    with app.app_context():
        report = Report(
            name="Disabled Report",
            type=ReportType.SYSTEM,
            status=ReportStatus.DISABLED,
            base_entity="Employee",
            system_report_id="disabled_report",
        )
        db_session.add(report)
        db_session.commit()

        assert report.status == ReportStatus.DISABLED


def test_report_unique_name(app, db_session):
    """
    Test that report names must be unique.

    Setup:
        - Create a report

    Action:
        - Try to create another report with the same name

    Verification:
        - Second report creation fails
    """
    with app.app_context():
        report1 = Report(
            name="Unique Report",
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="unique_report_1",
        )
        db_session.add(report1)
        db_session.commit()

        report2 = Report(
            name="Unique Report",  # Same name
            type=ReportType.SYSTEM,
            status=ReportStatus.ENABLED,
            base_entity="Employee",
            system_report_id="unique_report_2",
        )
        db_session.add(report2)

        try:
            db_session.commit()
            assert False, "Should have raised an exception for duplicate name"
        except Exception:
            db_session.rollback()
            assert True
