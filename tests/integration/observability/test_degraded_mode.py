# tests/integration/observability/test_degraded_mode.py

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from multimedia_scraper.core.observability.bootstrap.bootstrap_observability import (
    BootstrapObservabilityController,
)
from multimedia_scraper.core.observability.bootstrap.degraded_logger import (
    DegradedObservabilityLogger,
)
from multimedia_scraper.core.observability.bootstrap.early_bootstrap_buffer import (
    EarlyBootstrapBuffer,
)
from multimedia_scraper.core.observability.bootstrap.startup_diagnostics import (
    StartupDiagnosticsRegistry,
)
from multimedia_scraper.core.observability.dto.correlation import (
    CorrelationMetadataDTO,
)
from multimedia_scraper.core.observability.dto.event_category import (
    EventCategory,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.dto.operation_trace import (
    OperationTraceDTO,
)
from multimedia_scraper.core.observability.dto.severity import (
    LogSeverity,
)
from multimedia_scraper.core.observability.dto.supervision_lineage import (
    SupervisionLineageDTO,
)
from multimedia_scraper.core.observability.sinks.base import (
    BaseTelemetrySink,
)
from multimedia_scraper.core.observability.sinks.composite_sink import (
    CompositeTelemetrySink,
)
from multimedia_scraper.core.observability.sinks.console_sink import (
    ConsoleTelemetrySink,
)


class FailingSink(
    BaseTelemetrySink,
):
    async def _write_event(
        self,
        event: LogEventDTO,
    ) -> None:
        raise RuntimeError(
            "sink failure",
        )


def _event() -> LogEventDTO:
    trace = OperationTraceDTO(
        trace_id="trace",
        span_id="span",
        parent_span_id=None,
        operation_id="op",
        operation_name="runtime",
        started_at_utc=datetime.now(
            tz=UTC,
        ),
    )

    supervision = SupervisionLineageDTO(
        runtime_id="runtime",
        root_supervisor_id="root",
        supervisor_id="root",
        parent_supervisor_id=None,
        supervisor_depth=0,
    )

    correlation = CorrelationMetadataDTO(
        correlation_id="corr",
        causation_id=None,
        runtime_scope_id="scope",
        trace=trace,
        supervision=supervision,
    )

    return LogEventDTO(
        timestamp_utc=datetime.now(
            tz=UTC,
        ),
        monotonic_ns=1,
        severity=LogSeverity.ERROR,
        event_category=(EventCategory.TELEMETRY),
        subsystem="runtime",
        operation="emit",
        message="failure",
        correlation=correlation,
        fields={},
    )


@pytest.mark.asyncio
async def test_degraded_mode_activation() -> None:
    sink = CompositeTelemetrySink(
        sinks=[
            FailingSink(),
        ],
    )

    degraded = DegradedObservabilityLogger(
        sink=ConsoleTelemetrySink(),
    )

    controller = BootstrapObservabilityController(
        early_buffer=(EarlyBootstrapBuffer()),
        sink=sink,
        degraded_logger=degraded,
        diagnostics=(StartupDiagnosticsRegistry()),
    )

    await controller.initialize()

    assert controller.degraded_mode is False

    await controller.emit(
        _event(),
    )

    # allow sink worker execution
    await asyncio.sleep(0)

    assert controller.degraded_mode is True
