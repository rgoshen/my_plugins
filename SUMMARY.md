# Summary

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
