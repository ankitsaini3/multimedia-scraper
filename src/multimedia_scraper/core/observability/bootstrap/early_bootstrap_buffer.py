# src/multimedia_scraper/core/observability/bootstrap/early_bootstrap_buffer.py

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Sequence
from typing import Final

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class EarlyBootstrapBuffer:
    """
    Bounded pre-runtime telemetry buffer.

    Exists ONLY during bootstrap initialization.

    Guarantees:
    - bounded memory usage
    - deterministic replay ordering
    - zero detached execution
    """

    DEFAULT_CAPACITY: Final[int] = 256

    def __init__(
        self,
        *,
        capacity: int = DEFAULT_CAPACITY,
    ) -> None:
        self._capacity = capacity

        self._events: deque[LogEventDTO] = deque(
            maxlen=capacity,
        )

    def append(
        self,
        event: LogEventDTO,
    ) -> None:
        self._events.append(
            event,
        )

    def drain(
        self,
    ) -> Sequence[LogEventDTO]:
        drained = tuple(
            self._events,
        )

        self._events.clear()

        return drained

    def snapshot(
        self,
    ) -> Iterable[LogEventDTO]:
        return tuple(
            self._events,
        )
