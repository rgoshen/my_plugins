---
name: agent-design
description: Use when deciding whether to build an agent, designing tools for an agent, choosing a planning strategy (ReAct, plan-then-execute, reflexion), managing agent memory and context windows, setting safety boundaries, evaluating agent task completion, or preventing runaway agent loops.
---

# Agent Design

Reference for building tool-using, multi-step AI systems.

## When Agents Are the Right Pattern

Use when:
- Task requires calling external tools or APIs (search, database, file ops, code execution)
- Task has conditional branching that depends on intermediate results
- Number of steps isn't known in advance
- A human doing the task would need to "look things up" or "try something and check"

**When they aren't:** a single model call would work; task flow is deterministic and can be hardcoded; latency doesn't tolerate multi-step loops; cost of N model calls exceeds value delivered.

Rule of thumb: if you can draw the complete flowchart before runtime, you need a pipeline, not an agent.

## Tool Design

Tools are the agent's interface to the world. Poor tool design causes more failures than bad planning.

- **Clear, unambiguous names and descriptions** — the model picks tools by description; vague = wrong picks
- **Typed inputs and outputs** — JSON Schema or function signatures
- **Atomic operations** — one tool does one thing; "search_and_summarize" should be two tools
- **Idempotent where possible** — retries shouldn't create duplicate side effects
- **Error messages the model can act on** — "Authentication failed: API key expired" vs "Error 500"
- **Least privilege** — every tool is attack surface; give the agent only what it needs

## Planning Strategies

| Strategy | How it works | Best for |
|---|---|---|
| **ReAct** | Think → Act → Observe → repeat | General-purpose, easy to debug, works with most models |
| **Plan-then-execute** | Generate full plan, then execute steps | Tasks with known structure, reduces mid-task replanning |
| **Reflexion / self-correction** | Execute, evaluate result, revise if needed | Tasks where first attempts often fail |
| **Tree of Thought** | Explore multiple reasoning paths, select best | Complex reasoning where first path may be wrong |

Start with ReAct. Add complexity only when measurement shows simpler approaches fail on your task.

## Memory and Context Management

- **Conversation history** — summarize older turns, keep recent turns verbatim; raw history fills context fast
- **Working memory** — intermediate results stored as structured state, not conversational prose
- **Long-term memory** — persistent across sessions; requires external storage (database, vector store); adds retrieval latency
- **Context window budget** — system prompt + tools + history + working memory + retrieved context all compete; budget explicitly and monitor utilization; when context fills, the agent starts forgetting

## Safety and Boundaries

- **Action confirmation** — irreversible actions (delete, send, publish) require human confirmation unless explicitly pre-authorized
- **Scope limits** — define what the agent is *allowed to do*, not just what tools it has
- **Runaway prevention** — set a maximum number of steps or tool calls per task; an agent stuck in a loop will consume tokens indefinitely
- **Blast radius** — before giving an agent a capability, ask: "what's the worst that could happen if this tool is used incorrectly?" Design safeguards for that case.
- **Audit trail** — log every tool call, observation, and decision; when the agent does something unexpected, the trail is how you find out why

## Evaluation

| What to measure | How |
|---|---|
| **Task completion rate** | % of tasks finished correctly end-to-end |
| **Step efficiency** | Steps taken vs minimum needed |
| **Tool selection accuracy** | Right tool chosen per step? |
| **Recovery from errors** | Does the agent adapt when a tool call fails? |
| **Cost per task** | Total tokens across all steps |
| **Failure mode classification** | Wrong tool? Bad plan? Context overflow? Hallucinated tool input? |

Evaluate on realistic multi-step tasks, not isolated tool calls. An agent that uses each tool correctly in isolation can still fail at composing them into a coherent plan.
