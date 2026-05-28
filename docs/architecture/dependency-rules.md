# Dependency Rules

## Stable Dependency Direction

Dependencies must point inward.

```text
Interface -> Application -> Domain
Infrastructure -> Domain
```

---

## Forbidden Coupling

Avoid:

- infrastructure leaking into domain
- plugins calling CLI systems
- domain importing yt-dlp
- application importing mpv directly
- shared mutable global state

---

## Allowed Shared Contracts

Shared contracts belong in domain.

Examples:

```text
SearchProvider
ExtractionProvider
PlaybackSource
MediaMetadata
DownloadRequest
```

---

## Plugin Isolation

Plugins must not depend on other plugins.

Plugins communicate through stable domain contracts only.
