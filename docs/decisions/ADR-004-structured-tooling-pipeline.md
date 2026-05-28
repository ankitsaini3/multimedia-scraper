# ADR-004 — Structured Tooling Pipeline

**Status:** Accepted (Updated)

## Context
The project requires:
- Deterministic environments
- Strong validation
- Fast feedback loops
- Reproducible CI behavior

Tooling inconsistency increases:
- Debugging difficulty
- Onboarding complexity
- CI instability
- Maintenance cost

## Decision
The project will standardize on:
- uv for dependency & environment management
- ruff (lint + format)
- mypy (strict typing)
- pytest (parallel testing)
- poe + _tasks.py (cross-platform task orchestration)
- GitHub Actions CI

Validation is mandatory before merge.

### New Rationale Points
**Why `Makefile` Was Removed:**
- Shell portability problems across Linux, macOS, and Windows
- Windows inconsistencies (missing `rm`, `&&`, `;`, tab/space sensitivity)
- Fragile shell chaining breaks deterministically in different CI runners or developer setups

**Why `_tasks.py` Exists:**
- Guarantees deterministic command execution via Python's `subprocess`
- Ensures platform consistency without shell interpreter dependencies
- Maintains strict CI/local parity by abstracting OS-level path and process handling

**Why Ruff Replaced Black:**
- Single-tool formatting eliminates config drift and formatter conflicts
- Reduces tooling overlap (ruff lint + format replaces black, isort, flake8)
- 10–100x faster execution improves local feedback loops
- Simplified governance: one config source, one binary to maintain

## Consequences
### Positive
- Deterministic environments
- Fast local iteration
- Automated discipline
- Consistent formatting
- Stable CI behavior
- Cross-platform reliability without shell escaping or interpreter dependencies

### Negative
- Stricter setup requirements
- Additional tooling maintenance
- Reduced flexibility for ad-hoc workflows
- Slight overhead from Python orchestration layer (`_tasks.py`)

These tradeoffs are acceptable.

## Alternatives Considered
**Minimal Tooling**  
Rejected because:
- Governance becomes inconsistent
- Quality enforcement weakens
- Architecture erosion accelerates

**Highly Customized Internal Tooling**  
Rejected because:
- Excessive maintenance burden
- Poor solo-maintainer sustainability
- Unnecessary complexity