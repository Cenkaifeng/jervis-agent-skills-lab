---
name: openclaw-model-usage
description: Inspect OpenClaw model usage, session token/context occupancy, agent-level model distribution, and active-session health using built-in OpenClaw tools. Use when the user asks about model usage, token usage, which models are being used, session occupancy, agent model distribution, or whether usage is too high in the current OpenClaw environment. Not for provider billing portals or CodexBar-local client cost logs.
---

# OpenClaw model usage

## Overview

Use this skill to answer “what models are we using?” and “how full are sessions?” for this OpenClaw deployment.

Prefer OpenClaw-native telemetry over third-party tools. Start with the built-in status/session tools before considering any external usage source.

## Quick workflow

### Fast path via bundled script

When you want a one-shot operational summary, run:

```bash
python {baseDir}/scripts/report_usage.py --format text
python {baseDir}/scripts/report_usage.py --format json
python {baseDir}/scripts/report_usage.py --agent jarvis --active-hours 24
python {baseDir}/scripts/report_usage.py --min-pct 40 --warn-pct 40 --crit-pct 70
```

Use the script for repeatable overview reports; use direct tools (`session_status`, `sessions_list`) when you need a narrower or conversationally guided answer.


1. **Clarify the scope implicitly from the user's wording**:
   - “我这个会话用了多少 / 当前模型是什么” → current session
   - “最近都在用什么模型” → active sessions overview
   - “哪个 agent 最占 token / 上下文” → session comparison
   - “升级后模型路由正常吗” → gateway + sessions snapshot
   - “账单/美元花费” → explain whether exact cost is or is not available from OpenClaw tools

2. **Use the right tool first**:
   - **Current session** → `session_status`
   - **Cross-session overview** → `sessions_list`
   - **Gateway-wide snapshot / channel + model view** → `exec` with `openclaw status` or `openclaw status --deep`

3. **Go deeper only when needed**:
   - Use `session_status(sessionKey=...)` for specific sessions found in `sessions_list`
   - Use `sessions_history` only when the user needs behavior/debug context, not for basic usage summaries

4. **Be precise about what the numbers mean**:
   - `Tokens` / `context` from session views are occupancy and usage indicators
   - Do **not** call them provider-billed cost unless a tool explicitly provides cost
   - If exact billing is unavailable, say so plainly and still provide the best operational usage summary

## Default reporting formats

### A. Current session
Use `session_status` and summarize:
- model
- context window
- current occupancy / token usage
- whether reasoning / overrides matter

### B. Active-session overview
Use `sessions_list`, then summarize:
- active sessions by agent
- model distribution
- largest token/context consumers
- any suspiciously stale or oversized sessions

### C. Upgrade / health check angle
Use `openclaw status --deep` when the user is really asking whether model usage/routing still looks healthy after a config change or upgrade. Include:
- current OpenClaw app version
- default model shown by status
- important active sessions and their models
- obvious mismatches or drift

## Rules

- Prefer concise operational summaries over raw dumps.
- If only one session matters, do **not** enumerate all sessions.
- If many sessions are active, rank the top few by token/context usage instead of listing everything.
- Do not invent cost numbers.
- If the user wants a persistent dashboard/report, propose creating a dedicated script or cron after first giving the live snapshot.
- Highlight operational next steps when they are obvious: prepare fresh thread, note old-model residue, or flag stale large sessions.

## When to read more

Read `references/query-recipes.md` for common query patterns and response shapes when you need a reusable reporting structure.
