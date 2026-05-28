
# Error Handling Strategy

The system must fail predictably.

---

## Error Categories

| Category | Example |
|---|---|
| Domain Errors | invalid metadata |
| Infrastructure Errors | network failures |
| Integration Errors | incompatible plugin |
| Runtime Errors | playback failure |
| User Errors | invalid CLI arguments |

---

## Rules

- Never swallow exceptions silently.
- Use typed exceptions.
- Preserve root causes.
- Add structured logging.
- Translate infrastructure errors at boundaries.

---

## Boundary Translation

Infrastructure exceptions should not leak raw implementation details.

Example:

```text
yt-dlp exception
    -> StreamExtractionError
```

---