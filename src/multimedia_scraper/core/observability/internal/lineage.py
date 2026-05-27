# src/multimedia_scraper/core/observability/internal/lineage.py

from __future__ import annotations

from multimedia_scraper.core.observability.dto.supervision_lineage import (
    SupervisionLineageDTO,
)


def create_child_supervision_lineage(
    lineage: SupervisionLineageDTO,
    *,
    supervisor_id: str,
    task_id: str | None,
) -> SupervisionLineageDTO:
    """
    Create immutable child supervision lineage.

    Parent lineage MUST remain untouched.
    """

    return SupervisionLineageDTO(
        runtime_id=lineage.runtime_id,
        root_supervisor_id=lineage.root_supervisor_id,
        supervisor_id=supervisor_id,
        parent_supervisor_id=lineage.supervisor_id,
        supervisor_depth=lineage.supervisor_depth + 1,
        task_id=task_id,
    )
