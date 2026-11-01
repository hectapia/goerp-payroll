# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Processors for specialized payroll operations."""

from .loan_processor import LoanProcessor
from .accumulation_processor import AccumulationProcessor
from .vacation_processor import VacationProcessor
from .novelty_processor import NoveltyProcessor
from .accounting_processor import AccountingProcessor

__all__ = [
    "LoanProcessor",
    "AccumulationProcessor",
    "VacationProcessor",
    "NoveltyProcessor",
    "AccountingProcessor",
]
