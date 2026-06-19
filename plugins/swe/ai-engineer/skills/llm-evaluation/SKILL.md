---
name: llm-evaluation
description: Use when designing an eval set, choosing metrics for an LLM task, structuring experiments, measuring model quality, building benchmarks, deciding what "better" means, or evaluating RAG retrieval and generation separately. Also for agent task completion measurement or detecting model drift in production.
---

# LLM Evaluation

Reference for measuring model and system quality rigorously.

## Dataset Design

- **Label quality over quantity.** 20 well-labeled examples reveal more than 200 sloppy ones.
- **Cover the full input space.** Edge cases, not just the happy path.
- **Separate eval sets.** A "gold" set for grading and a "dev" set for iteration — never tune against the set you grade on.
- **Adversarial sets** for systems that face untrusted input. Label each example with the expected correct behavior.

## Experiment Design

- **One variable per experiment.** Hold everything else constant.
- **State the hypothesis first.** "I expect X because Y." Write it down before running.
- **Report negative results.** "This didn't work, here's why" is a finding. Hiding it is worse than not finding it.
- **Be honest about statistical power.** Small datasets reveal patterns but don't prove them. Say so.

## Metrics by System Type

| System | Primary metrics |
|---|---|
| **Classification / extraction** | Precision, recall, F1 per class |
| **Generation** | Human review for a sample; BLEU/ROUGE as rough signals only |
| **RAG** | Retrieval: recall@k, MRR. Generation: faithfulness, relevance, attribution |
| **Agents** | Task completion rate, step efficiency, tool selection accuracy, cost per task |
| **Structured output** | Parse rate, schema adherence, cross-field validation pass rate |

## Beyond Accuracy

- **Per-field accuracy** when output is structured
- **Latency percentiles** — p95 is what users feel; mean hides tail behavior
- **Tokens per request** — cost driver and context budget consumer
- **Failure mode distribution** — when it fails, what kind of failure?
- **Retry / recovery behavior** if your system has it
- **Operational metrics** — error rate over time, drift indicators

## Benchmarking vs Monitoring

These answer different questions — don't mix them in a single "metrics" view:

- **Benchmarking**: "How does this perform on a known test set?" Static snapshot.
- **Monitoring**: "What's happening right now?" Rolling time-series, drift indicators, alerting.

## Agent-Specific Evaluation

| What to measure | How |
|---|---|
| **Task completion rate** | % of tasks finished correctly end-to-end |
| **Step efficiency** | Steps taken vs minimum needed |
| **Tool selection accuracy** | Right tool chosen per step? |
| **Recovery from errors** | Does the agent adapt when a tool call fails? |
| **Cost per task** | Total tokens across all steps |
| **Failure mode classification** | Wrong tool? Bad plan? Context overflow? Hallucinated input? |

Evaluate on realistic multi-step tasks, not isolated tool calls. An agent that uses each tool correctly in isolation can still fail at composing them into a coherent plan.
