# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Plugin Manager."""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from dataclasses import dataclass
from importlib import import_module
from importlib.metadata import distributions
from typing import Mapping, cast

# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #
from flask import Flask

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from goerp_payroll.log import log
from goerp_payroll.model import PluginRegistry, db

# ----------------------[ GLOBAL VARIABLES DEFINITION ]---------------------- #
PLUGIN_DISTRIBUTION_PREFIX = "goerp-payroll-plugin-"


@dataclass(frozen=True)
class DiscoveredPlugin:
    distribution_name: str
    plugin_id: str
    version: str | None


def _distribution_to_plugin_id(distribution_name: str) -> str:
    if not distribution_name.startswith(PLUGIN_DISTRIBUTION_PREFIX):
        return distribution_name
    return distribution_name[len(PLUGIN_DISTRIBUTION_PREFIX) :]


def _plugin_id_to_module_name(plugin_id: str) -> str:
    return f"goerp_payroll_plugin_{plugin_id.replace('-', '_')}"


def discover_installed_plugins() -> list[DiscoveredPlugin]:
    found: list[DiscoveredPlugin] = []

    for dist in distributions():
        metadata = cast(Mapping[str, str], dist.metadata)
        name = (metadata.get("Name") or "").strip()
        if not name or not name.startswith(PLUGIN_DISTRIBUTION_PREFIX):
            continue

        plugin_id = _distribution_to_plugin_id(name)
        version = (dist.version or "").strip() or None
        found.append(DiscoveredPlugin(distribution_name=name, plugin_id=plugin_id, version=version))

    found.sort(key=lambda p: p.distribution_name)
    return found


def sync_plugin_registry() -> None:
    """Sync the plugin registry with installed plugins.

    This function queries the database to sync installed plugins.
    If the database tables don't exist yet, it will raise an OperationalError.
    This is expected behavior during initial setup - the application should
    ensure the database is initialized before calling this function, or
    handle the OperationalError gracefully.
    """
    from sqlalchemy.exc import OperationalError, ProgrammingError

    installed = {p.distribution_name: p for p in discover_installed_plugins()}

    try:
        rows = db.session.execute(db.select(PluginRegistry)).scalars().all()
    except (OperationalError, ProgrammingError) as exc:
        # Database tables don't exist yet - this is expected during initial setup
        # or in test environments. Re-raise the error so the caller can handle it.
        raise OperationalError(
            "Cannot sync plugin registry: database tables not initialized. "
            "Please run database initialization first.",
            params=None,
            orig=exc,
        ) from exc

    by_name = {r.distribution_name: r for r in rows}

    changed = False

    for name, plugin in installed.items():
        if name in by_name:
            if by_name[name].plugin_id != plugin.plugin_id:
                by_name[name].plugin_id = plugin.plugin_id
                changed = True
            if by_name[name].version != plugin.version:
                by_name[name].version = plugin.version
                changed = True
            if by_name[name].installed is not True:
                by_name[name].installed = True
                changed = True
            continue

        record = PluginRegistry()
        record.distribution_name = name
        record.plugin_id = plugin.plugin_id
        record.version = plugin.version
        record.active = False
        record.installed = True
        db.session.add(record)
        changed = True

    for name, record in by_name.items():
        if name in installed:
            continue
        if record.installed is not False:
            record.installed = False
            changed = True
        if record.active:
            record.active = False
            changed = True

    if changed:
        db.session.commit()


def _load_plugin_module(distribution_name: str, plugin_id: str):
    module_name = _plugin_id_to_module_name(plugin_id)
    try:
        return import_module(module_name)
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            f"Plugin '{distribution_name}' is installed but does not provide module '{module_name}'."
        ) from exc


def load_plugin_module(plugin_id: str):
    module_name = _plugin_id_to_module_name(plugin_id)
    return import_module(module_name)


def register_active_plugins(app: Flask) -> None:
    active_plugins = (
        db.session.execute(db.select(PluginRegistry).filter_by(active=True, installed=True)).scalars().all()
    )

    for plugin in active_plugins:
        try:
            module = _load_plugin_module(plugin.distribution_name, plugin.plugin_id)

            register = getattr(module, "register_blueprints", None)
            if register is None or not callable(register):
                raise AttributeError("Missing callable 'register_blueprints(app)'")

            register(app)
        except (ModuleNotFoundError, AttributeError) as exc:
            log.warning("Plugin '%s' could not be registered: %s", plugin.distribution_name, exc)
            plugin.active = False
            plugin.installed = False
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
        except Exception as exc:
            log.warning("Plugin '%s' failed during registration: %s", plugin.distribution_name, exc)
            plugin.active = False
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()


def get_active_plugins_menu_entries() -> list[dict]:
    active_plugins = (
        db.session.execute(db.select(PluginRegistry).filter_by(active=True, installed=True)).scalars().all()
    )

    entries: list[dict] = []
    for plugin in active_plugins:
        try:
            module = _load_plugin_module(plugin.distribution_name, plugin.plugin_id)

            getter = getattr(module, "get_menu_entry", None)
            if callable(getter):
                entry = getter()
            else:
                entry = getattr(module, "MENU_ENTRY", None)

            if not isinstance(entry, dict):
                continue

            label = entry.get("label")
            icon = entry.get("icon")
            url = entry.get("url")
            if not label or not url:
                continue

            entries.append(
                {
                    "distribution_name": plugin.distribution_name,
                    "plugin_id": plugin.plugin_id,
                    "label": label,
                    "icon": icon,
                    "url": url,
                }
            )
        except Exception as exc:
            log.warning("Plugin '%s' menu entry could not be loaded: %s", plugin.distribution_name, exc)

    return entries
