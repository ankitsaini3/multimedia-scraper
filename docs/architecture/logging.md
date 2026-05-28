# Logging System

Logging is treated as infrastructure shared across all systems.

The logging package must evolve as a reusable internal library.

---

## Logging Goals

- structured logs
- contextual metadata
- lifecycle visibility
- debugging support
- production diagnostics

---

## Required Context

Important runtime operations should include:

- request IDs
- plugin names
- provider names
- playback session IDs
- download IDs
- stream IDs

---

## Logging Rules

- never use print()
- avoid duplicate logs
- avoid noisy low-value logs
- preserve exception tracebacks
- standardize formatting

---