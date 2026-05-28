# Testing Strategy

# Philosophy

The goal is not test quantity.

The goal is runtime stability.

Phase 1 prioritizes testing of:

- foundations
- architecture
- async behavior
- lifecycle safety

before feature development.

---

# Testing Categories

# Unit Tests

Purpose:

- validate isolated logic
- verify deterministic behavior
- protect contracts

---

# Unit Test Targets

Mandatory for:

- RuntimeContext
- configuration loading
- plugin registry
- event dispatching
- task supervision
- cancellation propagation
- error handling

---

# Integration Tests

Purpose:

- validate subsystem interaction
- validate runtime lifecycle
- verify startup/shutdown correctness

---

# Integration Test Targets

Mandatory for:

- application startup
- shutdown lifecycle
- dependency wiring
- plugin loading
- async orchestration

---

# Architecture Tests

Purpose:

- preserve modular monolith boundaries
- prevent dependency leakage
- enforce architectural rules

---

# Architecture Validation

Mandatory checks:

- forbidden imports
- layer isolation
- plugin boundaries
- infrastructure separation

---

# Async Testing Philosophy

Async systems require special discipline.

Every async workflow should support:

- cancellation
- timeout handling
- graceful shutdown
- failure propagation

---

# Forbidden Practices

Never:

- ignore async task leaks
- swallow exceptions silently
- create unmanaged background tasks
- weaken tests to satisfy CI

---

# CI Enforcement

Testing is mandatory in CI.

Required CI checks:

```text
ruff
black --check
mypy --strict
pytest
import-linter
deptry
```

---

# Long-Term Philosophy

The testing strategy exists to preserve:

- deterministic behavior
- runtime safety
- maintainability
- confidence during refactoring