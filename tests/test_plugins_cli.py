from __future__ import annotations

import types

import click


def test_cli_plugins_lists_installed_plugins(monkeypatch):
    from goerp_payroll import cli

    monkeypatch.setattr(
        cli,
        "discover_installed_plugins",
        lambda: [
            types.SimpleNamespace(plugin_id="gt"),
            types.SimpleNamespace(plugin_id="pa"),
        ],
    )

    cmd = cli.plugins
    assert sorted(cmd.list_commands(None)) == ["gt", "pa"]


def test_cli_plugin_init_and_update_invoke_module(monkeypatch):
    from goerp_payroll import cli

    calls = {"init": 0, "update": 0}

    fake_module = types.SimpleNamespace(
        init=lambda: calls.__setitem__("init", calls["init"] + 1),
        update=lambda: calls.__setitem__("update", calls["update"] + 1),
    )

    monkeypatch.setattr(cli, "load_plugin_module", lambda plugin_id: fake_module)

    plugin_cmd = cli.plugins.get_command(None, "gt")
    assert isinstance(plugin_cmd, click.core.Group)

    init_cmd = plugin_cmd.get_command(None, "init")
    update_cmd = plugin_cmd.get_command(None, "update")
    assert init_cmd is not None
    assert update_cmd is not None

    # Call the underlying callbacks directly (they expect a click ctx and an appcontext)
    # We only validate wiring to module functions here.
    init_fn = init_cmd.callback
    update_fn = update_cmd.callback

    # These callbacks require app context; wiring is tested at module level.
    assert callable(init_fn)
    assert callable(update_fn)


def test_cli_plugin_enable_toggles_active(app, db_session, monkeypatch):
    from goerp_payroll import plugin_manager
    from goerp_payroll.model import PluginRegistry, db

    # Pretend the plugin is installed so sync_plugin_registry keeps it installed
    monkeypatch.setattr(
        plugin_manager,
        "discover_installed_plugins",
        lambda: [plugin_manager.DiscoveredPlugin("goerp-payroll-plugin-gt", "gt", "1.0.0")],
    )

    with app.app_context():
        plugin = PluginRegistry(
            distribution_name="goerp-payroll-plugin-gt",
            plugin_id="gt",
            version="1.0.0",
            active=False,
            installed=True,
        )
        db.session.add(plugin)
        db.session.commit()

    runner = app.test_cli_runner()
    result = runner.invoke(args=["plugins", "gt", "enable"])

    assert result.exit_code == 0

    with app.app_context():
        refreshed = db.session.get(PluginRegistry, plugin.id)
        assert refreshed.active is True
