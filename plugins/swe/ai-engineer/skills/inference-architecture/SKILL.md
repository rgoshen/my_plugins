---
name: inference-architecture
description: Use when designing structured output from an LLM, building validation layers, handling model output errors, setting sampling parameters (temperature, top-p, max tokens), configuring thinking/reasoning mode, writing retry logic, or defining the contract between a model and its downstream consumers.
---

# Inference Architecture

Reference for building reliable LLM inference pipelines.

## Structured Output

LLMs are probabilistic. Output structure is not guaranteed. Mitigations in increasing order of strength:

1. **Prompt the schema** in the system message
2. **Parse and validate** after generation — accept only what's valid
3. **Retry on failure** with a repair prompt that includes the specific validation error
4. **Constrained generation** (Instructor, Outlines, function calling) — model forced to produce valid output at the decoding layer
5. **Library-enforced schemas** (Pydantic with validation) as the contract at the system boundary

Pick the minimum that gives you the reliability you need.

## Validation Layers

| Layer | What it checks | When |
|---|---|---|
| **Input validation** | Length, format, suspicious content | Before the model sees the data |
| **Schema validation** | Output matches expected shape | After generation |
| **Semantic validation** | Output is internally consistent (cross-field rules, logical constraints) | After schema passes |
| **Human-in-the-loop** | High-stakes decisions reviewed by a human | For flagged outputs |

## Error Handling

- **Typed result contracts** — success vs. failure is part of the type system, not a convention
- **Retry policies** — bounded (max N attempts), with backoff, with repair context passed to the model
- **Failure categorization** — unreachable, malformed, and semantic failures deserve different handling
- **Never silently pass through bad output** — if validation fails and retry doesn't recover, surface the failure explicitly

## Sampling Parameters

| Parameter | Guidance |
|---|---|
| **Temperature** | 0.0–0.3 for structured/factual; 0.7–1.2 for creative |
| **Top-p** | 0.9 is a reasonable default |
| **Top-k** | 40 is a reasonable default |
| **Repetition penalty** | > 1.0 helps with looping but hurts JSON (field names legitimately repeat) |
| **Max tokens** | Interacts with thinking mode — test your runtime before relying on it as a safety net |

## Thinking / Reasoning Mode

When a model generates internal reasoning before visible output:

- Thinking tokens are generated and billed even when invisible
- `max_tokens` may cap thinking + visible tokens combined — verify on your runtime
- **Disable for**: structured output tasks, latency-sensitive apps, high-volume inference
- **Control via**: `think=false` (Ollama native API), `/no_think` prompt prefix, custom modelfile

Lock thinking mode before benchmarking — mixed settings invalidate comparisons.

## Pipeline Pattern

```
Input → [Input validation] → [Model call] → [Schema validation] → [Semantic validation] → Output
                                   ↑                   |
                             [Retry + repair] ←─────────┘ (on failure, bounded)
                                                          ↓ (exhausted)
                                                     Explicit failure
```

The pipeline is the system. The model is one component. Design the pipeline first, then plug the model into it.
