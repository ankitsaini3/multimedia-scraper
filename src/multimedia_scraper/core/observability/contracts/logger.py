# src/multimedia_scraper/core/observability/contracts/logger.py

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from multimedia_scraper.core.observability.dto.event_category import (
    EventCategory,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.dto.severity import (
    LogSeverity,
)
from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)


class RuntimeLogger(Protocol):
    """
    Runtime-scoped structured logger contract.

    This is NOT a global singleton logger.

    Implementations MUST remain:
    - lifecycle-aware
    - task-aware
    - async-safe
    - bounded
    - supervision-aware
    """

    async def emit(
        self,
        event: LogEventDTO,
    ) -> None:
        """
        Emit immutable structured telemetry event.
        """

    async def log(
        self,
        *,
        severity: LogSeverity,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
        exception: BaseException | None = None,
    ) -> None:
        """
        Emit structured runtime event.
        """

    async def trace(
        self,
        *,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
    ) -> None: ...

    async def debug(
        self,
        *,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
    ) -> None: ...

    async def info(
        self,
        *,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
    ) -> None: ...

    async def warn(
        self,
        *,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
    ) -> None: ...

    async def error(
        self,
        *,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
        exception: BaseException | None = None,
    ) -> None: ...

    async def fatal(
        self,
        *,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
        exception: BaseException | None = None,
    ) -> None: ...
