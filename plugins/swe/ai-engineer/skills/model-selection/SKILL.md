---
name: model-selection
description: Use when choosing between models, comparing local vs cloud inference, selecting quantization level, evaluating model families (Llama, Mistral, Qwen, OpenAI, Anthropic, Gemma, DeepSeek), picking an inference runtime, or deciding whether a model fits available hardware or budget.
---

# Model Selection

Reference for choosing models and inference approaches.

## Evaluation Dimensions

- **Capability on your task** — measured on YOUR eval set, not published benchmarks
- **Size / memory footprint** — determines where it can run
- **Latency** — tokens/sec; p95 matters more than mean
- **Cost** — per-request (cloud) or amortized (local hardware)
- **Context window** — larger isn't always better; attention degrades on long contexts
- **Structured output reliability** — some models follow JSON schemas more reliably than others
- **License** — commercial use allowed? redistribution? fine-tuning permitted?
- **Maturity** — how well-understood are its failure modes?

Don't pick a model by reputation. Test on your task.

## Local vs Cloud vs Hybrid

| Choice | Wins on | Loses on |
|---|---|---|
| **Local inference** | Cost at volume, privacy, no rate limits, offline capability | Hardware investment, capacity ceiling, operational burden |
| **Cloud API** | Frontier capability, zero infra, elastic scale, always current | Per-request cost, privacy concerns, rate limits, vendor lock-in |
| **Hybrid** | Local for volume, cloud for hard cases | Complexity, two prompt sets to maintain, two failure modes |

Break-even test: at your actual request volume, which option is cheaper *over 12 months* including operational time? Small volumes favor cloud. High volumes favor local. The crossover depends on hardware cost and token counts.

## Model Families

- **Proprietary APIs** (OpenAI, Anthropic, Google): frontier capability, closed weights, usage-based pricing
- **Open-weight from labs** (Llama, Qwen, Mistral, Gemma, DeepSeek): downloadable, runnable locally, varying commercial licenses
- **Specialized code models** (DeepSeek Coder, Qwen Coder, CodeLlama): tuned for code, often outperform general models on coding tasks at smaller sizes
- **Small efficient models** (Phi, Llama 3.2 1B/3B, small Gemma): edge devices, useful for routing/classification in pipelines

## Quantization Options

| Format | Memory savings | Quality loss |
|---|---|---|
| **FP16/BF16** | Baseline | None |
| **INT8** | ~2x | Minimal |
| **Q4_K_M / INT4 / 4-bit** | ~4x | Noticeable but usually acceptable |
| **< 4-bit** | > 4x | Significant — only for extreme memory constraints |

## Sampling Parameters Quick Reference

| Output type | Temperature | Notes |
|---|---|---|
| **Structured (JSON, code)** | 0.0–0.3 | Near-zero maximizes schema adherence |
| **Factual Q&A** | 0.0–0.3 | Consistent answers, fewer hallucinations |
| **Creative writing** | 0.7–1.0 | Variation is desirable |
| **Brainstorming** | 0.9–1.2 | Exploration over convergence |

Top-p (0.9) and top-k (40) are reasonable defaults. Repetition penalty > 1.0 helps with looping but hurts JSON output.

## Thinking / Reasoning Mode

Some models (Qwen 3.5, DeepSeek-R1, QwQ) generate internal chain-of-thought before visible output:

- Thinking tokens are billed even though they don't appear in output. A 150-token response may consume 2,000+ reasoning tokens internally.
- 2,000 reasoning tokens at 60 tok/sec = 33 seconds of invisible work.
- **Disable for**: structured output, latency-sensitive apps, high-volume inference
- **Keep for**: complex reasoning, multi-step planning, where measured quality improvement justifies cost

Lock this decision before benchmarking — mixed settings invalidate comparisons.
