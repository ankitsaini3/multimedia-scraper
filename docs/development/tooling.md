# Tooling & Development Environment

## Cross-Platform Parity

All workflows run identically on Linux, macOS, Windows, WSL, and GitHub Actions.

Shell-dependent commands (`make`, `&&`, `;`, `/bin/sh` vs `cmd.exe`) are explicitly avoided.

---

# Python Version

```text
>= 3.11
```

## Why

Python 3.11 provides:

- mature async ecosystem support
- stable typing support (`|` union syntax, `TypeGuard`)
- excellent tooling compatibility

The project targets `>=3.10` but enforces `3.10` as the baseline validation version.

---

# Package & Environment Management

## Tool

```text
uv
```

### Why uv

- fast, deterministic dependency resolution
- lockfile-driven reproducibility (`uv.lock`)
- zero global Python pollution
- built-in virtual environment management
- native CI acceleration

---

# Environment Setup

## 1. Initialize Environment & Install Dependencies

```bash
uv sync --extra dev
```

Installs runtime + all development tooling defined in `[project.optional-dependencies]`.


## Git Hooks (Optional)
This project does not enforce automatic git hooks. Validation is run explicitly via task commands or CI.

If you prefer local hook enforcement for faster feedback, run:
```bash
uv run pre-commit install --install-hooks
```

# Task Orchestration

## Tool

```text
poe + _tasks.py
```

### Why

- replaces `Makefile` (cross-platform fragile)
- zero shell interpreter dependencies
- deterministic command sequencing
- identical local/CI execution paths

All tasks are defined in `[tool.poe.tasks]` within `pyproject.toml`.

### Core Commands

```bash
uv run poe fmt-chk    # Check if files are correctly formatted without modifying them (fails if formatting is needed) 
uv run poe fmt        # Auto-format all Python files with Ruff to enforce consistent code style
uv run poe lint       # Lint + auto-fix safe issues
uv run poe lint       # Run Ruff linter in check-only mode to report all code quality issues
uv run poe type       # Perform static type checking with mypy to catch type-related bugs
uv run poe test       # Run the test suite in parallel across all available CPU cores for faster execution
uv run poe check      # Full pre-commit validation (format-chk + lint-chk + type + test)
uv run poe cov        # Run tests with code coverage and display missing/uncovered lines in the terminal
uv run poe ci         # Full CI pipeline (clean + fmt + lint + type + cov)
uv run poe clean      # Remove caches, build artifacts, coverage reports
uv run poe arch       # Check architectural boundaries with ImportLinter (forbidden imports)
uv run poe deps       # Check dependencies in source code only (avoids false positives from tests/scripts)
```

---

# Formatting

## Ruff Format

```bash
uv run poe fmt
```

Ruff handles **all** formatting. Black, isort, and manual whitespace rules are deprecated.

- Single config source (`[tool.ruff]` + `[tool.ruff.format]`)
- 10–100x faster than legacy formatters
- Guaranteed idempotent output

---

# Linting

## Ruff Check

```bash
uv run poe lint-chk
```

Purpose:

- lint enforcement (`E`, `F`, `W`, `B`, `C90`, `SIM`, `UP`, `I`)
- automatic import sorting
- async correctness validation
- dead code & print suppression in production paths

Per-file ignores are centralized in `[tool.ruff.lint.per-file-ignores]`.

---

# Type Checking

## Mypy Strict Mode

```bash
uv run poe type
```

Strict typing is mandatory.

- `strict = true` enables all type safety guarantees
- `pydantic.mypy` plugin ensures model validation accuracy
- Tests allow relaxed typing via `[[tool.mypy.overrides]]`

No weakening of typing rules is allowed without an ADR.

---

# Testing

## Run Tests

```bash
uv run poe test
```

- Parallel execution via `pytest-xdist` (`-n auto --dist loadfile`)
- Async mode set to `auto` in `[tool.pytest.ini_options]`
- Coverage reports available via `uv run poe cov`

---

# Architecture Validation

## Import Linter

```bash
uv run poe arch
```

Purpose:

- prevent dependency leakage
- preserve layer isolation (`core`, `infrastructure`, `plugins`, `app`)
- maintain modular monolith boundaries

Contracts are defined in `[tool.importlinter.contracts]`.

---

# Dependency Validation

## Deptry

```bash
uv run poe deps
```

Purpose:

- detect unused dependencies
- prevent dependency sprawl
- keep packaging deterministic

Dev group mapping is handled via `pep621_dev_dependency_groups = ["dev"]`.

---

# Mandatory Validation Workflow

## Before Every Commit

```bash
uv run poe check
```

This runs:

- `ruff format --check .`
- `ruff check .`
- `mypy src/multimedia_scraper`
- `pytest` (parallel)

## Before Every Push / CI Trigger

```bash
uv run poe ci
```

This runs:

- full cleanup
- formatting
- linting with auto-fix
- strict type checking
- coverage reporting

Architectural checks (`deptry`, `import-linter`) are enforced via pre-push hooks and GitHub Actions.

---

# Non-Negotiable Rules

Never:

- bypass pre-commit hooks
- disable CI checks casually
- weaken strict typing for convenience
- ignore import boundary violations
- commit failing checks
- use shell-dependent task runners (`make`, `&&`, custom bash scripts)

Architectural erosion begins when governance becomes optional.

---
