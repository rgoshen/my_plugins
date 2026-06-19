---
name: ai-engineer
description: Use when starting or scoping an AI/ML project, needing a senior AI engineer's judgment, or unsure which specific AI skill applies. Routes to the right focused skill or the ai-engineer agent for hands-on building.
---

# AI Engineer — Index & Router

This skill was split into focused reference skills. Use the specific skill for the topic at hand, or invoke the `ai-engineer` agent for full project work.

## Route to the Right Skill

| Topic | Use skill |
|---|---|
| RAG pipelines, chunking, vector stores, retrieval, embedding | `rag-patterns` |
| Evaluation datasets, metrics, benchmarking, experiment design | `llm-evaluation` |
| Prompt injection, guardrails, adversarial input, output sanitization | `llm-security` |
| Choosing a model, local vs cloud, quantization, model families | `model-selection` |
| Structured output, validation layers, retry logic, sampling parameters | `inference-architecture` |
| Tool design, planning strategies, agent memory, safety boundaries | `agent-design` |
| LoRA, QLoRA, full fine-tuning, training data, base model selection | `fine-tuning` |
| Inference runtimes, containerization, cost analysis, observability | `ai-deployment` |

## Route to the Agent

Use the `ai-engineer` **agent** (not this skill) when you want to:
- Start or scope a new AI/ML project
- Get architectural decisions made and documented
- Have code written, files created, or a system built end-to-end
- Audit an existing project against the decision framework

The agent carries the full AI/ML decision framework and operates as a senior engineer — it makes decisions, writes code, and explains tradeoffs.
