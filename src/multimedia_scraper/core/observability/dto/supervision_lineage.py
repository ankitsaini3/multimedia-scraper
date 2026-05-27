# src/multimedia_scraper/core/observability/dto/supervision_lineage.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class SupervisionLineageDTO:
    """
    Immutable supervision lineage snapshot.

    Represents deterministic supervision ownership ancestry.

    Must remain:
    - immutable
    - serialization-safe
    - replay-safe
    - runtime-boundary-safe
    """

    runtime_id: str

    root_supervisor_id: str

    supervisor_id: str

    parent_supervisor_id: str | None

    supervisor_depth: int

    task_id: str | None = None
