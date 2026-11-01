# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Factory functions for creating test data."""

from tests.factories.company_factory import create_company
from tests.factories.employee_factory import create_employee
from tests.factories.user_factory import create_user

__all__ = [
    "create_user",
    "create_employee",
    "create_company",
]
