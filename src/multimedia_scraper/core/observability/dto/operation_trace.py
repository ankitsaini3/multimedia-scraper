# src/multimedia_scraper/core/observability/dto/operation_trace.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OperationTraceDTO:
    """
    Immutable operation tracing metadata.

    Represents:
    - request lineage
    - retry lineage
    - operation ancestry
    - trace hierarchy

    Must remain deterministic and immutable.
    """

    trace_id: str

    span_id: str

    parent_span_id: str | None

    operation_id: str

    operation_name: str

    operation_version: int = 1

    started_at_utc: datetime
