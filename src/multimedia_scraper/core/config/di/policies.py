from __future__ import annotations

IMMUTABLE_CONFIG_POLICY = frozenset(
    {
        "runtime",
        "cache",
        "ffmpeg",
        "plugins",
        "network",
    }
)
