---
name: session-state-manager
description: Use when a cs-tutor teach skill needs to persist or restore session state (lastsession.md, roadmap, teaching-plan) across conversations. Internal helper — not invoked directly by users; parameters supplied by the calling skill.
allowed-tools: Read Write Glob Bash(date *) Bash(python3 *)
---

# session-state-manager

Generic state persistence for cs-tutor sessions. The calling teach skill supplies all tutor-specific parameters — this skill contains no hardcoded knowledge of any particular tutor or subject area.

## Parameters (supplied by calling skill)

| Parameter | Description | Example |
|-----------|-------------|---------|
| `roadmap-file` | Roadmap filename in the working directory | `architecture-roadmap.md`, `language-roadmap.md`, `data-structures-roadmap.md` |
| `output-label` | Label for the artifact/work field in the session log | `Artifacts`, `Code`, `Exercises` |

---

## LOAD — restore session state

Run at the start of every session when directed by the calling skill.

1. Check for `lastsession.md` in the working directory.

2. **If found:**
   a. Read the most recent entry — the top block, from the first `## YYYY-MM-DD` heading down to (but not including) the next such heading, or end of file.
   b. Read the roadmap file named by `roadmap-file`. Find the first unchecked item (`- [ ]`).
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

Open `roadmap-file`. For each item the user completed solidly this session, change `- [ ]` to `- [x]`. Items started but not fully landed: leave unchecked and flag in the log entry below.

### Step 2 — Prepend to lastsession.md

Get today's date: `date +%Y-%m-%d`.

Write a new entry at the **top** of `lastsession.md`. Prepend — do not append — newest entry on top. Use `output-label` as the field name for the artifact/work line.

```markdown
## YYYY-MM-DD

**Covered:** <topics completed this session, briefly>

**{{output-label}}:** <which user story / files were touched this session>

**Next:** <the very next item from the roadmap, plus any unfinished thread>

**Notes:** <insight, confusion, or decision worth remembering>
```

Replace `{{output-label}}` with the value supplied by the calling skill (e.g., `Artifacts`, `Code`, `Exercises`).

### Step 3 — Export transcript

Use Glob to find `export_session.py` inside `~/.claude/plugins/cache/cs-tutor*/scripts/`. Run it with `python3 <found-path>`. The script writes the verbatim transcript to `sessions/session-NNN.txt` (auto-numbered) and prints the output path. Tell the user where it was saved.

### Step 4 — Confirm

One sentence: the log entry date, how many roadmap items were checked off, and the transcript path. Don't pad.
