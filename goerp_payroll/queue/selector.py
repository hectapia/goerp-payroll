# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Automatic queue driver selection based on environment."""

from __future__ import annotations

import os
import sys

from goerp_payroll.log import log
from goerp_payroll.queue.driver import QueueDriver
from goerp_payroll.queue.drivers import DramatiqDriver, NoopQueueDriver

_cached_driver: QueueDriver | None = None


def _is_production_env() -> bool:
    env_markers = [
        os.environ.get("ENV"),
        os.environ.get("APP_ENV"),
        os.environ.get("FLASK_ENV"),
        os.environ.get("NODE_ENV"),
    ]
    return any(str(value).strip().lower() == "production" for value in env_markers if value is not None)


def _is_test_env() -> bool:
    """Detect if code is running under automated tests."""
    testing_flag = os.environ.get("TESTING", "").strip().lower()
    if testing_flag in {"1", "true", "yes", "on"}:
        return True
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return True
    if os.environ.get("PYTEST_VERSION"):
        return True
    if os.environ.get("PYTEST_XDIST_WORKER"):
        return True
    return "pytest" in sys.modules


def _ping_redis(redis_url: str) -> bool:
    """Test if Redis is available.

    Args:
        redis_url: Redis connection URL

    Returns:
        True if Redis responds to ping, False otherwise
    """
    try:
        import redis

        # Use connection pool for efficiency if multiple pings needed
        # Socket timeout ensures we don't hang waiting for Redis
        client = redis.from_url(
            redis_url,
            socket_connect_timeout=2,
            socket_timeout=2,
            decode_responses=False,
        )
        client.ping()
        # Close connection to avoid leaking resources
        client.close()
        return True
    except Exception:
        return False


def get_queue_driver(force_backend: str | None = None) -> QueueDriver:
    """Get the appropriate queue driver based on environment.

    Selection logic:
    1. If force_backend is specified and supported, use that backend
    2. If REDIS_URL exists and Redis responds -> use Dramatiq
    3. Otherwise -> use Noop driver (background disabled)

    Args:
        force_backend: Optional backend to force ('dramatiq')

    Returns:
        QueueDriver instance (Dramatiq or Noop)

    Raises:
        RuntimeError: If no driver is available
    """
    global _cached_driver
    driver: QueueDriver

    # In test environments, always use Noop driver to avoid optional dependencies
    if force_backend is None and _is_test_env():
        driver = NoopQueueDriver()
        _cached_driver = driver
        return driver

    # Return cached driver if available
    if _cached_driver is not None and force_backend is None:
        return _cached_driver

    # Get Redis URL from environment
    redis_url = os.environ.get("REDIS_URL") or os.environ.get("CACHE_REDIS_URL")

    if force_backend not in {None, "dramatiq"}:
        raise RuntimeError(f"Unsupported queue backend '{force_backend}'. Only 'dramatiq' is supported.")

    # Try Dramatiq only if Redis is available
    if redis_url and _ping_redis(redis_url):
        driver = DramatiqDriver(redis_url=redis_url)
        if driver.is_available():
            log.info("Using Dramatiq driver with Redis backend")
            _cached_driver = driver
            return driver
        log.warning("Redis available but Dramatiq failed to initialize")

    # No background queue available -> return Noop driver to keep app operational
    if _is_production_env():
        log.warning("Dramatiq+Redis unavailable in production. Background queue is disabled (Noop driver active).")
    else:
        log.info("Dramatiq+Redis unavailable. Background queue is disabled (Noop driver active).")

    driver = NoopQueueDriver()
    _cached_driver = driver
    return driver


def reset_cached_driver() -> None:
    """Reset the cached driver instance.

    This is mainly useful for testing to force driver reinitialization.
    """
    global _cached_driver
    _cached_driver = None
