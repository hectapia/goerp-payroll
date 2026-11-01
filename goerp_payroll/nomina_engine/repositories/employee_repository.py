# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Repository for Employee operations."""

from __future__ import annotations

from typing import Optional

from goerp_payroll.model import Empleado
from .base_repository import BaseRepository


class EmployeeRepository(BaseRepository[Empleado]):
    """Repository for Employee operations."""

    def get_by_id(self, empleado_id: str) -> Optional[Empleado]:
        """Get employee by ID."""
        return self.session.get(Empleado, empleado_id)

    def save(self, empleado: Empleado) -> Empleado:
        """Save employee."""
        self.session.add(empleado)
        return empleado
