# src/multimedia_scraper/core/observability/bootstrap/bootstrap_state.py

from __future__ import annotations

from strenum import StrEnum


class ObservabilityBootstrapState(
    StrEnum,
):
    PRE_BOOTSTRAP = "pre_bootstrap"

    EARLY_BOOTSTRAP = "early_bootstrap"

    INITIALIZING = "initializing"

    ACTIVE = "active"

    DEGRADED = "degraded"

    DRAINING = "draining"

    FLUSHING = "flushing"

    SHUTDOWN = "shutdown"
