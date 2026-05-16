# cs-tutor

![Version](https://img.shields.io/badge/version-v0.2.0-blue.svg)
![CI](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Claude Code plugin that provides senior-engineer mentors for learning computer science topics. Currently covers software architecture patterns and programming languages.

---

## Prerequisites

### draw.io (arch-teach only)

The `arch-teach` skill produces native `.drawio` architectural diagrams and opens them automatically. Two components are required:

1. **draw.io desktop app** — the application that renders and edits `.drawio` files.
   [Download draw.io](https://www.drawio.com/) — available for macOS, Windows, and Linux.

2. **draw.io MCP server** — connects Claude Code to the draw.io desktop app so diagrams open automatically during sessions.
   Setup instructions: [draw.io MCP server for Claude Code CLI](https://github.com/jgraph/drawio-mcp/blob/main/skill-cli/README.md)

If neither is installed, diagram files are still written to disk — you can open them manually in the desktop app or at [app.diagrams.net](https://app.diagrams.net). If only the desktop app is installed (no MCP server), diagrams are written to disk but won't auto-open during the session.

---

## What's included

| Component | Name | Purpose |
|---|---|---|
| Agent | `arch-tutor` | Senior engineer persona for architecture patterns tutoring |
| Agent | `pl-tutor` | Senior engineer persona for programming language tutoring |
| Skill | `arch-teach` | Session workflow for architecture tutoring — roadmap, draw.io diagrams, ADRs, session export |
| Skill | `pl-teach` | Session workflow for language tutoring — roadmap, code review, project, session export |
| Command | `/cs-tutor:arch-teach` | Start or resume an architecture tutoring session |
| Command | `/cs-tutor:pl-teach` | Start or resume a language tutoring session |
| Skill | `session-state-manager` | Shared LOAD/SAVE handler — used internally by all teach skills; not invoked directly |
| Script | `scripts/export_session.py` | Auto-export verbatim session transcript to `sessions/session-NNN.txt` |

---

## Installation

```
/plugin marketplace add rgoshen/my_plugins
/plugin install cs-tutor@my-plugins
```

---

## Usage

Start an architecture patterns session:
```
/cs-tutor:arch-teach
/cs-tutor:arch-teach hexagonal
/cs-tutor:arch-teach event-driven
```

Start a programming language session:
```
/cs-tutor:pl-teach
/cs-tutor:pl-teach Rust
/cs-tutor:pl-teach Go
```

Run these commands from the repo where you want session files to live.

---

## How sessions work

Both tutors are stateful and manage the same file set in your working directory:

| File | Purpose |
|---|---|
| `lastsession.md` | Rolling log, newest entry on top — the tutor resumes from here |
| `architecture-roadmap.md` / `language-roadmap.md` | Curriculum checklist, checked off as concepts land |
| `teaching-plan.md` | Project overview + user stories; every concept produces a deliverable |
| `sessions/session-NNN.txt` | Verbatim transcript of each completed session, auto-exported |

### Kickoff sequence (first session)

1. Confirm the language or architecture focus
2. Build or import a curriculum roadmap
3. Design a practice project with a full **project overview** (what, why, tech stack, layout, definition of done)
4. Write user stories

### First session prelude

Before the first concept, the tutor covers five things: **overview, history, benefits, issues, and use cases** of the language or the discipline of architecture patterns. This frames everything that follows.

### Architectural diagrams (arch-teach)

For each pattern, the tutor produces a native `.drawio` diagram — component maps, C4 containers, sequence diagrams, data flow. Diagrams open automatically when the draw.io desktop app and MCP server are both installed (see Prerequisites); otherwise the `.drawio` file is written to disk for manual opening.

### Session export

At the end of every session the tutor automatically runs `scripts/export_session.py`, which reads the session JSONL and writes a verbatim numbered transcript to `sessions/session-NNN.txt`.

---

## Adding a new tutor

cs-tutor is designed to grow into a full CS curriculum. All session state logic lives in the shared `session-state-manager` skill — new tutors plug into it with two parameters and need not duplicate any load/save code.

### Checklist

1. **Agent** — create `agents/<subject>-tutor.md`. Include these in the frontmatter:
   ```yaml
   skills:
     - <subject>-teach
     - session-state-manager
   memory: project
   ```

2. **Teach skill** — create `skills/<subject>-teach/SKILL.md`. In **Step 1**, reference LOAD:
   ```
   Follow the LOAD phase defined in the session-state-manager skill
   (already loaded in your context) with:
   - roadmap-file: <subject>-roadmap.md
   ```
   In **Step 4**, reference SAVE:
   ```
   Follow the SAVE phase defined in the session-state-manager skill
   (already loaded in your context) with:
   - roadmap-file: <subject>-roadmap.md
   - output-label: <label>   # e.g. Exercises, Code, Problems, Projects
   ```

3. **Command** — create `commands/<subject>-teach.md` as a thin entry point that invokes the agent.

4. **Session files** — document in your teach skill's "Working files" section which roadmap file the subject uses (e.g., `data-structures-roadmap.md`).

### session-state-manager parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `roadmap-file` | Yes | Roadmap filename in the working directory |
| `output-label` | SAVE only | Label for the artifact/work field in the session log |

`session-state-manager` itself never needs to change when a new tutor is added.

---

## Philosophy

Both tutors enforce a strict mentor-not-driver model:

- You make every decision and write every line of code
- Every claim is grounded in current documentation (Context7 MCP first, WebSearch + WebFetch as fallback)
- Sessions are grounded in a real project, not abstract drills
- Review is honest — industry standard, not encouragement

---

## License

MIT
