# Contributing

## Adding a new plugin

1. Create `plugins/<plugin-name>/` with the standard structure:
   ```
   plugins/<plugin-name>/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── agents/
   ├── skills/
   ├── commands/
   └── README.md
   ```
2. Add `.claude-plugin/plugin.json` with `name`, `description`, and `version`
3. Add at least one skill, agent, or command
4. Add `README.md` documenting what the plugin provides and how to use it
5. Register the plugin in `.claude-plugin/marketplace.json`
6. Run `claude plugin validate .` — fix all errors before opening a PR

## Plugin conventions

- **Never hardcode `~/.claude/` paths** in skills or agents — plugins are copied to a cache directory on install; those paths won't exist
- **Agents are entry points; skills are workflows** — agents carry the persona and declare which skills they use via `skills:` frontmatter; skills contain the session logic; skills must not attempt to read agent files
- **Commands** are thin `.md` files in `commands/` that invoke an agent; they are the user-facing slash commands
- **`version` in one place only** — set it in `plugin.json`, not in the `marketplace.json` entry, to avoid silent conflicts

## Plugin-specific authoring guides

Some plugins define conventions that all contributors to that plugin must follow. Check the plugin's own README before adding components to an existing plugin.

| Plugin | Convention doc |
|--------|---------------|
| `cs-tutor` | See [plugins/cs-tutor/README.md — Adding a new tutor](plugins/cs-tutor/README.md#adding-a-new-tutor) for the session-state-manager parameter contract required by every teach skill |

## Validation

```bash
claude plugin validate .
```

Fix all errors. Warnings should also be resolved where practical.

## Branch and PR

- Branch: `feature/<plugin-name>` or `fix/<description>`
- PR title: follow Conventional Commits (`feat:`, `fix:`, etc.)
- CI must pass before merge
