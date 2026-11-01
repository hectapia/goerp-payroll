# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Rate limiting configuration for the application.

This module configures rate limiting to protect against brute force attacks
and abuse, particularly for authentication endpoints.
"""

from __future__ import annotations

# <-------------------------------------------------------------------------> #
# Standard library
# <-------------------------------------------------------------------------> #
from os import environ
from typing import Any, cast

# <-------------------------------------------------------------------------> #
# Third party libraries
# <-------------------------------------------------------------------------> #
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# <-------------------------------------------------------------------------> #
# Local modules
# <-------------------------------------------------------------------------> #


def get_rate_limiter_storage():
    """Get storage backend for rate limiter based on available configuration.

    Returns:
        str: Storage URI for rate limiter
        - Uses Redis if REDIS_URL or SESSION_REDIS_URL is available (production)
        - Falls back to memory storage for development/testing
    """
    # Try to get Redis URL from environment
    redis_url = environ.get("REDIS_URL") or environ.get("SESSION_REDIS_URL")

    if redis_url:
        # Use Redis for distributed rate limiting (production)
        return redis_url
    # Use memory storage for development/testing
    # Note: This won't work across multiple processes
    return "memory://"


# Default configuration for rate limiting
DEFAULT_RATE_LIMITS = ["200 per day", "50 per hour"]
DEFAULT_STORAGE_OPTIONS = {"socket_connect_timeout": 30}
DEFAULT_STRATEGY = "fixed-window"

# Global limiter instance (initialized via init_app in configure_rate_limiting)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=cast(Any, DEFAULT_RATE_LIMITS),
    storage_options=cast(Any, DEFAULT_STORAGE_OPTIONS),
    strategy=DEFAULT_STRATEGY,
)


def configure_rate_limiting(app):
    """Configure rate limiting for the Flask application.

    Sets up Flask-Limiter with appropriate storage backend:
    - Disabled for testing (to avoid rate limit issues in tests)
    - Redis for production (distributed, persistent)
    - Memory for development (simple, non-persistent)

    Args:
        app: Flask application instance

    Returns:
        Limiter: Configured Flask-Limiter instance
    """
    from goerp_payroll.log import log

    # Disable rate limiting in testing mode
    if app.config.get("TESTING"):
        app.config["RATELIMIT_ENABLED"] = False
        log.info("Rate limiting disabled (testing mode)")
        limiter.init_app(app)
        return limiter

    storage_uri = app.config.get("RATELIMIT_STORAGE_URI") or get_rate_limiter_storage()
    app.config["RATELIMIT_STORAGE_URI"] = storage_uri

    # Log which storage backend we're using
    if storage_uri.startswith("redis"):
        log.info("Rate limiting configured with Redis storage (production mode)")
    else:
        log.info("Rate limiting configured with memory storage (development mode)")

    limiter.init_app(app)

    # Note: Specific endpoint rate limits can be applied using decorators in the blueprints.
    # For the login endpoint, we apply a stricter limit (5 per minute) to prevent brute force.
    # This is documented in the security audit report.

    return limiter
