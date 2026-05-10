# TODO

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
