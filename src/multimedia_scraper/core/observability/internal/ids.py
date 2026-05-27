# src/multimedia_scraper/core/observability/internal/ids.py

from __future__ import annotations

import uuid


def new_correlation_id() -> str:
    return uuid.uuid4().hex


def new_trace_id() -> str:
    return uuid.uuid4().hex


def new_span_id() -> str:
    return uuid.uuid4().hex
