# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Tests para visitar todas las rutas de la aplicación automáticamente."""

from tests.helpers.auth import login_user


def test_visita_todas_las_rutas_sin_autenticacion(app, client):
    """
    Test que visita todas las rutas GET sin autenticación.

    Este test descubre automáticamente todas las rutas registradas en la
    aplicación y realiza peticiones GET a cada una para verificar que:
    - No hay errores 500 (Internal Server Error)
    - No hay errores 404 (Not Found) en rutas existentes
    - La aplicación permite navegación fluida

    Rutas que requieren autenticación deben redirigir (302/303), no fallar.

    Setup:
        - Cliente sin autenticar

    Action:
        - Descubrir todas las rutas GET
        - Hacer petición a cada ruta

    Verification:
        - No hay errores 500
        - Rutas sin parámetros responden correctamente
    """
    with app.app_context():
        routes_to_test = []

        # Obtener todas las reglas de enrutamiento
        for rule in app.url_map.iter_rules():
            # Solo probar rutas GET
            if "GET" in rule.methods:
                # Excluir rutas estáticas
                if rule.endpoint == "static":
                    continue

                # Solo probar rutas sin parámetros variables
                # (rutas con parámetros necesitan datos específicos)
                if "<" not in rule.rule:
                    routes_to_test.append(rule.rule)

        # Verificar que encontramos rutas
        assert len(routes_to_test) > 0, "No se encontraron rutas para probar"

        # Visitar cada ruta
        errores = []
        for route in routes_to_test:
            try:
                response = client.get(route, follow_redirects=False)

                # Verificar que no hay error 500
                if response.status_code >= 500:
                    errores.append(f"Ruta {route}: Error {response.status_code} (Internal Server Error)")

                # Las rutas existentes no deben devolver 404
                # Pueden devolver 302/303 (redirect a login) o 200 (OK)
                # o 403 (Forbidden) si están protegidas
                if response.status_code == 404:
                    errores.append(f"Ruta {route}: Error 404 (Not Found)")

            except Exception as e:
                errores.append(f"Ruta {route}: Excepción {str(e)}")

        # Si hay errores, fallar el test con información detallada
        if errores:
            mensaje_error = "\n".join(errores)
            assert False, f"Se encontraron errores en las siguientes rutas:\n{mensaje_error}"


def test_visita_todas_las_rutas_con_autenticacion(app, client, admin_user, db_session):
    """
    Test que visita todas las rutas GET con usuario autenticado.

    Este test verifica que un usuario autenticado puede navegar por todas
    las rutas sin encontrar errores 500 o 404.

    Setup:
        - Usuario admin autenticado

    Action:
        - Descubrir todas las rutas GET
        - Hacer petición a cada ruta como usuario autenticado

    Verification:
        - No hay errores 500
        - No hay errores 404 en rutas sin parámetros
        - Usuario puede navegar fluidamente
    """
    with app.app_context():
        # Autenticar usuario
        login_user(client, "admin-test", "admin-password")

        routes_to_test = []

        # Obtener todas las reglas de enrutamiento
        for rule in app.url_map.iter_rules():
            # Solo probar rutas GET
            if "GET" in rule.methods:
                # Excluir rutas estáticas
                if rule.endpoint == "static":
                    continue

                # Solo probar rutas sin parámetros variables
                if "<" not in rule.rule:
                    routes_to_test.append(rule.rule)

        # Verificar que encontramos rutas
        assert len(routes_to_test) > 0, "No se encontraron rutas para probar"

        # Visitar cada ruta
        errores = []
        advertencias = []
        rutas_exitosas = []

        for route in routes_to_test:
            try:
                response = client.get(route, follow_redirects=False)

                # Verificar que no hay error 500
                if response.status_code >= 500:
                    errores.append(f"Ruta {route}: Error {response.status_code} (Internal Server Error)")
                elif response.status_code == 404:
                    errores.append(f"Ruta {route}: Error 404 (Not Found)")
                elif response.status_code in [200, 302, 303]:
                    # Navegación exitosa
                    rutas_exitosas.append(f"Ruta {route}: {response.status_code}")
                else:
                    # Otros códigos de estado (como 403) no son errores críticos
                    advertencias.append(f"Ruta {route}: Código {response.status_code}")

            except Exception as e:
                errores.append(f"Ruta {route}: Excepción {str(e)}")

        # Si hay errores, fallar el test con información detallada
        # Incluir estadísticas en el mensaje de error
        if errores:
            estadisticas = (
                f"\n\nEstadísticas:\n"
                f"  Total de rutas probadas: {len(routes_to_test)}\n"
                f"  Rutas exitosas: {len(rutas_exitosas)}\n"
                f"  Advertencias: {len(advertencias)}\n"
                f"  Errores: {len(errores)}\n"
            )
            if advertencias:
                estadisticas += "\nAdvertencias:\n  " + "\n  ".join(advertencias[:5])
                if len(advertencias) > 5:
                    estadisticas += f"\n  ... y {len(advertencias) - 5} más"
            mensaje_error = "\n".join(errores) + estadisticas
            assert False, f"Se encontraron errores en las siguientes rutas:\n{mensaje_error}"


def test_lista_todas_las_rutas_disponibles(app):
    """
    Test de utilidad que lista todas las rutas disponibles en la aplicación.

    Este test valida que hay rutas registradas y cuenta los diferentes tipos.

    Setup:
        - App fixture

    Action:
        - Listar todas las rutas

    Verification:
        - Hay rutas registradas (GET y POST)
    """
    with app.app_context():
        rutas_get = []
        rutas_post = []
        rutas_otras = []

        for rule in app.url_map.iter_rules():
            if rule.endpoint == "static":
                continue

            route_info = {
                "ruta": rule.rule,
                "endpoint": rule.endpoint,
                "metodos": sorted(rule.methods - {"HEAD", "OPTIONS"}),
            }

            if "GET" in rule.methods:
                rutas_get.append(route_info)
            if "POST" in rule.methods:
                rutas_post.append(route_info)
            if not ("GET" in rule.methods or "POST" in rule.methods):
                rutas_otras.append(route_info)

        # Verificaciones
        assert len(rutas_get) > 0, "No hay rutas GET registradas"
        assert len(rutas_post) > 0, "No hay rutas POST registradas"

        # Para debugging, las estadísticas se pueden ver si el test falla
        estadisticas = (
            f"Rutas GET: {len(rutas_get)}, " f"Rutas POST: {len(rutas_post)}, " f"Otras rutas: {len(rutas_otras)}"
        )

        # Verificar números razonables
        assert len(rutas_get) >= 5, f"Muy pocas rutas GET. {estadisticas}"
        assert len(rutas_post) >= 3, f"Muy pocas rutas POST. {estadisticas}"
