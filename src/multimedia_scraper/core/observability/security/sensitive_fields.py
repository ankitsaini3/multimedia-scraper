# src/multimedia_scraper/core/observability/security/sensitive_fields.py

from __future__ import annotations

SENSITIVE_FIELD_NAMES: frozenset[str] = frozenset(
    {
        "authorization",
        "proxy_authorization",
        "token",
        "access_token",
        "refresh_token",
        "id_token",
        "password",
        "passwd",
        "secret",
        "api_key",
        "apikey",
        "cookie",
        "set_cookie",
        "session",
        "session_id",
        "credential",
    },
)
