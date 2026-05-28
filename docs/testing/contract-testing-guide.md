
# Contract Testing

Contract tests protect long-term architectural stability.

These tests should fail immediately when:

- DTO fields change
- interfaces change
- plugin contracts change
- event schemas change

---

## High Value Contract Targets

```text
SearchResult
MediaMetadata
PlaybackSource
BasePlugin
SearchPlugin
ExtractorPlugin
DownloadRequest
ProgressTracker
```

---