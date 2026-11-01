# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Warning collector for payroll execution."""

from __future__ import annotations

from typing import Protocol


class WarningCollectorProtocol(Protocol):
    """Protocol for objects that collect warnings."""

    def append(self, warning: str) -> None:
        """Append a warning message."""
        ...

    def extend(self, warnings: list[str]) -> None:
        """Extend with multiple warning messages."""
        ...


class WarningCollector:
    """Centralized warning collector to avoid mutable list sharing."""

    def __init__(self) -> None:
        self._warnings: list[str] = []

    def append(self, warning: str) -> None:
        self._warnings.append(warning)

    def extend(self, warnings: list[str]) -> None:
        self._warnings.extend(warnings)

    def __iter__(self):
        return iter(self._warnings)

    def __len__(self) -> int:
        return len(self._warnings)

    def __bool__(self) -> bool:
        return len(self._warnings) > 0

    def to_list(self) -> list[str]:
        return list(self._warnings)
