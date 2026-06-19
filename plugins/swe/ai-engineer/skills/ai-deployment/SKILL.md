---
name: ai-deployment
description: Use when deploying an AI application, choosing inference runtimes (Ollama, vLLM, llama.cpp, TGI, MLX), containerizing a model server, setting up monitoring or observability, calculating break-even between local and cloud inference, or designing logging and alerting for an LLM system in production.
---

# AI Deployment

Reference for deploying and operating AI systems in production.

## Inference Runtime Options (Local)

| Runtime | Best for | Notes |
|---|---|---|
| **Ollama** | Easy setup, broad model support, OpenAI-compatible | Best starting point for local inference |
| **llama.cpp** | Maximum flexibility, almost any hardware | More setup required |
| **vLLM** | Production-grade throughput, high volume | GPU required |
| **MLX** | Apple Silicon native | Often fastest on Macs |
| **TensorRT-LLM** | NVIDIA-specific extreme throughput | Significant setup complexity |
| **HF Transformers** | Research, maximum flexibility | Slowest for inference |

## Containerization Gotchas

- **GPU access in containers is platform-specific.** Docker Desktop on Mac/Windows runs a Linux VM with no host GPU access. Native Linux + NVIDIA Container Toolkit is the only fully GPU-capable Docker setup.
- **Model weights are large.** Bake them in (large images) or mount/download at runtime (slower first run). Mounting is usually the right call.
- **Keep the serving runtime on the host when GPU access in the container isn't viable.** The app runs containerized and talks to the runtime over localhost.

## Cloud Deployment Patterns

| Pattern | Best for | Watch out for |
|---|---|---|
| **Serverless** (Modal, Replicate, Beam) | Pay-per-use, bursty workloads | Cold starts, unpredictable latency |
| **Dedicated endpoints** (SageMaker, Vertex, Together) | Predictable latency, always-on | Fixed cost, over/under provisioning |
| **API gateway + multiple providers** | Vendor redundancy, fallback | Added latency, two prompt sets to maintain |
| **Self-managed VMs** | Maximum control | Maximum operational burden |

## Cost Analysis

Model three layers honestly:

**Direct inference cost**
- Cloud: input tokens × input price + output tokens × output price, per request
- Local: amortized hardware cost per request (effectively ~$0 marginal once hardware is paid)

**Hardware amortization (local)**
```
daily_hardware_cost = purchase_price / useful_life_days
```

**Break-even volume**
```
break_even_volume = daily_hardware_cost / cloud_cost_per_request
```
Below break-even: cloud is cheaper per day. Above: local is cheaper. Most "cloud is cheaper" or "local is cheaper" claims depend entirely on which side of this line the project sits.

**Total cost of ownership** — include engineering time, electricity, maintenance, and model updates. Hard to quantify, but name it honestly.

## Observability

Separate benchmarking from monitoring — they answer different questions:

- **Benchmarking**: "How does this perform on a known test set?" Static snapshot.
- **Monitoring**: "What's happening right now?" Rolling time-series, alerting, drift detection.

### What to Monitor

- Request latency (p50, p95, p99)
- Token usage per request (cost signal + context budget signal)
- Error rate and failure type distribution
- Output validation pass rate
- Drift indicators over time
- Resource utilization (GPU memory, CPU, queue depth)

### Logging Rules

- Log enough to debug failures: request ID, model, token counts, latency, validation result
- Never log full prompt content without explicit consent controls — full prompts are a PII liability
- Never log credentials, API keys, or secrets
