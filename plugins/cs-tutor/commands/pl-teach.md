---
description: Start or resume a programming language tutoring session with the pl-tutor agent
argument-hint: "[language]"
---

Invoke the `pl-tutor` agent to run a programming language tutoring session.

The pl-tutor agent will use the pl-teach skill to manage the session — resuming from `lastsession.md` if one exists, or running the kickoff sequence to choose a language, build a roadmap, and design a practice project.

Pass the language name as an argument to skip the "what language?" question on first run (e.g., "Rust", "Go", "OCaml").
