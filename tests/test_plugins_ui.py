from __future__ import annotations

from goerp_payroll.enums import TipoUsuario
from tests.helpers.auth import login_user


def test_plugins_ui_requires_login(client):
    res = client.get("/plugins/", follow_redirects=False)
    assert res.status_code in (301, 302)
    assert "/auth/login" in res.headers.get("Location", "")


def test_plugins_ui_lists_and_toggles(app, client, db_session, admin_user, monkeypatch):
    admin_user.tipo = TipoUsuario.ADMIN
    db_session.commit()

    res = login_user(client, "admin-test", "admin-password")
    assert res.status_code in (301, 302)

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

    list_res = client.get("/plugins/", follow_redirects=False)
    assert list_res.status_code == 200
    assert b"goerp-payroll-plugin-gt" in list_res.data

    from goerp_payroll.model import PluginRegistry, db

    with app.app_context():
        plugin = db.session.execute(db.select(PluginRegistry)).scalar_one()

    toggle_res = client.post(f"/plugins/toggle/{plugin.id}", follow_redirects=False)
    assert toggle_res.status_code in (301, 302)

    with app.app_context():
        refreshed = db.session.get(PluginRegistry, plugin.id)
        assert refreshed.active is True
