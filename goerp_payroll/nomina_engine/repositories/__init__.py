# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Repository layer for data access."""

from .base_repository import BaseRepository
from .planilla_repository import PlanillaRepository
from .employee_repository import EmployeeRepository
from .acumulado_repository import AcumuladoRepository
from .novelty_repository import NoveltyRepository
from .exchange_rate_repository import ExchangeRateRepository
from .config_repository import ConfigRepository

__all__ = [
    "BaseRepository",
    "PlanillaRepository",
    "EmployeeRepository",
    "AcumuladoRepository",
    "NoveltyRepository",
    "ExchangeRateRepository",
    "ConfigRepository",
]
