# TODO

## [2026-05-09] Fix: Marketplace & Plugin Issues

**Objective:**
Resolve all identified issues in the my_plugins marketplace repo so it is functionally correct and ready for public use.

**Approach:**
Fix issues in order of severity — functional bugs first, then missing structure, then CI/CD.

**Tests:**
- `claude plugin validate .` passes with zero errors after each fix
- Agent skills can reference agents without hardcoded absolute paths

**Risks & Tradeoffs:**
- Changing agent references in skills changes the UX contract for anyone currently using the plugin directly (not via marketplace install)

---

### Priority 1 — Functional Bugs
- [x] Fix typo in `marketplace.json`: `my-pluigins` → `my-plugins`
- [x] Add `description` to `marketplace.json` (fixes validator warning)
- [x] Fix hardcoded `~/.claude/agents/` path in `skills/arch-teach/SKILL.md`
- [x] Fix hardcoded `~/.claude/agents/` path in `skills/pl-teach/SKILL.md`
- [x] Add `commands/` with slash command entry points that invoke agents

### Priority 2 — Missing Required Files
- [x] Add `plugins/cs-tutor/README.md`
- [x] Add root `README.md`
- [x] Add `LICENSE`
- [x] Add `CONTRIBUTING.md`
- [x] Add `ARCHITECTURE.md`
- [x] Update `.gitignore` with dev entries

### Priority 3 — CI/CD
- [x] Create `.github/workflows/validate.yml`

### Priority 4 — Discovery / Metadata
- [ ] Add `category`, `tags`, `homepage` to cs-tutor plugin entry in `marketplace.json`
