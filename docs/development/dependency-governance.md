
# Dependency Governance

# Philosophy

Dependency governance is mandatory.

Documentation alone is insufficient.

The project must automatically reject architectural violations.

---

# Why Governance Matters

Without strict dependency governance:

- layers begin leaking
- infrastructure contaminates domain logic
- plugin isolation collapses
- runtime coupling increases
- refactoring becomes dangerous

Async multimedia systems become unmaintainable quickly when boundaries are weak.

---

# Architectural Direction Rules

# Allowed Dependency Flow

```text
app
  ↓
core
  ↓
infrastructure
```

Plugins communicate through contracts.

Not through hidden internal imports.

---

# Forbidden Dependency Flow

## Forbidden

```text
core → infrastructure
core → plugins
plugins → app
```

---

# Enforcement Tools

## Import Linter

Primary architecture enforcement tool.

Rules are defined in:

```text
importlinter.toml
```

---

# Example Rules

```text
Core cannot import infrastructure
Plugins cannot import app layer
Infrastructure cannot import plugins
```

---

# Why Tooling Enforcement Is Mandatory

Humans eventually compromise architecture under delivery pressure.

Tooling does not.

The project should fail immediately when boundaries are violated.

---

# Strict Typing Policy

## Mandatory

```bash
mypy --strict
```

Reason:

- async integration stability
- plugin contract safety
- predictable refactoring
- runtime correctness

---

# Dependency Hygiene

## Tool

```text
deptry
```

Purpose:

- remove unused dependencies
- prevent accidental transitive reliance
- keep environments deterministic

---

# Governance Rules

Never:

- disable import-linter rules casually
- weaken typing to silence errors
- add dependencies without justification
- bypass architecture contracts

Governance exists to preserve long-term maintainability.
