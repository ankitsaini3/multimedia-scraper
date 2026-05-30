from __future__ import annotations

from enum import Enum


class PluginLifecycleState(str, Enum):
    INITIALIZING = "initializing"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    DISCOVERED = "discovered"
    REGISTERED = "registered"
    VALIDATED = "validated"
    ACTIVATING = "activating"
    ACTIVE = "active"
    DEGRADED = "degraded"
    FAILED = "failed"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED = "terminated"
