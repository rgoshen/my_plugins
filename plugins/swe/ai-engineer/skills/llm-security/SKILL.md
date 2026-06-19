---
name: llm-security
description: Use when addressing prompt injection, guardrails, adversarial inputs, output sanitization, PII detection, content filtering, model extraction, data leakage, supply chain risks, or building defense-in-depth for LLM systems that process untrusted input.
---

# LLM Security

Reference for securing LLM systems against adversarial use.

## The Fundamental Vulnerability

LLMs cannot architecturally distinguish instructions from data. Everything is tokens in the same context. This is a property of how transformers work — it cannot be "fixed," only mitigated.

Relevant wherever your system processes untrusted input: user-submitted text, scraped content, forwarded emails, search results, tool outputs.

## Attack Categories

| Attack | Description |
|---|---|
| **Direct injection** | Explicit override instructions in input ("ignore previous instructions...") |
| **Obfuscated injection** | Same attack, encoded or transformed (Base64, language switching, Unicode tricks) |
| **Indirect injection** | Malicious instructions inside content the user legitimately includes (forwarded emails, quoted logs, retrieved documents in RAG) |
| **Multimodal injection** | Text hidden in images for vision models |
| **Data leakage** | Training data or context window contents appearing in outputs |
| **Model extraction** | Reconstructing a fine-tuned model via queries |
| **Denial of service** | Crafted inputs that maximize token use or inference time |
| **Supply chain** | Compromised model weights or training data |

## Defensive Layers

No single layer is sufficient. Defense-in-depth:

1. **Input screening / guardrails** — before the model sees the data (length, format, suspicious patterns)
2. **Prompt-level separation** — delimiters, instructions to treat input as data not commands
3. **Output validation** — catches cases where the model was redirected but produced invalid output
4. **Least privilege** — what the model can *do* with its output (tool calls, system actions) matters more than what it says

## Honest Framing

You don't "solve" prompt injection. You build layered mitigations, measure them against realistic attacks, and document the residual risk. Any claim stronger than that is wrong.

A security statement that says "we prevent prompt injection" rather than "we mitigate and measure" is a red flag — in a vendor's docs or your own.

## Other Concerns

- **PII** — in prompts, inference traces, fine-tuning data; log minimal non-PII context
- **Secrets in context** — never put credentials or API keys in prompts
- **Content filtering** — sanitize output before it reaches downstream consumers
- **Privacy in logs** — never log full prompt content in production without explicit consent controls; full logs are a PII liability
- **Fine-tuning data** — training on user data requires the same privacy controls as any data pipeline
