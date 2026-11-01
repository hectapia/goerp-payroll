# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Business logic validators for planilla operations."""

from goerp_payroll.model import Planilla, Empleado
from goerp_payroll.i18n import _


class PlanillaValidator:
    """Validators for planilla business logic."""

    @staticmethod
    def validar_empresa_empleado(planilla: Planilla, empleado: Empleado) -> tuple[bool, str | None]:
        """Validate that planilla and employee belong to the same company.

        Args:
            planilla: The planilla to validate
            empleado: The employee to validate

        Returns:
            Tuple of (is_valid, error_message). If valid, error_message is None.
        """
        if not planilla.empresa_id:
            return False, _("La planilla debe tener una empresa asignada antes de agregar empleados.")
        if not empleado.empresa_id:
            return False, _("El empleado debe tener una empresa asignada antes de ser agregado a una planilla.")
        if planilla.empresa_id != empleado.empresa_id:
            return False, _("El empleado y la planilla deben pertenecer a la misma empresa.")
        return True, None
