# ADR-003 — Dependency Governance Enforcement

## Status

Accepted

---

## Context

Large Python codebases gradually accumulate architectural drift.

Without enforcement:

- forbidden imports appear
- layers become coupled
- infrastructure leaks into core logic
- plugins bypass contracts

Documentation alone does not prevent erosion.

---

## Decision

The project will enforce architectural rules using:

- import-linter
- deptry
- ruff
- mypy
- pre-commit hooks
- CI validation

Boundary violations must fail automatically.

---

## Consequences

### Positive

- preserved architecture boundaries
- reduced hidden coupling
- safer refactoring
- deterministic dependency structure
- improved maintainability

### Negative

- stricter contribution process
- additional CI execution time
- higher upfront tooling complexity

These tradeoffs are acceptable.

---

## Alternatives Considered

### Documentation-Only Governance

Rejected because:

- humans eventually bypass rules
- architectural drift becomes inevitable

### Manual Review Enforcement

Rejected because:

- inconsistent enforcement
- reviewer fatigue
- poor long-term reliability

