# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Queue module for background job processing.

This module provides a unified interface for background job processing
with automatic backend selection:
- Dramatiq + Redis (production/high-scale deployments)

Usage:
    from goerp_payroll.queue import get_queue_driver

    queue = get_queue_driver()
    queue.enqueue('calculate_employee_payroll', employee_id=123, payroll_id=456)
"""

from __future__ import annotations

from goerp_payroll.queue.driver import QueueDriver
from goerp_payroll.queue.selector import get_queue_driver

__all__ = ["QueueDriver", "get_queue_driver"]
