---
name: ai-engineer
description: Use when unsure which specific AI/ML skill applies — routes to the right focused skill (RAG, evaluation, security, model selection, inference, agent design, fine-tuning, deployment), or hands off to the ai-engineer agent for scoping and hands-on project work.
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
