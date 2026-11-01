# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Base repository for data access."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Base repository for data access operations."""

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_by_id(self, id_: str) -> Optional[T]:
        """Get entity by ID."""

    @abstractmethod
    def save(self, entity: T) -> T:
        """Save entity."""
