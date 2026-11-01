# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.

"""No-op queue driver for test environments.

This driver avoids importing optional dependencies (dramatiq) while
providing a compatible interface.
"""

from __future__ import annotations

import os
from typing import Any, Callable

from goerp_payroll.log import log
from goerp_payroll.queue.driver import QueueDriver


class NoopQueueDriver(QueueDriver):
    """Queue driver that does nothing (used for tests)."""

    def enqueue(self, task_name: str, *args: Any, delay: int | None = None, **kwargs: Any) -> Any:
        allow_noop = os.environ.get("COATI_ALLOW_NOOP_QUEUE", "").lower() in {"1", "true", "yes", "on"}
        strict_noop = os.environ.get("COATI_STRICT_NOOP_QUEUE", "").lower() in {"1", "true", "yes", "on"}
        if not allow_noop:
            log.warning("NoopQueueDriver is active. Tasks will not run unless COATI_ALLOW_NOOP_QUEUE=1 is set.")
            if strict_noop:
                raise RuntimeError("NoopQueueDriver usage blocked without COATI_ALLOW_NOOP_QUEUE=1.")
        return {"task": task_name, "enqueued": False, "noop": True}

    def register_task(
        self,
        func: Callable,
        name: str | None = None,
        max_retries: int = 0,
        min_backoff: int = 0,
        max_backoff: int = 0,
    ) -> Callable:
        return func

    def is_available(self) -> bool:
        return True

    def get_stats(self) -> dict[str, Any]:
        return {"driver": "noop", "available": True}

    def get_task_result(self, task_id: Any) -> dict[str, Any]:
        return {"status": "noop", "task_id": task_id}

    def get_bulk_results(self, task_ids: list[Any]) -> dict[str, Any]:
        return {"total": len(task_ids), "completed": 0, "failed": 0, "pending": len(task_ids), "tasks": {}}
