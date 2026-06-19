---
title: ai-engineer
layout: default
parent: Plugins
nav_order: 3
---

# ai-engineer

![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)
![CI](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Senior AI/ML engineering specialist. A self-contained sub-agent carrying a full AI/ML decision framework, plus an indexed set of nine skills that auto-activate by topic (RAG, evaluation, security, model selection, inference, agent design, fine-tuning, deployment). Wired to Context7 for live documentation lookup.
{: .fs-5 }

---

## Prerequisites

### Context7 MCP

The plugin ships a Context7 MCP server (`.mcp.json`) for live model/SDK/runtime documentation lookup. Claude Code prompts to approve it on first use. If you already have Context7 configured globally, `/doctor` may note a duplicate server — expected and harmless.

---

## Install

```
/plugin marketplace add rgoshen/my_plugins
/plugin install ai-engineer@my-plugins
```

---

## Components

### Commands

| Command | Description |
|---|---|
| `/ai-engineer:ai-engineer` | The index skill — routes to the right focused skill |
| `/ai-engineer:rag-patterns` | RAG pipelines, chunking, vector stores, retrieval |
| `/ai-engineer:llm-evaluation` | Eval sets, metrics, benchmarking, experiment design |
| `/ai-engineer:llm-security` | Prompt injection, guardrails, output sanitization |
| `/ai-engineer:model-selection` | Model families, local vs cloud, quantization, fit |
| `/ai-engineer:inference-architecture` | Structured output, validation, sampling, retries |
| `/ai-engineer:agent-design` | Tool design, planning, agent memory, safety |
| `/ai-engineer:fine-tuning` | LoRA/QLoRA/full fine-tuning, base model, data |
| `/ai-engineer:ai-deployment` | Inference runtimes, containerization, cost, observability |

### Agents

| Agent | Description |
|---|---|
| `ai-engineer` | Senior AI/ML engineer sub-agent for delegated, multi-step project work in its own context; carries the full decision framework, preloads the index skill, and mandates Context7 lookup. Invoke as `@ai-engineer:ai-engineer`. |

### Skills

| Skill | Description |
|---|---|
| `ai-engineer` | Index — routes to the right focused skill, or to the sub-agent for hands-on building. |
| `rag-patterns` | RAG pipelines, chunking, vector stores, retrieval, hybrid search, RAG evaluation. |
| `llm-evaluation` | Eval sets, metrics, benchmarking, experiment design, drift detection. |
| `llm-security` | Prompt injection, guardrails, adversarial input, PII/output sanitization. |
| `model-selection` | Model families, local vs cloud, quantization, hardware/budget fit. |
| `inference-architecture` | Structured output, validation layers, sampling params, retry logic. |
| `agent-design` | Tool design, planning strategies, agent memory, safety boundaries. |
| `fine-tuning` | LoRA/QLoRA/full fine-tuning, base-model selection, training data. |
| `ai-deployment` | Inference runtimes, containerization, cost analysis, observability. |

---

## How it works

- **Inline skills**: just start working on an AI/ML topic — the matching skill activates on context. Unsure which applies? The `ai-engineer` index skill routes you.
- **Sub-agent**: delegate project-level work (scoping, architecture decisions, building end-to-end). It runs in its own context, makes and documents decisions, and returns a self-contained summary.
- **One decision framework**: the agent carries the framework inline and preloads the index skill via `skills:` frontmatter; the focused skills stand alone for quick, inline expertise.

---

## Philosophy

- **Architect the solution, make the decisions, balance the tradeoffs.** Every significant decision names its options, tradeoffs, chosen path — and its failure modes.
- **Production thinking from day one.** Validation, error handling, observability, and evaluation are architectural concerns, not afterthoughts.
- **Treat AI outputs as untrusted.** Always a validation layer, a failure path, and a fallback.
- **Look it up, don't guess.** Version-sensitive model/SDK/runtime facts go through Context7 before being asserted, then cited.

---

## Changelog

See [CHANGELOG.md](https://github.com/rgoshen/my_plugins/blob/main/plugins/swe/ai-engineer/CHANGELOG.md).

---

## Source

[github.com/rgoshen/my_plugins/tree/main/plugins/swe/ai-engineer](https://github.com/rgoshen/my_plugins/tree/main/plugins/swe/ai-engineer)
