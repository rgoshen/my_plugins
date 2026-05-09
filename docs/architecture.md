---
title: Architecture
layout: default
nav_order: 3
---

# Architecture

## Overview

This repository is a Claude Code plugin marketplace — a git-hosted catalog that users add with `/plugin marketplace add rgoshen/my_plugins` and install individual plugins from.

## Repository layout

```
my_plugins/
├── .claude-plugin/
│   └── marketplace.json     # The marketplace registry
├── plugins/
│   └── <plugin-name>/       # One directory per plugin
│       ├── .claude-plugin/
│       │   └── plugin.json  # Plugin manifest
│       ├── agents/          # Agent personas (.md with YAML frontmatter)
│       ├── skills/          # Workflow skills (<name>/SKILL.md)
│       ├── commands/        # User-facing slash commands (.md)
│       └── README.md
└── .github/
    └── workflows/
        └── validate.yml     # CI validation
```

## Plugin component model

Each plugin follows a layered model:

```
User
  └── invokes Command (/cs-tutor:arch-teach)
        └── invokes Agent (arch-tutor)
              └── uses Skill (arch-teach) for session workflow
```

**Agent** — defines WHO: persona, tools, model, memory, and which skills it carries (`skills:` frontmatter). Agents are the primary entry point.

**Skill** — defines WHAT: the workflow, session state, and instructions Claude follows. Skills must be self-contained; they must not reference agent files by path.

**Command** — a thin `.md` file that describes the entry point for users. Invokes the appropriate agent.

This separation means:
- Personas can be updated without touching workflow logic
- Workflows can be tested independently of personas
- Users get a consistent slash command interface regardless of internal structure

## Versioning

Plugin versions are resolved from `plugin.json` → `marketplace.json` entry → git commit SHA (in that order). This repo omits explicit versions in `marketplace.json` entries; `plugin.json` is the single source of truth per plugin.

## Distribution

Claude Code clones this repo when users run `/plugin marketplace add rgoshen/my_plugins`. Plugins with `source: "./plugins/<name>"` are resolved relative to the marketplace root and sparse-cloned into the user's plugin cache at `~/.claude/plugins/cache/`.
