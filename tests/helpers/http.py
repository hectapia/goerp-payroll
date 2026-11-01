# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""HTTP helpers for tests."""


def follow_redirects_once(client, response):
    """
    Follow a redirect response once.

    Args:
        client: Flask test client
        response: Response object with redirect

    Returns:
        Response: Response from following the redirect
    """
    if response.status_code not in (301, 302, 303, 307, 308):
        return response

    location = response.headers.get("Location", "")
    if not location:
        return response

    return client.get(location, follow_redirects=False)
