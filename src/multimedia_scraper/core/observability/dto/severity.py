# src/multimedia_scraper/core/observability/dto/severity.py

from __future__ import annotations

from strenum import StrEnum


class LogSeverity(StrEnum):
    """
    Canonical semantic log severity taxonomy.

    Numeric severity inheritance from stdlib logging
    is intentionally forbidden.
    """

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"
