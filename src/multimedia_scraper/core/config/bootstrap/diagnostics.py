from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConfigBootstrapDiagnostics:
    phase: str
    source_count: int
    success: bool
