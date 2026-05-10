# TODO

## [2026-05-11] Refactor: extract tutor-persona and session-prelude shared skills

**Status:** Planned — do NOT include in PR #5 (feature/session-state-manager). New branch required: `feature/shared-tutor-skills`.

**Objective:**
Eliminate duplication across cs-tutor agent and teach skill files by extracting two new shared skills. Required before adding a third tutor — otherwise every new tutor copies the same boilerplate.

**What to extract:**

### 1. `plugins/cs-tutor/skills/tutor-persona/SKILL.md`

Pull from both `agents/arch-tutor.md` and `agents/pl-tutor.md`:
- **Review structure** (4-part format: Strengths → Required changes → Stylistic suggestions → What to look up) — currently verbatim in both agent files
- **Communication style** (Direct, Concise, Socratic, No emoji, Look it up when you don't know) — nearly identical in both
- **"What you do not do" list** (don't do the user's work, don't skip lookups, don't move on until solid) — same principle in both
- **Knowledge sourcing philosophy** (never teach from memory, Context7 first, WebSearch fallback, trust doc over memory, model the habit)

After extraction, each agent file keeps only its unique persona: subject domain, core philosophy framing ("you are never the architect of record" vs "you are never the driver"), and subject-specific review criteria (diagrams/ADRs for arch; code/PR standards for pl).

Add `tutor-persona` to `skills:` in both `arch-tutor.md` and `pl-tutor.md`.

### 2. `plugins/cs-tutor/skills/session-prelude/SKILL.md`

Pull from both `skills/arch-teach/SKILL.md` and `skills/pl-teach/SKILL.md`:
- The 5-item first-session structure: Overview → History → Benefits → Issues → Use Cases
- Framing: tight (5-10 min), happens once only, don't repeat on resume, encourage questions, bridge into first topic
- Subject-specific content is NOT in this skill — the calling teach skill provides it via a parameter or inline note

After extraction, each teach skill's "First session prelude" section becomes a single line:
`Follow the session-prelude skill (already loaded in your context). Subject: <subject name>.`

Add `session-prelude` to `skills:` in both `arch-tutor.md` and `pl-tutor.md`.

**Files to change:**
- CREATE `plugins/cs-tutor/skills/tutor-persona/SKILL.md`
- CREATE `plugins/cs-tutor/skills/session-prelude/SKILL.md`
- EDIT `plugins/cs-tutor/agents/arch-tutor.md` — add both skills, remove extracted content
- EDIT `plugins/cs-tutor/agents/pl-tutor.md` — add both skills, remove extracted content
- EDIT `plugins/cs-tutor/skills/arch-teach/SKILL.md` — replace prelude block with single reference line
- EDIT `plugins/cs-tutor/skills/pl-teach/SKILL.md` — replace prelude block with single reference line
- EDIT `plugins/cs-tutor/README.md` — add both skills to component table, update new-tutor checklist
- EDIT `plugins/cs-tutor/.claude-plugin/plugin.json` — bump to v0.3.0
- EDIT `SUMMARY.md` — add entry before commit

**Validation:**
- `claude plugin validate .` must pass
- Both agent files must still contain enough unique content to be meaningful personas
- Both teach skills must still flow correctly end-to-end after the prelude block is replaced

**Rationale:**
Four patterns of duplication identified across arch-tutor/pl-tutor agents and arch-teach/pl-teach skills. Extracting now (before a third tutor is added) keeps the cost low. After extraction, adding any new tutor requires zero changes to tutor-persona or session-prelude — they inherit everything shared automatically.

---

## [2026-05-11] Feature: session-state-manager shared skill

**Objective:**
Centralize the session load/save logic that is currently duplicated in `arch-teach` and `pl-teach`.
Both skills do near-identical work in Step 1 (resume check) and Step 4 (end-of-session save);
a shared `session-state-manager` skill eliminates that duplication and ensures consistent behavior
across relaunches.

**Approach:**
1. Create `plugins/cs-tutor/skills/session-state-manager/SKILL.md` with a LOAD phase and a SAVE phase.
2. Slim `arch-teach` Steps 1 and 4 to a one-line delegation to session-state-manager (arch mode).
3. Slim `pl-teach` Steps 1 and 4 to a one-line delegation to session-state-manager (pl mode).
4. Add `session-state-manager` to the `skills:` list in both `arch-tutor.md` and `pl-tutor.md`.
5. Bump plugin version to 0.2.0.
6. Update SUMMARY.md and commit on `feature/session-state-manager`.

**Tests:**
No executable tests (skill files are markdown instructions, not code). Validation:
- `claude plugin validate .` passes with no errors.
- Both teach skills reference the session-state-manager delegation clearly.
- Both agent files include session-state-manager in their skills lists.

**Risks & Tradeoffs:**
- Skill-to-skill delegation is done via natural-language reference, not a formal call mechanism;
  the LLM must correctly interpret "delegate to session-state-manager, arch mode".
- Separate log entry templates (arch vs pl) kept distinct to preserve clarity; a unified template
  could be simpler but sacrifices self-documentation.
