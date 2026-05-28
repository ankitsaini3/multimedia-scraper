# Layering Rules

## Domain Layer

Contains:

- entities
- DTOs
- enums
- value objects
- contracts
- protocols
- validation rules
- domain events

Must NOT contain:

- filesystem access
- networking
- framework logic
- database logic
- yt-dlp usage
- mpv usage
- browser automation

Examples:

```text
SearchResult
MediaMetadata
StreamSource
PlaybackSession
PluginCapability
```

---

## Application Layer

Contains orchestration logic.

Responsibilities:

- coordinating workflows
- handling use cases
- managing pipelines
- lifecycle orchestration
- retries
- recovery
- task coordination

Must NOT:

- directly perform infrastructure operations
- contain UI logic
- contain provider-specific logic

Examples:

```text
SearchAggregator
PlaybackCoordinator
DownloadOrchestrator
StreamResolver
```

---

## Infrastructure Layer

Contains implementation details.

Responsibilities:

- yt-dlp integration
- mpv integration
- browser automation
- database access
- filesystem access
- HTTP clients
- process management
- caching

Infrastructure implements domain/application contracts.

Examples:

```text
YoutubePlugin
MpvPlayer
SqliteRepository
YtDlpExtractor
```

---

## Interface Layer

Contains external entrypoints.

Responsibilities:

- CLI
- future GUI
- future HTTP API
- future websocket layer

Interfaces must remain thin.

Interfaces orchestrate through application services.

