# src/multimedia_scraper/core/observability/bootstrap/bootstrap_snapshot.py

from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.core.observability.bootstrap.bootstrap_state import (
    ObservabilityBootstrapState,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ObservabilityBootstrapSnapshot:
    """
    Immutable observability runtime snapshot.
    """

    state: ObservabilityBootstrapState

    degraded_mode: bool

    healthy_sinks: int

    unhealthy_sinks: int

    dropped_events: int
