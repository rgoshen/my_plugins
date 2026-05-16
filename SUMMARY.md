# Summary

## [2026-05-16 03:45] Commit Summary

**Change Type:** Feature
**Scope:** cs-tutor / agents / skills

**Summary:**
Created `skills/tutor-persona/SKILL.md` and extracted four shared content blocks from both `arch-tutor.md` and `pl-tutor.md`: communication style, 4-part review structure, knowledge-sourcing philosophy (abstract principle), and shared "what you do not do" items. Both agent files now list `tutor-persona` in `skills:` frontmatter; extracted content removed from each.

**Rationale:**
Eliminates duplicated content across two agent files. At two tutors the cost is low; extracting now means any third tutor added in the future inherits all shared behavior for free by listing the skill — no copy-paste required. Subject-specific content (personas, domain methodology, lookup source priority, domain-specific prohibitions) remains in each agent.

**References:**
- TODO.md: [2026-05-11] Refactor: extract tutor-persona and session-prelude shared skills
- Issue: #7

## [2026-05-15 17:19] Commit Summary

**Change Type:** Fix
**Scope:** cs-tutor plugin — drawio integration

**Summary:**
Removed `mcpServers.drawio` from `plugin.json` and replaced the direct `mcp__drawio__*` tool calls in `arch-teach/SKILL.md` with an invocation of the global `drawio` skill. Updated `allowed-tools` accordingly.

**Rationale:**
The drawio MCP server declaration in `plugin.json` caused a `/doctor` duplicate warning for users who already have the drawio MCP configured globally. More importantly, the approach was wrong for public distribution: the plugin should not depend on the MCP server at all — the global `drawio` skill achieves the same result using the Write tool and the draw.io desktop CLI, with graceful fallback if the app is not installed.

**References:**
- Branch: feature/drawio-skill-integration

## [2026-05-11] Commit Summary

**Change Type:** Docs
**Scope:** cs-tutor CHANGELOG — v0.2.0 release notes

**Summary:**
Added `## [0.2.0]` section to CHANGELOG.md with release notes covering the session-state-manager skill, README authoring guide, skill language fix, and agent updates.

**Rationale:**
Release workflow reads CHANGELOG.md to populate the GitHub Release notes on merge to main.

**References:**
- TODO.md: [2026-05-11] Feature: session-state-manager shared skill

---

## [2026-05-11] Commit Summary

**Change Type:** Docs
**Scope:** TODO.md — planned refactor annotation

**Summary:**
Added a detailed execution plan to TODO.md for the next refactor: extracting `tutor-persona` and `session-prelude` shared skills from the cs-tutor plugin. Includes exact files to create/edit, content to move, validation steps, and version bump target (v0.3.0). Also saved a project memory entry so the next session auto-surfaces this work.

**Rationale:**
Four duplication patterns were identified across arch-tutor/pl-tutor and arch-teach/pl-teach. Annotating the plan now (before closing this PR) ensures the next agent session has full context to execute without reconstruction.

**References:**
- TODO.md: [2026-05-11] Refactor: extract tutor-persona and session-prelude shared skills

---

## [2026-05-11] Commit Summary

**Change Type:** Fix
**Scope:** cs-tutor — arch-teach, pl-teach, README (clarify skill-context language)

**Summary:**
Replaced all "delegate to skill" phrasing with "follow the phase defined in skill (already loaded in your context)" across arch-teach Step 1 and 4, pl-teach Step 1 and 4, and the new-tutor checklist in the README. "Delegate" implied a formal call mechanism; the correct model is that all listed skills are loaded into the agent's context simultaneously and the teach skill directs the LLM to follow the relevant section.

**Rationale:**
Accurate language prevents future authors from expecting a dynamic dispatch mechanism that does not exist. Skills are loaded as context, not called as functions.

**References:**
- TODO.md: [2026-05-11] Feature: session-state-manager shared skill

---

## [2026-05-11] Commit Summary

**Change Type:** Docs
**Scope:** cs-tutor README + root CONTRIBUTING.md — tutor authoring convention

**Summary:**
Added "Adding a new tutor" section to `plugins/cs-tutor/README.md` documenting the session-state-manager parameter contract, new tutor checklist, and parameter reference table. Updated CONTRIBUTING.md to point to this guide. Fixed version badge in README from v0.1.0 to v0.2.0. Added `session-state-manager` to the component table.

**Rationale:**
The two-parameter convention (`roadmap-file`, `output-label`) was only discoverable by reading the skill source. For a growing curriculum, contributors (human or AI) need the contract documented at the point of authoring. The checklist format mirrors the project CLAUDE.md "Definition of Ready" pattern.

**References:**
- TODO.md: [2026-05-11] Feature: session-state-manager shared skill

---

## [2026-05-11] Commit Summary

**Change Type:** Refactor
**Scope:** cs-tutor — session-state-manager (generalize for multi-tutor ecosystem)

**Summary:**
Made `session-state-manager` fully generic by removing all hardcoded arch/pl mode handling. The skill now accepts `roadmap-file` and `output-label` parameters from the calling teach skill, and uses a single unified log entry template with a parameterized `Output` field. Both `arch-teach` and `pl-teach` delegation lines updated to pass explicit parameters.

**Rationale:**
The first implementation hardcoded two modes (arch/pl), meaning every new tutor would require editing the shared skill. With a full CS curriculum planned, the skill must be open for extension without modification: each teach skill passes its own `roadmap-file` and `output-label`, and `session-state-manager` stays generic forever. The unified `{{output-label}}` template keeps the log format consistent across all tutors while preserving per-tutor vocabulary.

**References:**
- TODO.md: [2026-05-11] Feature: session-state-manager shared skill

---

## [2026-05-11] Commit Summary

**Change Type:** Feature
**Scope:** cs-tutor — session-state-manager skill

**Summary:**
Added a shared `session-state-manager` skill that centralizes session load/save logic previously duplicated across `arch-teach` and `pl-teach`. Both teaching skills now delegate Step 1 (resume check) and Step 4 (end-of-session save) to this shared skill via a one-line reference. Both tutor agents updated to include the new skill in their `skills:` list. Plugin bumped to v0.2.0.

**Rationale:**
Session load/save was copy-pasted between the two teach skills with minor variations, creating a maintenance hazard. A single source of truth makes the behavior consistent across relaunches, easier to fix in one place, and extensible if additional tutor modes are added later. Separate log entry templates (arch: `Artifacts` field; pl: `Code` field) kept distinct to preserve per-mode self-documentation.

**References:**
- TODO.md: [2026-05-11] Feature: session-state-manager shared skill

---

## [2026-05-09 21:15] Commit Summary

**Change Type:** Fix
**Scope:** cs-tutor — arch-teach skill Phase 1

**Summary:**
Made the pattern catalogue conditional on `$ARGUMENTS` being empty. When no argument is passed and there is no `lastsession.md`, the tutor now shows the full pattern list ordered from foundational to advanced before asking any questions. When `$ARGUMENTS` is non-empty, the catalogue is skipped and the tutor proposes the argument as the starting focus for confirmation.

**Rationale:**
A learner who hasn't specified a focus area cannot meaningfully answer "what patterns do you want to study?" without first knowing what patterns exist. The foundational-first ordering (Layered → MVC → Hexagonal → Clean → ...) also serves as a natural default curriculum suggestion.

---

## [2026-05-09 21:00] Commit Summary

**Change Type:** Fix
**Scope:** cs-tutor — arch-teach skill kickoff sequence

**Summary:**
Rewrote Step 2 (Kickoff) of the arch-teach skill to fix two bugs observed in session transcripts: (1) the agent inferred the topic/pattern from the working directory name instead of asking the user directly; (2) the agent rolled into lesson content immediately after the user chose a pattern without first writing the required files or issuing the mandatory stop.

**Rationale:**
The original Step 2 contained the correct rules, but as prose paragraphs they were easy for the model to skip. The fix restructures Step 2 into four named phases (Phase 1–4), each ending with an explicit **STOP** directive and a condition that must be satisfied before the next phase begins. The no-assumption prohibition is now a blockquote at the top of the step, with a concrete example (directory named `layered-architecture`), making it impossible to miss. The final kickoff gate is now labeled **HARD STOP** and includes the exact question the model must ask before proceeding to the session loop.

**Bug Fix Context:**
Root cause: LLMs treat soft prose directives ("Then stop") as advisory when surrounded by flowing instructions. Hard-labeled gates with explicit wait conditions and named phases enforce the sequence structurally.

**References:**
- Session transcript: 2026-05-09-194852-command-messagecs-tutorarch-teach...

## [2026-05-09 23:55] Commit Summary

**Change Type:** Fix  
**Scope:** CI — release workflow, badges

**Summary:**
Fixed `set -e` trap in release workflow: `[[ condition ]] && echo` pattern exits with code 1 when the condition is false, killing the job even after work completed successfully. Replaced with `if/fi`. Also initialized `NOTES=""` before the conditional block to prevent `set -u` from tripping on an unset variable. Renamed "Build" badge to "CI" in plugin README and docs to accurately reflect that the workflow covers both plugin validation and pytest tests.

**Rationale:**
The v0.1.0 release succeeded (tag pushed, GitHub Release created) but CI reported failure due to the `&&` exit-code leak under `set -e`. Badge rename is cosmetic but accurate — the validate.yml workflow covers both jobs.

**References:**
- PR: #3 (feature/fix-release-set-e-trap)

---

## [2026-05-09 23:30] Commit Summary

**Change Type:** Feature + Fix  
**Scope:** cs-tutor plugin — release workflow, v0.1.0 bump

**Summary:**
Fixed the release workflow, which was committing version bumps directly to `main` — blocked by branch protection, leaving orphaned tags. Redesigned the workflow to be tag-only: version bumps go through PRs, CI only reads plugin.json, tags HEAD, and creates GitHub Releases. Bumped cs-tutor to v0.1.0 with CHANGELOG, badge updates, and proper docs alignment.

**Rationale:**
The original `git push origin main --tags` caused a race: tags pushed successfully (leaving an orphaned `cs-tutor-v0.1.0`) while the branch push failed with GH006. Subsequent runs hit "tag already exists" and crashed. Deleting the orphaned tag and redesigning the workflow eliminates both failure modes permanently.

**References:**
- PR: #2 (feature/fix-release-workflow-v0.1.0)

---

## [2026-05-09 22:15] Commit Summary

**Change Type:** Feature  
**Scope:** cs-tutor plugin — skills, scripts, CI, docs, plugin manifest

**Summary:**
Major cs-tutor enhancement: expanded first-session preludes for both tutors to five mandatory items (overview, history, benefits, issues, use cases); added structured project overview to kickoff; integrated draw.io diagram generation into arch-teach with graceful fallback; added auto-export session transcript via `export_session.py` at end of every session; bundled `@drawio/mcp` MCP server in plugin manifest; added 18-test pytest suite for the export script; added pytest CI job to validate workflow; updated all docs and README badges.

**Rationale:**
The tutors were skipping the language/architecture overview on first sessions, giving users no frame for the curriculum. The project overview was implicit and inconsistent. draw.io diagrams were proposed but not integrated. Session transcript export required a user-run `\export` command which is easy to forget. Bundling the MCP server removes a setup step for users. All changes were validated against the plugin architecture conventions in CLAUDE.md.

**References:**
- PR: #1 (feature/improve-tutor-skills)
- TODO.md: Improve cs-tutor tutor skills

---

## [2026-05-09 21:45] Commit Summary

**Change Type:** Fix  
**Scope:** cs-tutor plugin manifest

**Summary:**
Fixed plugin.json `name` field from `"Computer Science Tutor"` to `"cs-tutor"` (kebab-case required by runtime). Plugin installation was failing with "Plugin name cannot contain spaces."

**Rationale:**
The Claude Code plugin runtime validates that plugin names are kebab-case. The manifest had a human-readable display name instead. The fix is a one-field change; the release workflow auto-bumped to v0.0.3.

**References:**
- TODO.md: Fix: Plugin installation failures

---

## [2026-05-09 00:00] Commit Summary

**Change Type:** Fix + Feature  
**Scope:** Marketplace registry, cs-tutor plugin, CI/CD

**Summary:**
Fixed all critical issues identified in the initial marketplace audit: corrected the marketplace name typo, fixed the broken agent-path references in skills, restructured the plugin to follow the correct agent→skill architecture, and added all missing project files and CI validation.

**Rationale:**
The skills were referencing agent files by absolute path (`~/.claude/agents/`), which breaks when the plugin is installed from the marketplace (files land in the plugin cache, not the global agents directory). The root cause was an architectural inversion — skills were trying to activate agents, when the correct model is agents invoking skills via their `skills:` frontmatter. Removing the "Activate the persona" sections makes skills self-contained workflow instructions, which is their proper role. Commands were added as the user-facing entry points that invoke agents.

**References:**
- TODO.md: Fix: Marketplace & Plugin Issues
- Docs: https://code.claude.com/docs/en/plugins-reference
- Docs: https://code.claude.com/docs/en/plugin-marketplaces
