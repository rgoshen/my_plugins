# cs-tutor

![Version](https://img.shields.io/badge/version-v0.0.2-blue.svg)
![Build](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Claude Code plugin that provides senior-engineer mentors for learning computer science topics. Currently covers software architecture patterns and programming languages.

## What's included

| Component | Name | Purpose |
|---|---|---|
| Agent | `arch-tutor` | Senior engineer persona for architecture patterns tutoring |
| Agent | `pl-tutor` | Senior engineer persona for programming language tutoring |
| Skill | `arch-teach` | Session workflow for architecture tutoring (roadmap, ADRs, design reviews) |
| Skill | `pl-teach` | Session workflow for language tutoring (roadmap, code review, project) |
| Command | `/cs-tutor:arch-teach` | Start or resume an architecture tutoring session |
| Command | `/cs-tutor:pl-teach` | Start or resume a language tutoring session |

## Installation

```
/plugin marketplace add rgoshen/my_plugins
/plugin install cs-tutor@my-plugins
```

## Usage

Start an architecture patterns session:
```
/cs-tutor:arch-teach
/cs-tutor:arch-teach hexagonal
```

Start a programming language session:
```
/cs-tutor:pl-teach
/cs-tutor:pl-teach Rust
```

Sessions are stateful. Each tutor maintains:
- `lastsession.md` — rolling session log (newest entry on top)
- `architecture-roadmap.md` / `language-roadmap.md` — curriculum checklist
- `teaching-plan.md` — practice project user stories

Run these commands from the repo where you want the session files to live.

## Philosophy

Both tutors follow a strict mentor-not-driver model:
- You make every decision and write every line of code
- Every claim is grounded in current documentation (no training-data guesses)
- Sessions are grounded in a real project, not abstract drills
- Review is honest — industry standard, not encouragement

## License

MIT
