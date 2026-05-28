from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeId:
    value: UUID

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeMetadata:
    runtime_version: str

    created_at: datetime

    bootstrap_completed_at: datetime | None
