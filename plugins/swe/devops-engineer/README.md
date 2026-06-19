# devops-engineer

A senior DevOps/platform-engineering specialist for OpenTofu, Terraform, IaC, AWS, and CI/CD, packaged as a Claude Code plugin in the [`my_plugins`](https://github.com/rgoshen/my_plugins) marketplace. Part of the **swe** plugin family (`plugins/swe/`).

These entry points share the plugin's conventions, plus the Context7 MCP server for live documentation lookup:

- **`devops-engineer` skill** (`skills/devops-engineer/`) — loads *inline* in your main conversation when IaC/AWS comes up, and is also invocable as `/devops-engineer:devops-engineer`. Quick hits and mid-conversation expertise.
- **`ci-cd` skill** (`skills/ci-cd/`) — CI-agnostic CI/CD expertise (GitHub Actions, GitLab CI, Woodpecker CI, branching/release models, deployment strategies, pipeline security). Loads inline when CI/CD comes up, and is invocable as `/devops-engineer:ci-cd`. Platform-specific YAML lives in its `references/`.
- **Sub-agent** (`agents/devops-engineer.md`) — runs in its *own context* for delegated, multi-step work (`@devops-engineer:devops-engineer`). It preloads the skill via the `skills:` frontmatter field, so the conventions live in one place and don't drift. It enforces Context7 lookup harder than the inline skill.
- **Context7 MCP** (`.mcp.json`) — provides live docs lookup to the session; the agent inherits it.

## Structure

```
plugins/swe/devops-engineer/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── devops-engineer/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── conventions.md
│   └── ci-cd/
│       ├── SKILL.md
│       └── references/
│           ├── branching-models.md
│           ├── github-actions.md
│           ├── gitlab-ci.md
│           ├── woodpecker-ci.md
│           ├── deployment-strategies.md
│           ├── pipeline-security.md
│           └── iac-pipelines.md
├── agents/
│   └── devops-engineer.md
└── .mcp.json
```

The skill *folder* name (`devops-engineer`) sets both the skill name and its `/devops-engineer:devops-engineer` slash command. The agent file is named for the agent.

## Install

```
/plugin marketplace add rgoshen/my_plugins
/plugin install devops-engineer@my-plugins
```

On first use Claude Code prompts to approve the Context7 MCP server.

## Usage

- **Inline skill**: start working on IaC/AWS; it activates on context (`.tf`/`.tofu` files, tofu/terraform commands, plan/apply errors, "write a module", "review my terraform", "design the AWS architecture for X"), or call `/devops-engineer:devops-engineer`.
- **Sub-agent**: delegate, e.g. *"Use the devops-engineer sub-agent to audit modules/networking for security issues"*, or let Claude auto-delegate on multi-step IaC tasks.

## Notes

- **Context7 enforcement differs by entry point on purpose.** Plugin-shipped agents can't declare `mcpServers` in their own frontmatter, so Context7 is provided at the plugin's `.mcp.json` and the agent inherits it. The agent's prompt mandates resolve-then-fetch-then-cite; the inline skill states it as a strong preference. Both are behavioral biases, not hard locks — a pre-commit/CI hook is the only true guarantee.
- **No duplication drift:** the agent doesn't restate the conventions — it preloads the skill via `skills:`. Edit `SKILL.md` / `references/conventions.md` once.
- If you already have Context7 configured globally, `/doctor` may note a duplicate server; this is expected and harmless.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
