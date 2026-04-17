# Architecture

## Overview

```
User
 |
 v
API (FastAPI)
 |
 v
InputGuard  <-- validate and sanitize
 |
 v
BaseAgent (ReAct loop)
 |-- Memory (conversation context)
 |-- Tools (external actions)
 |-- LLM (reasoning)
 |
 v
OutputGuard <-- validate response
 |
 v
User
```

## Agent Loop (ReAct)

1. **Reason** — LLM reasons about the task and decides which tool to use
2. **Act** — Execute the tool
3. **Observe** — Receive the result and add it to memory
4. Repeat until `stop_reason == end_turn` or `max_iterations`

## Technical Decisions

| Decision | Choice | Why |
|---------|---------|--------|
| Agent pattern | ReAct | Simple, auditable, works well with Claude |
| Memory | Buffer (sliding window) | Zero dependencies for MVP |
| Tool registry | Central dict | Easy to add/remove tools |
| Guardrails | Pure functions | Testable and low overhead |

## ADRs

Add relevant decisions: `docs/adr-001-memory-choice.md`
