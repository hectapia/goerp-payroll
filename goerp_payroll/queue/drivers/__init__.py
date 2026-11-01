# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Queue driver implementations."""

from __future__ import annotations

from goerp_payroll.queue.drivers.dramatiq_driver import DramatiqDriver
from goerp_payroll.queue.drivers.noop_driver import NoopQueueDriver

__all__ = ["DramatiqDriver", "NoopQueueDriver"]
