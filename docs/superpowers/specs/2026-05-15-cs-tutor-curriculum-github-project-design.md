# cs-tutor Full Curriculum & GitHub Project Design

- **Date:** 2026-05-15
- **Status:** Approved

---

## Overview

Expand the `cs-tutor` plugin from 2 tutors to a complete university-level computer science and software engineering curriculum of 26 tutors across 6 tracks. Set up a repo-level GitHub Project with a structured board, custom fields, milestones, labels, and issue templates to track all development work across the `my_plugins` repo.

---

## Curriculum Architecture

### Tracks and Tutors (26 total)

| Status | Tutor | Track | Tier |
|--------|-------|-------|------|
| ✅ exists | `arch-teach` | Software Design | — |
| ✅ exists | `pl-teach` | Software Design | — |
| planned | `software-design-teach` | Software Design | 1 |
| planned | `dsa-teach` | CS Foundations | 1 |
| planned | `databases-teach` | Systems | 1 |
| planned | `design-patterns-teach` | Software Design | 1 |
| planned | `system-design-teach` | Systems | 1 |
| planned | `security-fundamentals-teach` | Security | 1 |
| planned | `web-dev-teach` | Web | 1 |
| planned | `linear-algebra-teach` | CS Foundations | 2 |
| planned | `probability-stats-teach` | CS Foundations | 2 |
| planned | `os-teach` | Systems | 2 |
| planned | `networks-teach` | Systems | 2 |
| planned | `distributed-systems-teach` | Systems | 2 |
| planned | `testing-teach` | SE Practice | 2 |
| planned | `appsec-teach` | Security | 2 |
| planned | `devops-teach` | SE Practice | 2 |
| planned | `ml-teach` | AI & ML | 3 |
| planned | `deep-learning-teach` | AI & ML | 3 |
| planned | `llm-teach` | AI & ML | 3 |
| planned | `compilers-teach` | CS Foundations | 3 |
| planned | `computer-org-teach` | CS Foundations | 3 |
| planned | `clean-code-teach` | Software Design | 3 |
| planned | `api-design-teach` | SE Practice | 3 |
| planned | `sre-teach` | SE Practice | 3 |
| planned | `discrete-math-teach` | CS Foundations | 3 |

**24 planned tutors + 2 existing = 26 total**

### Per-Tutor Anatomy

Every tutor is exactly 3 files, following the arch-teach/pl-teach pattern:

```
agents/<subject>-tutor.md        ← WHO: persona, allowed tools, shared skills
skills/<subject>-teach/SKILL.md  ← WHAT: session workflow, roadmap, project loop
commands/<subject>-teach.md      ← ENTRY: user-facing slash command
```

### Shared Infrastructure (Milestone 0 — do before any new tutor)

Three shared skills wire into every tutor via the `skills:` frontmatter in each agent file:

| Skill | Purpose |
|-------|---------|
| `session-state-manager` | ✅ exists — LOAD/SAVE session state, roadmap check-off |
| `tutor-persona` | planned — review structure, communication style, Socratic method, knowledge-sourcing philosophy |
| `session-prelude` | planned — 5-part first-session structure (overview/history/benefits/issues/use cases) |

After Milestone 0, adding any new tutor requires zero changes to shared skills.

### Theory-First Pedagogy

Every tutor drives two parallel threads:

1. **Theory thread** — canonical sources are looked up before each concept. The learner must explain the *why*, not just the *what*, before the tutor moves on. No pattern/algorithm/theorem is taught as a label — it is taught as an answer to a question the learner must first understand.

2. **Project thread** — a single real-world project runs the full course. Each concept is applied to it so theory never floats free of practice. For theory-heavy subjects (Compilers, OS, Discrete Math, Linear Algebra), the project is explicitly designed to exercise the theory in working code or proofs — e.g. the Compilers learner builds a small compiler stage by stage, one theory chapter per deliverable.

The artifact for each concept (diagram, ADR, code, proof, benchmark) must demonstrate theoretical understanding, not just implementation.

---

## GitHub Project Structure

### Project

- **Name:** `my_plugins Development`
- **Scope:** Repo-level — covers all plugins (cs-tutor now, others as added)
- **Default view:** Board

### Board Columns

| Column | Meaning |
|--------|---------|
| Backlog | Defined, not yet started |
| Ready | Fully specced, next to pick up |
| In Progress | Active branch exists |
| In Review | PR open |
| Done | Merged and closed |

### Custom Fields

| Field | Type | Values |
|-------|------|--------|
| **Tier** | Single select | `0 · Infrastructure`, `1 · Core`, `2 · Core Systems`, `3 · Advanced` |
| **Type** | Single select | `New Tutor`, `Bug`, `Enhancement`, `Infrastructure`, `Documentation` |
| **Track** | Single select | `CS Foundations`, `Systems`, `Software Design`, `Security`, `SE Practice`, `AI & ML`, `Web`, `Cross-cutting` |
| **Plugin** | Single select | `cs-tutor`, `ai-engineer`, `repo-wide` |

### Milestones

| Milestone | Scope | Tutors |
|-----------|-------|--------|
| `v0.3.0 · Infrastructure` | Shared skills refactor | tutor-persona, session-prelude |
| `v1.0.0 · Tier 1 Core` | 7 new tutors | Software Design, DSA, Databases, Design Patterns, System Design, Security Fundamentals, Web Dev |
| `v1.5.0 · Tier 2 Core Systems` | 8 new tutors | Linear Algebra, Probability & Stats, OS, Networks, Distributed Systems, Testing, AppSec, DevOps |
| `v2.0.0 · Tier 3 Advanced` | 9 new tutors | ML, Deep Learning, LLMs, Compilers, Computer Org, Clean Code, API Design, SRE, Discrete Math |

### Issue Templates

**New Tutor**
- Subject name & track
- Tier (1/2/3)
- Theory scope — key concepts to cover in depth
- Project idea — what the learner builds across the course
- Canonical sources (textbooks, papers, reference implementations)
- Prerequisites (other tutors required first)
- Acceptance criteria

**Bug Report**
- Which tutor/skill
- Steps to reproduce
- Expected vs actual behavior
- Session log excerpt
- Severity: blocks learning / minor

**Enhancement Request**
- Which tutor/skill
- Problem being solved
- Proposed change
- Why now vs backlog
- Acceptance criteria

### Labels

| Label | Color | Meaning |
|-------|-------|---------|
| `tier:0` | yellow | Infrastructure milestone |
| `tier:1` | blue | Core milestone |
| `tier:2` | purple | Core Systems milestone |
| `tier:3` | green | Advanced milestone |
| `track:foundations` | gray | CS Foundations track |
| `track:systems` | gray | Systems track |
| `track:design` | gray | Software Design track |
| `track:security` | gray | Security track |
| `track:se-practice` | gray | SE Practice track |
| `track:ai-ml` | gray | AI & ML track |
| `track:web` | gray | Web track |
| `type:new-tutor` | blue | New tutor implementation |
| `type:bug` | red | Bug report |
| `type:enhancement` | green | Enhancement to existing tutor |
| `type:infrastructure` | yellow | Shared skill or repo infrastructure |
| `type:documentation` | gray | Docs only |
| `plugin:cs-tutor` | teal | Scoped to cs-tutor plugin |

---

## Build Sequence

1. **Merge PR #6** (drawio fix — already open)
2. **Milestone 0:** `feature/shared-tutor-skills` — tutor-persona + session-prelude (already specced in TODO.md)
3. **Release v0.3.0**
4. **Tier 1 tutors** — one branch per tutor, one PR per tutor
5. **Release v1.0.0**
6. Continue for Tier 2 → v1.5.0, Tier 3 → v2.0.0
