
# Playback System

Playback orchestration is independent from extraction.

The playback layer consumes normalized playback sources.

---

## Responsibilities

Playback system handles:

- session lifecycle
- buffering
- state transitions
- playback events
- retries
- external player integration

---

## Player Isolation

MPV integration belongs to infrastructure.

The application layer should depend only on playback contracts.
