# src/multimedia_scraper/core/observability/bootstrap/startup_diagnostics.py

from __future__ import annotations

from datetime import UTC, datetime

from multimedia_scraper.core.observability.bootstrap.bootstrap_diagnostics import (
    BootstrapPhaseDiagnostic,
)


class StartupDiagnosticsRegistry:
    """
    Deterministic startup diagnostic registry.

    Guarantees:
    - append-only startup diagnostics
    - immutable snapshots
    - deterministic ordering
    """

    def __init__(
        self,
    ) -> None:
        self._diagnostics: list[BootstrapPhaseDiagnostic] = []

    def phase_started(
        self,
        *,
        phase: str,
    ) -> BootstrapPhaseDiagnostic:
        diagnostic = BootstrapPhaseDiagnostic(
            phase=phase,
            started_at_utc=(
                datetime.now(
                    tz=UTC,
                )
            ),
            completed_at_utc=None,
            success=False,
            failure_type=None,
            failure_message=None,
        )

        self._diagnostics.append(
            diagnostic,
        )

        return diagnostic

    def phase_completed(
        self,
        *,
        phase: str,
    ) -> None:
        for index, item in enumerate(
            self._diagnostics,
        ):
            if item.phase == phase and item.completed_at_utc is None:
                self._diagnostics[index] = BootstrapPhaseDiagnostic(
                    phase=item.phase,
                    started_at_utc=(item.started_at_utc),
                    completed_at_utc=(
                        datetime.now(
                            tz=UTC,
                        )
                    ),
                    success=True,
                    failure_type=None,
                    failure_message=None,
                )

                return

    def phase_failed(
        self,
        *,
        phase: str,
        exception: BaseException,
    ) -> None:
        for index, item in enumerate(
            self._diagnostics,
        ):
            if item.phase == phase and item.completed_at_utc is None:
                self._diagnostics[index] = BootstrapPhaseDiagnostic(
                    phase=item.phase,
                    started_at_utc=(item.started_at_utc),
                    completed_at_utc=(
                        datetime.now(
                            tz=UTC,
                        )
                    ),
                    success=False,
                    failure_type=(type(exception).__name__),
                    failure_message=str(
                        exception,
                    ),
                )

                return

    def snapshot(
        self,
    ) -> tuple[BootstrapPhaseDiagnostic, ...]:
        return tuple(
            self._diagnostics,
        )
