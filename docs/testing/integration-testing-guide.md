
# Integration Testing Guide

The current project state indicates architectural drift and integration instability.

The primary recovery strategy is:

1. freeze public contracts
2. document boundaries
3. add integration tests
4. evolve incrementally

---

# Priority Integration Tests

## 1. Plugin Discovery Integration

Validates:

- registry loading
- plugin validation
- capability registration
- duplicate detection

---

## 2. Search Aggregation Integration

Validates:

- provider fan-out
- async orchestration
- result normalization
- pagination contracts
- partial failures

---

## 3. Stream Resolution Integration

Validates:

- metadata extraction
- stream normalization
- playback source conversion
- source selection

---

## 4. Playback Integration

Validates:

- mpv adapter
- playback lifecycle
- event propagation
- retry behavior

---

## 5. Download Integration

Validates:

- transfer orchestration
- progress reporting
- cancellation
- integrity checks

---

## 6. Configuration Integration

Validates:

- override ordering
- environment handling
- runtime overrides
- default fallback behavior

---

## 7. Logging Integration

Validates:

- structured context
- exception formatting
- lifecycle logs
- request correlation

---

# Recommended Test Directory Layout

```text
/tests
    /unit

    /contract
        test_plugin_contracts.py
        test_stream_source_contracts.py
        test_search_result_contracts.py

    /integration
        /plugin
        /search
        /streaming
        /playback
        /download
        /configuration
        /logging

    /e2e
```

---
