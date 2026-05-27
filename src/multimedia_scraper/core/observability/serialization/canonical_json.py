# src/multimedia_scraper/core/observability/serialization/canonical_json.py

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from typing import Any

from multimedia_scraper.core.errors.observability import (
    TelemetrySerializationError,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


def serialize_log_event(
    event: LogEventDTO,
) -> bytes:
    """
    Deterministic canonical JSON serialization.

    Guarantees:
    - sorted keys
    - UTF-8 encoding
    - stable enum encoding
    - stable datetime encoding
    """

    try:
        payload = asdict(event)

        serialized = json.dumps(
            payload,
            default=_json_default,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

        return serialized.encode("utf-8")

    except Exception as exc:
        raise TelemetrySerializationError(
            "failed to serialize structured log event",
        ) from exc


def _json_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, Enum):
        return value.value

    raise TypeError(
        f"unsupported serialization type: {type(value)!r}",
    )
