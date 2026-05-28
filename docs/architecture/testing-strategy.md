
# Testing Strategy

The project prioritizes integration stability over isolated implementation details.

Testing layers:

```text
Unit Tests
Contract Tests
Integration Tests
End-to-End Tests
```

---

## Unit Tests

Focus:

- domain logic
- DTO validation
- parsing
- utility behavior

Unit tests must avoid external systems.

---

## Contract Tests

Protect:

- plugin APIs
- DTO schemas
- protocol stability
- event payloads

These are critical for long-term evolution.

---

## Integration Tests

Highest priority.

Integration tests validate:

- plugin interoperability
- extraction pipeline
- playback pipeline
- search aggregation
- configuration loading
- logging integration
- event propagation

---

## End-to-End Tests

Validate real user flows.

Examples:

```text
search -> select -> play
search -> download
stream resolution -> playback
```

---