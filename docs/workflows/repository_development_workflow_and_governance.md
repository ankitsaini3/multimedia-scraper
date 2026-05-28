# Repository Development Workflow & Governance

## Purpose

This document defines the authoritative repository workflow, development process, branching strategy, commit conventions, and engineering governance model for the `multimedia_scraper` project.

The objective of this workflow is to maintain:

- architectural integrity
- deterministic development practices
- long-term maintainability
- implementation traceability
- stable runtime evolution
- disciplined subsystem ownership
- safe refactoring practices

This repository represents a long-lived runtime platform and not a short-lived application codebase. Development practices must therefore prioritize correctness, lifecycle integrity, structured evolution, and operational stability over rapid unstructured iteration.

---

# 1. Repository Philosophy

The repository follows the following engineering principles:

1. Architecture-first development
2. Deterministic implementation practices
3. Structured incremental evolution
4. Small and traceable changes
5. Runtime integrity over feature velocity
6. Explicit ownership and lifecycle governance
7. Stable and reproducible development environments
8. Continuous architectural validation

The repository is treated as:

- a runtime platform
- an orchestration system
- a plugin-capable execution environment
- a long-term maintainable infrastructure codebase

and not as:

- a prototype application
- a rapid experimentation sandbox
- an unstructured feature repository

---

# 2. Branching Strategy

## 2.1 Primary Branch

The repository uses a trunk-based workflow centered around a single stable branch:

```text
main
```

The `main` branch must always remain:

- bootable
- testable
- lint-clean
- deterministic
- architecturally valid
- releasable

The `main` branch must never contain:

- partially migrated subsystems
- unfinished architectural transitions
- broken runtime states
- unstable experimental implementations
- unreviewed architectural behavior

---

## 2.2 Feature Branches

All implementation work must occur in short-lived feature branches.

Recommended branch naming conventions:

```text
feat/<subsystem>/<topic>
fix/<subsystem>/<topic>
refactor/<subsystem>/<topic>
docs/<topic>
infra/<topic>
exp/<topic>
```

Examples:

```text
feat/config/bootstrap-loader
feat/runtime/supervision-tree
feat/download/retry-pipeline

fix/streaming/cancellation-leak

refactor/core/lifecycle-cleanup

infra/ci/test-matrix

exp/distributed-runtime
exp/wasm-workers
```

Feature branches should remain:

- narrowly scoped
- short-lived
- architecturally coherent
- isolated to bounded concerns

Long-running branches are discouraged.

---

## 2.3 Experimental Branches

Experimental or speculative architectural work must remain isolated in:

```text
exp/*
```

Examples include:

- distributed execution experiments
- alternate scheduler models
- WASM runtime prototypes
- remote worker systems
- actor-model experiments
- sandboxing prototypes

Experimental work must not destabilize the stable runtime architecture.

---

# 3. Commit Conventions

## 3.1 Commit Philosophy

Commits represent:

- architectural intent
- invariant changes
- lifecycle behavior changes
- isolated subsystem evolution

Commits must not represent:

- arbitrary coding sessions
- unrelated edits
- mixed behavioral changes
- large unstructured modifications

Each commit should ideally introduce:

- one architectural behavior
- one bounded invariant change
- one isolated subsystem transition

---

## 3.2 Commit Format

Commit messages must follow:

```text
<type>(<scope>): <description>
```

Examples:

```text
build(tooling): initialize project tooling foundation

feat(config): implement immutable configuration models
feat(runtime): implement lifecycle state machine
feat(supervision): add hierarchical task supervision

fix(download): prevent orphan retry tasks during shutdown

refactor(runtime): isolate cancellation propagation logic

docs(runtime): freeze structured concurrency invariants

infra(ci): add deterministic test matrix
```

---

## 3.3 Commit Types

| Type | Purpose |
|---|---|
| build | Build tooling and repository tooling |
| feat | New functionality |
| fix | Defect correction |
| refactor | Structural improvement without behavioral change |
| docs | Documentation and architecture contracts |
| test | Verification-related changes |
| perf | Performance improvements |
| infra | CI/CD and development infrastructure |
| security | Security-related changes |
| revert | Revert previous changes |

---

## 3.4 Commit Granularity

Commits should remain architecturally atomic.

Preferred:

```text
feat(config): implement immutable configuration DTOs
feat(config): add layered source resolution
feat(config): integrate bootstrap freeze semantics
```

Avoid:

```text
feat: implement configuration system
```

Large monolithic commits reduce traceability and architectural clarity.

---

# 4. Pull Request Governance

## 4.1 Pull Request Philosophy

All changes should be integrated through pull requests, including single-maintainer workflows.

Pull requests serve as:

- architectural checkpoints
- review boundaries
- historical design references
- subsystem evolution records
- invariant verification boundaries

---

## 4.2 Pull Request Scope

Pull requests should remain:

- subsystem-focused
- narrowly scoped
- architecturally coherent
- independently reviewable

Preferred pull request scope:

```text
one subsystem transition
one architectural capability
one bounded invariant change
```

Avoid combining unrelated architectural changes in a single pull request.

---

## 4.3 Pull Request Requirements

Every pull request should clearly document:

1. Architectural intent
2. Affected contracts
3. Ownership changes
4. Lifecycle implications
5. Failure behavior changes
6. Observability implications
7. Verification strategy
8. Migration considerations
9. Compatibility implications

---

# 5. Development Workflow

## 5.1 Architecture-First Development

The repository follows:

```text
contracts
→ architecture review
→ bounded implementation
→ invariant verification
→ integration
```

Implementation should not precede architectural understanding.

---

## 5.2 Recommended Implementation Sequence

For major subsystems:

1. Define or finalize contracts
2. Review ownership semantics
3. Review lifecycle semantics
4. Implement isolated models/interfaces
5. Implement orchestration behavior
6. Add observability
7. Add deterministic tests
8. Integrate into runtime bootstrap
9. Verify shutdown and recovery semantics

---

## 5.3 Incremental Integration

Subsystems should integrate incrementally.

Avoid:

- large all-at-once merges
- repository-wide rewrites
- partially migrated runtime states
- hidden compatibility breaks

Preferred approach:

```text
small coherent transitions
with continuous runtime validation
```

---

# 6. Architectural Governance

## 6.1 Contracts Are Authoritative

The `docs/contracts/` directory is authoritative.

Implementation must conform to contracts.

If implementation conflicts with architecture:

```text
contracts win
```

Architectural deviations require explicit review and formal revision.

---

## 6.2 Frozen Contracts

Frozen contracts represent stable architectural guarantees.

Frozen contracts must not be modified casually.

Changes to frozen contracts require:

- explicit architectural reasoning
- compatibility analysis
- lifecycle analysis
- migration analysis
- subsystem impact review

---

## 6.3 Runtime Integrity Prioritization

The repository prioritizes:

- runtime integrity
- deterministic behavior
- structured concurrency correctness
- lifecycle safety
- ownership correctness
- cleanup guarantees

over:

- rapid feature velocity
- premature optimization
- convenience abstractions
- implicit behavior

---

# 7. Testing & Verification Workflow

## 7.1 Deterministic Testing

All tests should prioritize deterministic behavior.

Tests must avoid uncontrolled dependence on:

- wall-clock time
- real network state
- developer machine state
- uncontrolled filesystem state
- unseeded randomness

---

## 7.2 Verification Expectations

Subsystem implementations should include:

- unit tests
- integration tests
- lifecycle validation
- cancellation verification
- cleanup verification
- serialization validation
- failure-path testing
- recovery testing

---

## 7.3 Runtime Safety Validation

Critical runtime systems should validate:

- orphan task prevention
- cancellation propagation
- supervision integrity
- resource cleanup
- deterministic shutdown
- retry boundaries
- serialization stability
- persistence recovery

---

# 8. Continuous Integration Expectations

## 8.1 Mandatory Validation

CI should eventually enforce:

- formatting validation
- static typing validation
- linting
- deterministic test execution
- import boundary validation
- architectural invariant tests
- serialization compatibility checks
- DTO validation tests
- contract compliance checks

---

## 8.2 Flaky Tests

Flaky tests are treated as defects.

Non-deterministic verification behavior should be investigated immediately.

---

## 8.3 Stable Mainline Requirement

The `main` branch should remain continuously stable.

Broken runtime states should never persist on `main`.

---

# 9. Refactoring Policy

## 9.1 Refactoring Expectations

Refactoring should:

- preserve architectural invariants
- preserve lifecycle semantics
- preserve ownership guarantees
- preserve observability guarantees
- preserve deterministic behavior

---

## 9.2 Large Refactors

Large refactors should occur in isolated migration branches.

Recommended migration approach:

1. Introduce compatibility layer
2. Incrementally migrate subsystems
3. Validate invariants continuously
4. Remove compatibility layer after stabilization

---

# 10. Release & Versioning Strategy

## 10.1 Early Versioning

Before stable runtime guarantees:

```text
0.x.y
```

Examples:

```text
0.1.0
0.2.0
0.3.0
```

Major architectural evolution is expected during early development.

---

## 10.2 Architecture Tags

Stable architectural milestones should be tagged.

Examples:

```text
arch-runtime-v1
arch-config-v1
arch-supervision-v1
arch-security-v1
```

These tags provide historical architectural reference points.

---

# 11. Engineering Principles

The repository follows the following engineering principles:

## Determinism

Equivalent inputs should produce equivalent runtime behavior.

---

## Structured Concurrency

Detached execution is forbidden.

All execution must remain supervised and lifecycle-bound.

---

## Explicit Ownership

All mutable runtime state, resources, tasks, and authority must have explicit ownership.

---

## Explicit Boundaries

Cross-boundary communication must remain explicit, serialized, and observable.

---

## Lifecycle Integrity

Startup, execution, shutdown, cleanup, and recovery semantics must remain deterministic.

---

## Observability

Runtime state and failures must remain observable and diagnosable.

---

## Security

Authority, capabilities, and trust boundaries must remain explicit and enforceable.

---

## Maintainability

Long-term maintainability is prioritized over short-term implementation convenience.

---

# 12. Final Repository Rule

The repository follows one overriding engineering rule:

```text
Never merge architectural uncertainty into main.
```

If architectural behavior is unclear:

1. isolate experimentation
2. clarify contracts
3. validate invariants
4. integrate incrementally

Stable architecture precedes stable implementation.

