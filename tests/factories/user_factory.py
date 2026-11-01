# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Factory functions for creating users."""

from goerp_payroll.auth import proteger_passwd
from goerp_payroll.model import Usuario


def create_user(
    db_session, usuario, password, nombre="Test", apellido="User", correo_electronico=None, tipo="admin", activo=True
):
    """
    Create a user in the database.

    This is a simple factory function that creates a user with the given
    parameters. No implicit data creation or side effects.

    Args:
        db_session: SQLAlchemy session
        usuario: Username (unique identifier)
        password: Plain text password (will be hashed)
        nombre: First name (default: "Test")
        apellido: Last name (default: "User")
        correo_electronico: Email address (optional)
        tipo: User type (default: "admin")
        activo: Active status (default: True)

    Returns:
        Usuario: Created user instance with ID assigned
    """
    user = Usuario()
    user.usuario = usuario
    user.acceso = proteger_passwd(password)
    user.nombre = nombre
    user.apellido = apellido
    user.correo_electronico = correo_electronico
    user.tipo = tipo
    user.activo = activo

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user
