# src/multimedia_scraper/core/observability/context/propagation.py

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import Token

from multimedia_scraper.core.errors.observability import (
    CorrelationPropagationError,
)
from multimedia_scraper.core.observability.context.runtime_context import (
    current_telemetry_context,
)
from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)
from multimedia_scraper.core.observability.internal.context_builders import (
    create_child_telemetry_context,
)


@contextmanager
def bind_telemetry_context(
    context: TelemetryContextDTO,
) -> Iterator[TelemetryContextDTO]:
    """
    Bind immutable telemetry context to current task execution.

    Guarantees:
    - task-local propagation
    - async-safe context isolation
    - deterministic restoration
    """

    token: Token[TelemetryContextDTO | None]

    token = current_telemetry_context.set(
        context,
    )

    try:
        yield context

    finally:
        current_telemetry_context.reset(
            token,
        )


@contextmanager
def child_telemetry_context(
    *,
    subsystem: str | None = None,
    operation: str | None = None,
    supervisor_id: str | None = None,
    task_id: str | None = None,
) -> Iterator[TelemetryContextDTO]:
    """
    Create child task-local telemetry lineage.

    Used for:
    - supervised child tasks
    - request pipelines
    - retries
    - event consumers
    - plugin execution scopes

    Context creation is immutable and lineage-preserving.
    """

    parent = current_telemetry_context.get()

    if parent is None:
        raise CorrelationPropagationError(
            "cannot create child telemetry context without active parent context",
        )

    child = create_child_telemetry_context(
        parent,
        subsystem=subsystem,
        operation=operation,
        supervisor_id=supervisor_id,
        task_id=task_id,
    )

    with bind_telemetry_context(
        child,
    ):
        yield child


def get_telemetry_context() -> TelemetryContextDTO | None:
    """
    Return current immutable telemetry context.
    """

    return current_telemetry_context.get()
