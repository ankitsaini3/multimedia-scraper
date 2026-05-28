# Plugin Architecture

Plugins are one of the most critical stability boundaries.

The plugin API is treated as a long-term contract.

---

## Plugin Responsibilities

Plugins may provide:

- search
- metadata extraction
- stream extraction
- downloading
- subtitles
- thumbnails
- authentication

---

## Plugin Constraints

Plugins must:

- implement stable interfaces
- avoid direct access to CLI/UI systems
- avoid global mutable state
- remain independently testable
- fail gracefully

---

## Plugin Discovery

Discovery is centralized.

Plugins register themselves through a registry.

The registry owns:

- lifecycle
- validation
- dependency checks
- capability checks

---

## Plugin Contracts

Stable contracts include:

```text
BasePlugin
SearchPlugin
ExtractorPlugin
DownloadPlugin
PlaybackProvider
```

Changing these contracts requires:

- ADR review
- compatibility evaluation
- migration strategy
- integration testing
