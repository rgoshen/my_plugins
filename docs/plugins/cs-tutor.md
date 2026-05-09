---
title: cs-tutor
layout: default
parent: Plugins
nav_order: 1
---

# cs-tutor

![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)
![Build](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Senior-engineer mentors for computer science learning — architecture patterns and programming languages. Follows a strict mentor-not-driver model: you make every decision, you write every line of code.
{: .fs-5 }

---

## Prerequisites

### draw.io *(arch-teach only)*

The `arch-teach` skill produces native `.drawio` architectural diagrams and opens them automatically via the bundled `@drawio/mcp` server. This requires the **draw.io desktop app**.

[Download draw.io](https://www.drawio.com/){: .btn .btn-outline }

The MCP server is bundled with this plugin and configured automatically on install. If draw.io is not installed, `.drawio` files are still written to disk and can be opened manually or at [app.diagrams.net](https://app.diagrams.net).

---

## Install

```
/plugin marketplace add rgoshen/my_plugins
/plugin install cs-tutor@my-plugins
```

---

## Components

### Commands

| Command | Description |
|---|---|
| `/cs-tutor:arch-teach` | Start or resume a software architecture patterns tutoring session |
| `/cs-tutor:pl-teach` | Start or resume a programming language tutoring session |

### Agents

| Agent | Description |
|---|---|
| `arch-tutor` | Senior engineer persona for architecture patterns tutoring. Teaches one pattern at a time, grounded in Fowler, Evans, Newman, Hohpe. |
| `pl-tutor` | Senior engineer persona for programming language tutoring. Grounds every concept in current official docs before teaching. |

### Skills

| Skill | Description |
|---|---|
| `arch-teach` | Session workflow for architecture tutoring — roadmap, draw.io diagrams, ADRs, session export |
| `pl-teach` | Session workflow for language tutoring — roadmap, code review, practice project, session export |

### Scripts

| Script | Description |
|---|---|
| `scripts/export_session.py` | Reads the session JSONL and writes a verbatim numbered transcript to `sessions/session-NNN.txt` at end of session |

---

## Usage

### Start an architecture session

```
/cs-tutor:arch-teach
/cs-tutor:arch-teach hexagonal
/cs-tutor:arch-teach event-driven
/cs-tutor:arch-teach microservices boundaries
```

### Start a language session

```
/cs-tutor:pl-teach
/cs-tutor:pl-teach Rust
/cs-tutor:pl-teach Go
/cs-tutor:pl-teach OCaml
```

---

## How sessions work

Both tutors are stateful. Run the command from the repo where you want session files to live.

| File | Purpose |
|---|---|
| `lastsession.md` | Rolling session log, newest entry on top. The tutor resumes from here. |
| `architecture-roadmap.md` / `language-roadmap.md` | Curriculum checklist, checked off as concepts land. |
| `teaching-plan.md` | Project overview + user stories. Every concept produces a deliverable that ships into the current story. |
| `sessions/session-NNN.txt` | Verbatim transcript of each completed session, auto-exported. |

### Kickoff sequence (first session only)

1. Confirm language or architecture focus
2. Build or import a curriculum roadmap
3. Design a practice project — the tutor presents a full **project overview** (what we're building, why, tech stack, project layout, definition of done) and gets your approval before writing it
4. Break the project into user stories

### First session prelude

Before the first concept the tutor covers five things — **overview, history, benefits, issues, and use cases** — to frame everything that follows. This happens once and is not repeated on resume.

### Architectural diagrams *(arch-teach)*

For each pattern the tutor produces a native `.drawio` diagram (C4 context/container, component map, sequence, data flow). Diagrams open automatically in draw.io desktop via the bundled MCP server. The saved `.drawio` file is the artifact of record, referenced in session logs and ADRs.

### Session export

At the end of every session the tutor runs `scripts/export_session.py` automatically. The script reads the raw session JSONL from `~/.claude/projects/`, extracts human/assistant turns, and writes `sessions/session-NNN.txt` — a verbatim, zero-editing transcript numbered sequentially.

---

## Philosophy

Both tutors enforce the same rules:

- **You are never the driver.** You make every architectural decision and write every line of code. The tutor poses questions, surfaces tradeoffs, and reviews what you produce.
- **Every claim is grounded in current docs.** Context7 MCP first, WebSearch + WebFetch as fallback. If a lookup contradicts training data, the lookup wins.
- **One concept at a time.** The tutor doesn't move on until your artifact meets industry standard.
- **Honest review.** Feedback is concrete and specific — not encouragement padding.

---

## Changelog

See [CHANGELOG.md](https://github.com/rgoshen/my_plugins/blob/main/plugins/cs-tutor/CHANGELOG.md).

---

## Source

[github.com/rgoshen/my_plugins/tree/main/plugins/cs-tutor](https://github.com/rgoshen/my_plugins/tree/main/plugins/cs-tutor)
