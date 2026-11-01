# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Utilities for resolving absence-related novelty defaults."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def resolve_explicit_flag_from_form(
    form: Any,
    field_name: str,
    *,
    has_request_context: bool,
    request_form: Mapping[str, Any] | None,
) -> bool | None:
    """Extract explicit boolean value from a form field if explicitly sent.

    Returns None when a request context exists but the field key is absent from
    payload, allowing callers to apply concept-level defaults.
    """
    if not hasattr(form, field_name):
        return None

    if has_request_context and (request_form is None or field_name not in request_form):
        return None

    return bool(getattr(form, field_name).data)


def resolve_absence_flags_from_concept(
    concept: Any | None,
    *,
    explicit_es_inasistencia: bool | None = None,
    explicit_descontar_pago_inasistencia: bool | None = None,
) -> tuple[bool, bool]:
    """Resolve final absence flags using concept defaults and explicit values."""
    default_es_inasistencia = bool(getattr(concept, "es_inasistencia", False))
    default_descontar_pago = bool(getattr(concept, "descontar_pago_inasistencia", False))

    es_inasistencia = default_es_inasistencia if explicit_es_inasistencia is None else explicit_es_inasistencia
    descontar_pago_inasistencia = (
        default_descontar_pago if explicit_descontar_pago_inasistencia is None else explicit_descontar_pago_inasistencia
    )

    return es_inasistencia, descontar_pago_inasistencia


def resolve_absence_flags(
    *,
    percepcion_id: str | None,
    deduccion_id: str | None,
    get_percepcion: Callable[[str], Any | None],
    get_deduccion: Callable[[str], Any | None],
    explicit_es_inasistencia: bool | None = None,
    explicit_descontar_pago_inasistencia: bool | None = None,
) -> tuple[bool, bool]:
    """Resolve absence flags using concept lookup callbacks."""
    concept = None
    if percepcion_id:
        concept = get_percepcion(percepcion_id)
    elif deduccion_id:
        concept = get_deduccion(deduccion_id)

    return resolve_absence_flags_from_concept(
        concept,
        explicit_es_inasistencia=explicit_es_inasistencia,
        explicit_descontar_pago_inasistencia=explicit_descontar_pago_inasistencia,
    )
