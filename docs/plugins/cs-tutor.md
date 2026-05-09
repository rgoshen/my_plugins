---
title: cs-tutor
layout: default
parent: Plugins
nav_order: 1
---

# cs-tutor

![Version](https://img.shields.io/badge/version-v0.0.1-blue.svg)
![Build](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Senior-engineer mentors for computer science learning — architecture patterns and programming languages. Follows a strict mentor-not-driver model: you make every decision, you write every line of code.
{: .fs-5 }

---

## Install

```
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
| `arch-teach` | Session workflow for architecture tutoring — roadmap, ADRs, design reviews, session logs |
| `pl-teach` | Session workflow for language tutoring — roadmap, code review, practice project, session logs |

---

## Usage

### Start an architecture session

```
/cs-tutor:arch-teach
```

Or with a starting focus:

```
/cs-tutor:arch-teach hexagonal
/cs-tutor:arch-teach event-driven
/cs-tutor:arch-teach microservices boundaries
```

### Start a language session

```
/cs-tutor:pl-teach
```

Or skip the "what language?" question:

```
/cs-tutor:pl-teach Rust
/cs-tutor:pl-teach Go
/cs-tutor:pl-teach OCaml
```

---

## How sessions work

Both tutors are stateful. Run the command from the repo where you want session files to live. The skill manages three files automatically:

| File | Purpose |
|---|---|
| `lastsession.md` | Rolling session log, newest entry on top. The tutor resumes from here. |
| `architecture-roadmap.md` / `language-roadmap.md` | Curriculum checklist, checked off as concepts land. |
| `teaching-plan.md` | Practice project user stories. Every concept produces a deliverable that ships into the current story. |

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
