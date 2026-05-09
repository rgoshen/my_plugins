# CLAUDE.md — my_plugins Marketplace

This repo is a personal Claude Code plugin marketplace. It contains a `marketplace.json` registry and one or more plugins under `plugins/`. All engineering rules from the global `~/.claude/CLAUDE.md` apply; this file adds project-specific conventions on top.

---

## Repo Structure

```
my_plugins/
├── .claude-plugin/
│   └── marketplace.json        # Marketplace registry (the catalog)
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json     # Per-plugin manifest
│       ├── agents/             # Agent .md files
│       ├── skills/
│       │   └── <skill-name>/
│       │       └── SKILL.md
│       ├── commands/           # Slash command .md files (optional)
│       ├── hooks/              # hooks.json (optional)
│       └── README.md
├── .github/
│   └── workflows/
│       └── validate.yml        # CI: runs `claude plugin validate .`
├── CLAUDE.md                   # This file
├── README.md
├── CONTRIBUTING.md
├── ARCHITECTURE.md
├── LICENSE
├── TODO.md
└── SUMMARY.md
```

---

## Plugin Conventions

### Agents are entry points; skills are workflows

The correct component model is:

```
User → Command (/plugin:skill-name) → Agent (persona) → Skill (workflow)
```

- **Agent** — defines WHO: the persona, tools, model, memory, and which skills it carries via `skills:` frontmatter
- **Skill** — defines WHAT: the session workflow and instructions Claude follows; must be self-contained
- **Command** — a thin `.md` in `commands/` that invokes the agent; the user-facing slash command entry point

**Skills must never read agent files by path.** When a user installs a plugin, all files are copied to a cache directory (`~/.claude/plugins/cache/`). Paths like `~/.claude/agents/` will not exist. More importantly, if the agent invoked the skill, the persona is *already active* — the skill reading the agent file would be a redundant circular reference.

**Wrong** (broken path + circular):
```markdown
Read `~/.claude/agents/arch-tutor.md` and adopt that persona.
```

**Right** (skill is pure workflow; persona comes from the agent that invoked it):
```markdown
## Step 1: Resume or kickoff?
...
```

### Never hardcode `~/.claude/` paths in hooks or MCP configs either
Use `${CLAUDE_PLUGIN_ROOT}` for paths within the plugin in hook commands and MCP server configs.

### `marketplace.json` rules
- `name` must be kebab-case, no spaces, no uppercase (e.g., `my-plugins`)
- Each plugin entry requires `name` and `source` at minimum
- Do not set `version` in both `plugin.json` and `marketplace.json` — `plugin.json` wins silently and will mask marketplace versions
- Omitting `version` is valid and recommended for active development; Claude Code uses the git commit SHA

### `plugin.json` rules
- Required fields: `name`, `description`, `version`
- Optional but encouraged: `author`, `repository`, `license`, `keywords`
- The `$schema` field is accepted and ignored at runtime — keep it for editor autocomplete

### Skill `SKILL.md` frontmatter required fields
- `name` — kebab-case identifier
- `description` — one line, used for auto-invocation matching

---

## Validation

Always validate before committing:

```bash
claude plugin validate .
```

Or from inside Claude Code:

```
/plugin validate .
```

Common validation warnings to fix before PR:
- `No marketplace description provided` — add top-level `description` to `marketplace.json`
- `Plugin name is not kebab-case` — rename to lowercase-with-hyphens

---

## Adding a New Plugin

1. Create `plugins/<plugin-name>/` with the structure above
2. Add `.claude-plugin/plugin.json` with required fields
3. Add at least one skill, agent, or command
4. Add `README.md` to the plugin directory
5. Register the plugin in `.claude-plugin/marketplace.json`
6. Run `claude plugin validate .` and fix all errors
7. Open a PR on a `feature/<plugin-name>` branch

---

## GitHub Actions

CI runs `claude plugin validate .` on every PR. PRs with validation errors will not be merged.

---

## Installing This Marketplace Locally

```bash
/plugin marketplace add rgoshen/my_plugins
/plugin install cs-tutor@my-plugins
```

---

## Key References
- [Plugin marketplaces docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
