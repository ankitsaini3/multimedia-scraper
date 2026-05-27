# src/multimedia_scraper/core/observability/dto/correlation.py

from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.core.observability.dto.operation_trace import (
    OperationTraceDTO,
)
from multimedia_scraper.core.observability.dto.supervision_lineage import (
    SupervisionLineageDTO,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class CorrelationMetadataDTO:
    """
    Immutable runtime correlation metadata.

    Correlation MUST propagate across:
    - async tasks
    - supervision boundaries
    - retries
    - event pipelines
    - plugin boundaries

    This object MUST remain:
    - immutable
    - serialization-safe
    - replay-safe
    """

    correlation_id: str

    causation_id: str | None

    runtime_scope_id: str

    trace: OperationTraceDTO

    supervision: SupervisionLineageDTO
