# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Role-Based Access Control (RBAC) utilities.

This module provides decorators and utilities for implementing role-based
access control throughout the application.

User Types:
    - admin: Full access to all functionalities
    - hr: HR personnel with access to employee and payroll management
    - audit: Read-only access for auditing purposes
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from functools import wraps
from typing import TypeAlias

# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #
from flask import abort, flash, redirect, url_for
from flask_login import current_user

# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #
from goerp_payroll.enums import TipoUsuario
from goerp_payroll.i18n import _

Role: TypeAlias = TipoUsuario | str

# ----------------------[ GLOBAL VARIABLES DEFINITION ]---------------------- #
MESSAGE_LOGIN_REQUIRED = "Favor iniciar sesión para acceder al sistema."
ROUTE_AUTH_LOGIN = "auth.login"


def require_role(*allowed_roles: Role):
    """Decorator to restrict access to specific user roles.

    Args:
        *allowed_roles: Variable number of allowed role strings (admin, hr, audit)

    Returns:
        Decorated function that checks user role before execution

    Example:
        @require_role(TipoUsuario.ADMIN)
        def admin_only_view():
            pass

        @require_role(TipoUsuario.ADMIN, TipoUsuario.HHRR)
        def admin_or_hr_view():
            pass
    """
    normalized_roles = tuple(normalize_role(role) for role in allowed_roles)

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(_(MESSAGE_LOGIN_REQUIRED), "warning")
                return redirect(url_for(ROUTE_AUTH_LOGIN))

            # Check if user has required role
            if current_user.tipo not in normalized_roles:
                flash(_("No tiene permisos para acceder a esta funcionalidad."), "danger")
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def normalize_role(role: Role) -> str:
    """Normalize and validate role values to canonical strings."""
    if isinstance(role, TipoUsuario):
        return role.value
    if isinstance(role, str):
        normalized = role.strip().lower()
        allowed_values = {allowed_role.value for allowed_role in TipoUsuario}
        if normalized in allowed_values:
            return normalized
    raise ValueError(f"Invalid role: {role}")


def require_read_access():
    """Decorator to allow read access to admin, hhrr, and audit users.

    This is used for listing and viewing data where all user types should
    have access but audit users are read-only.

    Returns:
        Decorated function that allows read access to all authenticated users

    Example:
        @require_read_access()
        def list_employees():
            pass
    """

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(_(MESSAGE_LOGIN_REQUIRED), "warning")
                return redirect(url_for(ROUTE_AUTH_LOGIN))

            # All authenticated users can read
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_write_access():
    """Decorator to restrict write operations to admin and hhrr users only.

    Audit users are denied access to create, update, or delete operations.

    Returns:
        Decorated function that checks write permissions

    Example:
        @require_write_access()
        def create_employee():
            pass

        @require_write_access()
        def update_employee():
            pass
    """

    return require_role(TipoUsuario.ADMIN, TipoUsuario.HHRR)


def is_admin() -> bool:
    """Check if current user is an administrator.

    Returns:
        True if current user has admin role, False otherwise
    """
    return current_user.is_authenticated and current_user.tipo == TipoUsuario.ADMIN.value


def is_hhrr() -> bool:
    """Check if current user is HR personnel.

    Returns:
        True if current user has hhrr role, False otherwise
    """
    return current_user.is_authenticated and current_user.tipo == TipoUsuario.HHRR.value


def is_audit() -> bool:
    """Check if current user is an auditor.

    Returns:
        True if current user has audit role, False otherwise
    """
    return current_user.is_authenticated and current_user.tipo == TipoUsuario.AUDIT.value


def can_write() -> bool:
    """Check if current user has write permissions.

    Returns:
        True if current user is admin or hhrr, False otherwise
    """
    return current_user.is_authenticated and current_user.tipo in [TipoUsuario.ADMIN.value, TipoUsuario.HHRR.value]
