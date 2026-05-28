
# Download Pipeline

Downloads are orchestrated workflows.

The pipeline separates:

- extraction
- source selection
- transfer
- progress tracking
- validation
- storage

---

## Download Flow

```text
Download Request
    -> Source Resolution
    -> Transfer Strategy
    -> Progress Reporting
    -> Validation
    -> Completion Event
```

---

## Design Rules

Download orchestration must remain provider-agnostic.

Provider-specific logic belongs inside plugins.

---
