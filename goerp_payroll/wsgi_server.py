# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from typing import TYPE_CHECKING, Optional

# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #
from waitress import serve as wsgi_server

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #
from goerp_payroll.log import log

if TYPE_CHECKING:
    from flask import Flask


# Servidor predefinido.
def serve(app: Optional[Flask] = None, host: str = "0.0.0.0", port: int | str = 5000):

    if app is None:
        raise ValueError("wsgi_server.serve requires a Flask app instance.")

    log.trace("Starting waitress on %s:%s", host, port)
    wsgi_server(app, host=host, port=port)
