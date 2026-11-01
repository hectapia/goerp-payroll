# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Repository for Planilla operations."""

from __future__ import annotations

from typing import Any, Optional, cast
from sqlalchemy.orm import joinedload

from goerp_payroll.model import Planilla, PlanillaEmpleado, PlanillaIngreso, PlanillaDeduccion, PlanillaPrestacion
from .base_repository import BaseRepository


class PlanillaRepository(BaseRepository[Planilla]):
    """Repository for Planilla operations."""

    def get_by_id(self, planilla_id: str) -> Optional[Planilla]:
        """Get planilla with all necessary relationships loaded."""
        from sqlalchemy import select

        return (
            self.session.execute(
                select(Planilla)
                .options(
                    joinedload(cast(Any, Planilla.tipo_planilla)),
                    joinedload(cast(Any, Planilla.moneda)),
                    joinedload(cast(Any, Planilla.planilla_empleados)).joinedload(cast(Any, PlanillaEmpleado.empleado)),
                    joinedload(cast(Any, Planilla.planilla_percepciones)).joinedload(
                        cast(Any, PlanillaIngreso.percepcion)
                    ),
                    joinedload(cast(Any, Planilla.planilla_deducciones)).joinedload(
                        cast(Any, PlanillaDeduccion.deduccion)
                    ),
                    joinedload(cast(Any, Planilla.planilla_prestaciones)).joinedload(
                        cast(Any, PlanillaPrestacion.prestacion)
                    ),
                )
                .filter(Planilla.id == planilla_id)
            )
            .unique()
            .scalar_one_or_none()
        )

    def save(self, planilla: Planilla) -> Planilla:
        """Save planilla."""
        self.session.add(planilla)
        return planilla
