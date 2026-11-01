# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 - 2026 BMO Soluciones, S.A.
"""Security module - HTTP Security Headers and Security Utilities.

This module implements security best practices for Flask applications,
including HTTP security headers to protect against common web vulnerabilities.
"""

from __future__ import annotations


def configure_security_headers(app):
    """Configure HTTP security headers for the Flask application.

    Implements OWASP recommendations for secure HTTP headers:
    - Content-Security-Policy: Prevents XSS and data injection attacks
    - X-Frame-Options: Prevents clickjacking attacks
    - X-Content-Type-Options: Prevents MIME sniffing
    - Strict-Transport-Security: Forces HTTPS connections (production only)
    - X-XSS-Protection: Legacy XSS protection for older browsers
    - Referrer-Policy: Controls referrer information leakage

    Args:
        app: Flask application instance
    """
    from goerp_payroll.config import DESARROLLO

    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""

        # Content Security Policy - Restricts resource loading
        # Allows self-hosted resources and specific external sources
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers["Content-Security-Policy"] = csp

        # Prevent clickjacking - don't allow framing by any site
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Legacy XSS protection (for older browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # HSTS - Force HTTPS (only in production, never in testing)
        enable_hsts = not DESARROLLO and not app.config.get("TESTING", False)
        if enable_hsts:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response

    return app
