---
name: fine-tuning
description: Use when deciding whether to fine-tune a model, choosing between LoRA, QLoRA, and full fine-tuning, estimating training data requirements, selecting a base model, comparing fine-tuning against prompt engineering or RAG, or planning training infrastructure and data pipelines.
---

# Fine-Tuning

Reference for training and adapting language models.

## When Fine-Tuning Pays Off

- You need consistent behavior in a domain the base model handles inconsistently
- A smaller fine-tuned model can match a larger base model at lower inference cost
- You have real labeled data (hundreds to thousands of quality examples minimum)
- Behavior you need is hard to elicit via prompting alone

**When it doesn't:**
- A better prompt would work — always try this first
- Insufficient quality data
- Base model already does the task well
- You underestimate the operational cost of maintaining a fine-tuned model across base model updates

## Technique Selection

| Technique | Use when |
|---|---|
| **Prompt engineering** | Always the first option |
| **Few-shot prompting** | 3–10 canonical examples and the model picks up the pattern |
| **LoRA** | Parameter-efficient, consumer GPU-friendly, good for domain adaptation |
| **QLoRA** | LoRA with 4-bit base — larger models on smaller hardware |
| **Full fine-tuning** | You have compute, quality data, and a strong reason LoRA won't work |
| **DPO / RLHF** | Shaping preferences or style, not just task behavior |
| **Continued pretraining** | Teaching the model a new domain's language — rare; usually prompting or RAG works |

## Data Sizing Heuristics

- Training from scratch: ~20x parameter count in training tokens
- Fine-tuning: hundreds to low thousands of high-quality examples is often enough
- Quality matters more than quantity. One hour of label cleaning beats three hours of data collection.

## Training Infrastructure by Approach

| Approach | Approximate VRAM | Frameworks |
|---|---|---|
| **LoRA (7B model)** | ~16GB | Hugging Face, Axolotl |
| **QLoRA (13B model)** | ~12GB | Unsloth, Hugging Face |
| **Full fine-tune (7B)** | ~60GB+ | DeepSpeed, FSDP |
| **Full fine-tune (70B)** | Multi-GPU required | DeepSpeed + ZeRO-3 |

## Evaluation After Fine-Tuning

- Measure task performance vs the base model
- Measure regression on general capabilities — fine-tuning can improve target task while degrading breadth
- Export format must match inference runtime (safetensors for most; GGUF for llama.cpp/Ollama)

## Quantization for Deployment

| Format | Memory savings | Quality loss |
|---|---|---|
| **FP16/BF16** | Baseline | None |
| **INT8** | ~2x | Minimal |
| **Q4_K_M / 4-bit** | ~4x | Noticeable but usually acceptable |
| **< 4-bit** | > 4x | Significant — only for extreme memory constraints |
