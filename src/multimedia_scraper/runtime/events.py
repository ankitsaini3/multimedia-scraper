from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final
from uuid import UUID, uuid4

EVENT_SCHEMA_VERSION: Final[int] = 1


@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeEvent:
    """
    Base immutable runtime event.

    Runtime events are:

    - transport-safe
    - ephemeral
    - in-memory only
    - coordination-oriented

    Runtime events are NOT telemetry events.
    """

    event_id: UUID

    event_type: str

    created_at_utc: datetime

    schema_version: int = EVENT_SCHEMA_VERSION


def create_runtime_event(
    *,
    event_type: str,
) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=uuid4(),
        event_type=event_type,
        created_at_utc=datetime.now(UTC),
    )
