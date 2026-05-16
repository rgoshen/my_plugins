---
name: New Tutor
about: Propose a new tutor for the cs-tutor plugin
title: "feat(cs-tutor): add <subject>-teach tutor"
labels: "type:new-tutor,plugin:cs-tutor"
assignees: rgoshen
---

**Track:** <!-- CS Foundations | Systems | Software Design | Security | SE Practice | AI & ML | Web -->
**Tier:** <!-- 1 · Core | 2 · Core Systems | 3 · Advanced -->

## Subject
<!-- One sentence describing the subject area -->

## Theory Scope
<!-- Key concepts to cover in depth. Every concept must be grounded in theory — not just how to use it, but why it works. -->

## Project
<!-- What the learner builds across the full course. Must be a real-world project that exercises the theory — each concept chapter produces a deliverable that proves theoretical understanding. -->

## Canonical Sources
<!-- Textbooks, papers, and reference implementations the tutor must look up before teaching each concept. No teaching from memory. -->

## Prerequisites
<!-- Other tutors the learner should complete first -->

## Acceptance Criteria
- [ ] `agents/<subject>-tutor.md` created
- [ ] `skills/<subject>-teach/SKILL.md` created
- [ ] `commands/<subject>-teach.md` created
- [ ] Shared skills (tutor-persona, session-prelude, session-state-manager) wired in via `skills:` frontmatter
- [ ] Theory-first pedagogy enforced — every concept has a project deliverable that proves theoretical understanding
- [ ] `claude plugin validate .` passes
- [ ] README updated with new tutor entry
- [ ] CHANGELOG updated
- [ ] Version bumped in `plugin.json`
