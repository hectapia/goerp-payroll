# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Abstract base class for queue drivers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable


class QueueDriver(ABC):
    """Abstract base class for queue drivers.

    All queue implementations (currently Dramatiq) must implement this interface
    to provide a consistent API for background job processing.
    """

    @abstractmethod
    def enqueue(self, task_name: str, *args: Any, delay: int | None = None, **kwargs: Any) -> Any:
        """Enqueue a task for background processing.

        Args:
            task_name: Name of the task function to execute
            *args: Positional arguments to pass to the task
            delay: Optional delay in seconds before task execution
            **kwargs: Keyword arguments to pass to the task

        Returns:
            Task identifier or result promise (implementation-specific)

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    def register_task(
        self,
        func: Callable,
        name: str | None = None,
        max_retries: int = 3,
        min_backoff: int = 15000,
        max_backoff: int = 86400000,
    ) -> Callable:
        """Register a function as a background task.

        Args:
            func: Function to register as a task
            name: Optional name for the task (defaults to function name)
            max_retries: Maximum number of retry attempts
            min_backoff: Minimum backoff time in milliseconds
            max_backoff: Maximum backoff time in milliseconds

        Returns:
            Decorated function that can be called normally or enqueued

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this queue driver is available and ready to use.

        Returns:
            True if driver is available, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def get_stats(self) -> dict[str, Any]:
        """Get queue statistics.

        Returns:
            Dictionary with queue statistics (pending, processing, completed, etc.)
        """
        raise NotImplementedError

    @abstractmethod
    def get_task_result(self, task_id: Any) -> dict[str, Any]:
        """Get the result of a task by its ID.

        Args:
            task_id: Task identifier returned by enqueue()

        Returns:
            Dictionary with task status and result:
            {
                "status": "pending" | "processing" | "completed" | "failed",
                "result": Any (if completed),
                "error": str (if failed),
                "progress": dict (if driver supports it)
            }
        """
        raise NotImplementedError

    @abstractmethod
    def get_bulk_results(self, task_ids: list[Any]) -> dict[str, Any]:
        """Get results for multiple tasks (for bulk feedback: x of y completed).

        Args:
            task_ids: List of task identifiers

        Returns:
            Dictionary with aggregated status:
            {
                "total": int,
                "completed": int,
                "failed": int,
                "pending": int,
                "processing": int,
                "tasks": dict[task_id, status]
            }
        """
        raise NotImplementedError
