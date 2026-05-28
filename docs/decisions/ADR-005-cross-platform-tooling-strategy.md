# ADR-005 — Cross-Platform Tooling Strategy

**Status:** Accepted

## Context
The project operates across multiple developer environments (Linux, macOS, Windows, WSL) and CI runners. Traditional shell-dependent task runners (`make`, inline `sh`/`cmd`/`powershell` scripts) cause:
- Shell fragmentation
- Platform-specific behavior and path escaping failures
- `Makefile` portability problems (GNU vs BSD, tab sensitivity, missing POSIX commands)
- CI/local drift where workflows pass locally but fail in CI (or vice versa)

A unified, shell-independent execution strategy is required to guarantee identical behavior everywhere.

## Decision
Adopt a cross-platform deterministic tooling strategy using:
- `uv` for environment resolution and dependency execution
- Python task orchestration (`_tasks.py`) for all multi-step workflows
- Shell-independent execution for development, validation, and CI pipelines

All task chaining, cleanup, and environment setup will bypass `/bin/sh`, `cmd.exe`, and PowerShell. `uv run <task>` will serve as the single entry point for local and CI workflows.

### Why
- Avoid shell fragmentation and platform-specific interpreter quirks
- Eliminate `Makefile` portability problems and fragile `&&`/`;` chaining
- Prevent CI/local drift by enforcing identical Python `subprocess` execution paths
- Guarantee that developers on any OS run the exact same validation steps as CI

## Consequences
### Positive
- Identical Linux/macOS/Windows behavior
- Simpler CI configuration (single `uv run ci` step)
- Deterministic automation with predictable error propagation
- Zero dependency on OS-level shell commands or interpreter versions
- Faster onboarding (no environment-specific setup guides)

### Negative
- Custom Python orchestration layer adds slight bootstrap overhead
- Slightly more code to maintain (`_tasks.py`)
- Requires basic Python scripting knowledge for advanced task modifications
- Loss of traditional shell one-liners for ad-hoc debugging

These tradeoffs are acceptable for long-term maintainability and cross-platform stability.

## Alternatives Considered
**GNU Make / POSIX Shell Scripts**  
Rejected because:
- Windows incompatibility without WSL/Cygwin
- Fragile command chaining and whitespace sensitivity
- High maintenance burden for cross-platform path/flag normalization

**`just` / Taskfile / External Runners**  
Rejected because:
- Require separate binary installation or containerization
- Still rely on underlying shell interpreters for command execution
- Introduce additional dependency management overhead

**Inline TOML Chaining (`uv run cmd1 && cmd2`)**  
Rejected because:
- `&&`/`;` behavior varies across `cmd.exe`, `powershell`, and `sh`
- No built-in error handling or conditional execution
- Difficult to maintain as workflow complexity grows