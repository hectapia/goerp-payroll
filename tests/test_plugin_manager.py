from __future__ import annotations

import types


def test_sync_plugin_registry_adds_new_plugins(app, db_session, monkeypatch):
    from goerp_payroll.model import PluginRegistry, db
    from goerp_payroll import plugin_manager

    monkeypatch.setattr(
        plugin_manager,
        "discover_installed_plugins",
        lambda: [
            plugin_manager.DiscoveredPlugin(
                distribution_name="goerp-payroll-plugin-gt",
                plugin_id="gt",
                version="1.0.0",
            )
        ],
    )

    with app.app_context():
        plugin_manager.sync_plugin_registry()

        rows = db.session.execute(db.select(PluginRegistry)).scalars().all()
        assert len(rows) == 1
        assert rows[0].distribution_name == "goerp-payroll-plugin-gt"
        assert rows[0].plugin_id == "gt"
        assert rows[0].version == "1.0.0"
        assert rows[0].active is False
        assert rows[0].installed is True


def test_sync_plugin_registry_marks_missing_active_as_inactive(app, db_session, monkeypatch):
    from goerp_payroll.model import PluginRegistry, db
    from goerp_payroll import plugin_manager

    with app.app_context():
        record = PluginRegistry()
        record.distribution_name = "goerp-payroll-plugin-gt"
        record.plugin_id = "gt"
        record.version = "1.0.0"
        record.active = True
        record.installed = True
        db.session.add(record)
        db.session.commit()

    monkeypatch.setattr(plugin_manager, "discover_installed_plugins", lambda: [])

    with app.app_context():
        plugin_manager.sync_plugin_registry()
        refreshed = db.session.execute(db.select(PluginRegistry)).scalar_one()
        assert refreshed.active is False
        assert refreshed.installed is False


def test_get_active_plugins_menu_entries_reads_getter(app, db_session, monkeypatch):
    from goerp_payroll.model import PluginRegistry, db
    from goerp_payroll import plugin_manager

    with app.app_context():
        record = PluginRegistry()
        record.distribution_name = "goerp-payroll-plugin-gt"
        record.plugin_id = "gt"
        record.version = "1.0.0"
        record.active = True
        record.installed = True
        db.session.add(record)
        db.session.commit()

    fake_module = types.SimpleNamespace(
        get_menu_entry=lambda: {"label": "Guatemala", "icon": "bi bi-geo-alt", "url": "/gt/"}
    )

    monkeypatch.setattr(plugin_manager, "_load_plugin_module", lambda distribution_name, plugin_id: fake_module)

    with app.app_context():
        entries = plugin_manager.get_active_plugins_menu_entries()
        assert entries == [
            {
                "distribution_name": "goerp-payroll-plugin-gt",
                "plugin_id": "gt",
                "label": "Guatemala",
                "icon": "bi bi-geo-alt",
                "url": "/gt/",
            }
        ]
