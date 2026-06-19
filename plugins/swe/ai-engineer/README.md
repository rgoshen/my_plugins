# ai-engineer

A senior AI/ML engineering specialist, packaged as a Claude Code plugin in the [`my_plugins`](https://github.com/rgoshen/my_plugins) marketplace. Part of the **swe** plugin family (`plugins/swe/`).

A self-contained sub-agent carrying a full AI/ML decision framework, an indexed set of focused skills that auto-activate by topic, plus the Context7 MCP server for live documentation lookup:

- **Sub-agent** (`agents/ai-engineer.md`) — a senior AI engineer that runs in its *own context* for delegated, multi-step work (`@ai-engineer:ai-engineer`). It carries the full AI/ML decision framework inline (problem framing, data, evaluation, training, fine-tuning, inference, RAG, agents, deployment) and preloads the `ai-engineer` index skill via the `skills:` frontmatter field. It mandates Context7 lookup for version-sensitive facts.
- **Skills** (`skills/`) — nine skills that activate *inline* in your main conversation when a matching topic comes up. The `ai-engineer` skill is an index that routes to the right focused skill; the other eight are focused references.
- **Context7 MCP** (`.mcp.json`) — provides live docs lookup to the session; the agent inherits it.

## Structure

```
plugins/swe/ai-engineer/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── ai-engineer.md
├── skills/
│   ├── ai-engineer/SKILL.md            # index → routes to the focused skills
│   ├── rag-patterns/SKILL.md
│   ├── llm-evaluation/SKILL.md
│   ├── llm-security/SKILL.md
│   ├── model-selection/SKILL.md
│   ├── inference-architecture/SKILL.md
│   ├── agent-design/SKILL.md
│   ├── fine-tuning/SKILL.md
│   └── ai-deployment/SKILL.md
└── .mcp.json
```

The agent file is named for the agent. Each skill *folder* name sets both the skill name and its `/ai-engineer:<skill>` slash command.

## Install

```
/plugin marketplace add rgoshen/my_plugins
/plugin install ai-engineer@my-plugins
```

On first use Claude Code prompts to approve the Context7 MCP server.

## Usage

- **Inline skills**: start working on an AI/ML topic and the matching skill activates on context — chunking/vector stores (`rag-patterns`), eval sets/metrics (`llm-evaluation`), prompt injection/guardrails (`llm-security`), model choice/quantization (`model-selection`), structured output/validation (`inference-architecture`), tool/planning/memory design (`agent-design`), LoRA/QLoRA (`fine-tuning`), inference runtimes/observability (`ai-deployment`). Unsure which applies? The `ai-engineer` index skill routes you. Call any directly as `/ai-engineer:<skill>`.
- **Sub-agent**: delegate project-level work, e.g. *"Use the ai-engineer sub-agent to scope this RAG system and document the architecture decisions"*, or let Claude auto-delegate on multi-step AI/ML tasks.

## Notes

- **Self-contained agent, no duplication drift.** The agent carries the decision framework inline and preloads the `ai-engineer` index skill via `skills:`. The eight focused skills stand alone and auto-invoke by their descriptions on the main thread.
- **Context7 is provided at the plugin level.** Plugin-shipped agents can't declare `mcpServers` in their own frontmatter, so Context7 ships in the plugin's `.mcp.json` and the agent inherits it. The agent's prompt mandates resolve-then-fetch-then-cite for model identifiers, context limits, pricing, and SDK/runtime flags — the AI/ML facts most likely to be stale in training data.
- If you already have Context7 configured globally, `/doctor` may note a duplicate server; this is expected and harmless.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
