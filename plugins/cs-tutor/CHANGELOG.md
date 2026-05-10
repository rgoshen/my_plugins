# Changelog

## [0.2.0] - 2026-05-11

### Added
- `session-state-manager` shared skill — centralizes session LOAD and SAVE logic (resume check, roadmap update, log entry, transcript export) previously duplicated in `arch-teach` and `pl-teach`
- New-tutor authoring guide in README: step-by-step checklist and `session-state-manager` parameter contract for adding future tutors

### Changed
- `arch-teach` and `pl-teach` Steps 1 and 4 now reference `session-state-manager` instead of duplicating load/save logic
- `session-state-manager` is fully generic — parameterized by `roadmap-file` and `output-label`; no tutor-specific hardcoding
- Both tutor agents (`arch-tutor`, `pl-tutor`) updated to include `session-state-manager` in their `skills:` list
- Skill cross-reference language corrected from "delegate to" to "follow the phase defined in (already loaded in your context)"
- README version badge updated to v0.2.0; `session-state-manager` added to component table
- CONTRIBUTING.md updated with plugin-specific authoring guide pointer

## [0.1.0] - 2026-05-09

### Added
- Auto-export session transcripts via `scripts/export_session.py` at end of every session
- draw.io MCP server bundled in plugin manifest — no manual setup required
- draw.io diagram integration in `arch-teach`: generates native `.drawio` files per pattern with graceful fallback when draw.io is not installed
- Expanded first-session prelude for both tutors: overview, history, benefits, issues, and use cases (five required items, no skipping)
- Project overview section in kickoff: what we're building, why, tech stack / rough architecture, artifact types, definition of done
- Pytest test suite (18 tests) for `export_session.py` covering all extraction logic

### Changed
- Release workflow redesigned: version bumps via PR, workflow only tags and creates GitHub Releases (no direct commits to main)
- `export_session.py` renamed from `export-session.py` for Python importability
- Pytest CI job added to validate workflow

## [0.0.3] - 2026-05-09

### Fixed
- use kebab-case plugin name in manifest

All notable changes to the `cs-tutor` plugin.

## [0.0.2] - 2026-05-09

### Added
- scaffold marketplace structure and fix cs-tutor plugin
