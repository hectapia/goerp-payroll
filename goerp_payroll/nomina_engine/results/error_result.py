# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Error result DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ErrorResult:
    """Represents an error that occurred during processing."""

    message: str
    code: Optional[str] = None
    details: Optional[dict] = None
