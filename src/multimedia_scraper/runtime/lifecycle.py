from __future__ import annotations

from enum import Enum


class RuntimeLifecycleState(str, Enum):
    CREATED = "CREATED"

    BOOTSTRAPPING = "BOOTSTRAPPING"

    ACTIVE = "ACTIVE"

    SHUTTING_DOWN = "SHUTTING_DOWN"

    TERMINATED = "TERMINATED"

    FAILED = "FAILED"
