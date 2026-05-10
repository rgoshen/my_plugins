---
name: session-state-manager
description: Shared session state handler for cs-tutor sessions. Saves and loads lastsession.md, roadmap, and teaching-plan to preserve context across relaunches. Used internally by arch-teach and pl-teach; not invoked directly by users.
allowed-tools: Read Write Glob Bash(date *) Bash(python3 *)
---

# session-state-manager

Shared state persistence for cs-tutor sessions. The calling skill tells you which **mode** you're in — `arch` or `pl` — before delegating. Mode determines which roadmap file to read and which log entry template to use.

## File map

| File | arch mode | pl mode |
|------|-----------|---------|
| Session log | `lastsession.md` | `lastsession.md` |
| Roadmap | `architecture-roadmap.md` | `language-roadmap.md` |
| Teaching plan | `teaching-plan.md` | `teaching-plan.md` |

---

## LOAD — restore session state

Run at the start of every session when directed by the calling skill.

1. Check for `lastsession.md` in the working directory.

2. **If found:**
   a. Read the most recent entry — the top block, from the first `## YYYY-MM-DD` heading down to (but not including) the next such heading, or end of file.
   b. Read the roadmap file for this mode. Find the first unchecked item (`- [ ]`).
   c. Read `teaching-plan.md`. Identify the active user story.
   d. In **one message**, tell the user: what was covered last, what comes next on the roadmap, and which story is active. Three sentences maximum.
   e. **STOP. Wait for the user to confirm before proceeding.** They may want to revisit something or jump ahead.
   f. Report `SESSION_RESUMED = true` to the calling skill. Do NOT run any kickoff sequence.

3. **If not found:**
   - Report `SESSION_RESUMED = false`. The calling skill runs its kickoff sequence.

---

## SAVE — persist session state

Run at the end of every session when directed by the calling skill. All four steps are mandatory — none may be skipped.

### Step 1 — Update roadmap

Open the roadmap file for this mode. For each item the user completed solidly this session, change `- [ ]` to `- [x]`. Items started but not fully landed: leave unchecked and flag in the log entry below.

### Step 2 — Prepend to lastsession.md

Get today's date: `date +%Y-%m-%d`.

Write a new entry at the **top** of `lastsession.md`. Prepend — do not append — newest entry on top.

**arch mode:**
```markdown
## YYYY-MM-DD

**Covered:** <patterns the user completed this session, briefly>

**Artifacts:** <which user story / files were touched — diagrams, ADRs, code>

**Next:** <the very next pattern from the roadmap, plus any unfinished thread>

**Notes:** <tradeoff insight, confusion, or real-world parallel worth remembering>
```

**pl mode:**
```markdown
## YYYY-MM-DD

**Covered:** <concepts the user completed this session, briefly>

**Code:** <which user story / files were worked on>

**Next:** <the very next concept from the roadmap, plus any unfinished thread>

**Notes:** <confusion, pattern they liked, or tooling decision worth remembering>
```

### Step 3 — Export transcript

Use Glob to find `export_session.py` inside `~/.claude/plugins/cache/cs-tutor*/scripts/`. Run it with `python3 <found-path>`. The script writes the verbatim transcript to `sessions/session-NNN.txt` (auto-numbered) and prints the output path. Tell the user where it was saved.

### Step 4 — Confirm

One sentence: the log entry date, how many roadmap items were checked off, and the transcript path. Don't pad.
