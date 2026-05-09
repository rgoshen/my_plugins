# Summary

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
