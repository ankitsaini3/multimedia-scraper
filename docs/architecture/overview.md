# Architecture Overview

The project is divided into independently evolvable subsystems.

Primary subsystems:

| Subsystem | Responsibility |
|---|---|
| Plugin System | Provider extensibility |
| Search System | Cross-provider discovery |
| Extraction System | Metadata + stream extraction |
| Streaming System | Stream source handling |
| Playback System | Runtime playback orchestration |
| Download System | Download workflows |
| Configuration System | Layered configuration |
| Logging System | Structured observability |
| Event System | Cross-system notifications |
| Future Persistence | Metadata/index storage |
| Future Browser Automation | Dynamic provider support |

Each subsystem must:

- expose stable contracts
- minimize side effects
- avoid leaking infrastructure concerns
- remain independently testable
