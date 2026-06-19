# Changelog

All notable changes to the `ai-engineer` plugin.

## [0.1.0] - 2026-06-18

### Added
- Initial release. Imported into the `my_plugins` marketplace under `plugins/swe/`.
- `ai-engineer` sub-agent — a senior AI/ML engineer carrying a full AI/ML decision framework inline (problem framing, data, evaluation, cost, training, fine-tuning, inference/deployment, RAG, agents). Preloads the `ai-engineer` index skill via `skills:` frontmatter and mandates Context7 documentation lookup. Invoke as `@ai-engineer:ai-engineer`.
- `ai-engineer` skill — an index that routes to the right focused skill, or to the sub-agent for hands-on project work.
- Eight focused skills, each auto-activating by topic and invocable as `/ai-engineer:<skill>`:
  - `rag-patterns` — RAG pipelines, chunking, vector stores, retrieval, evaluation.
  - `llm-evaluation` — eval sets, metrics, benchmarking, experiment design, drift.
  - `llm-security` — prompt injection, guardrails, output sanitization, defense-in-depth.
  - `model-selection` — model families, local vs cloud, quantization, hardware/budget fit.
  - `inference-architecture` — structured output, validation layers, sampling, retry logic.
  - `agent-design` — tool design, planning strategies, agent memory, safety boundaries.
  - `fine-tuning` — LoRA/QLoRA/full fine-tuning, base-model selection, training data.
  - `ai-deployment` — inference runtimes, containerization, cost analysis, observability.
- Context7 MCP server (`.mcp.json`) for live model/SDK/runtime documentation lookup.
