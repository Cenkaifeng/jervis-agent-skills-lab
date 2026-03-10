# Query recipes

## 1) Current session usage

Use `session_status`.

Report:
- current model
- current context window
- current occupancy / token usage
- any notable override or reasoning mode

Example user asks:
- “我这个会话现在用的什么模型？”
- “现在上下文占了多少？”
- “看看当前会话用量”

## 2) Multi-session overview

Preferred repeatable path:

```bash
python {baseDir}/scripts/report_usage.py --format text
python {baseDir}/scripts/report_usage.py --agent jarvis --active-hours 24
python {baseDir}/scripts/report_usage.py --min-pct 40
python {baseDir}/scripts/report_usage.py --mode anomaly
```

Or use `sessions_list(limit=...)` first when you want a manual/custom answer.

Look for:
- which agents are active
- which models appear most often
- highest token/context sessions
- stale sessions that still occupy large context

Good response shape:
- total active sessions inspected
- model distribution
- top 3 highest-occupancy sessions
- recommendation block (fresh thread / old-model residue / stale-large sessions)

## 3) Agent-specific usage

Use `sessions_list`, filter by session key prefix (for example `agent:jarvis:` or `agent:main:`) in your reasoning, then inspect the most relevant sessions with `session_status(sessionKey=...)`.

Use when asked:
- “jarvis 最近都在用什么模型？”
- “main 和 jarvis 谁更占 token？”

## 4) Post-upgrade model sanity check

Use `exec`:
- `openclaw status`
- `openclaw status --deep` when health/channel/probe context matters

Then combine with `sessions_list` if needed.

Report:
- running app version
- default model from status
- key active sessions and their models
- any mismatch between expected routing and observed sessions

## 5) Exact billing question

If the user asks for actual money spent:
- first check whether `session_status` or status output provides cost in this environment
- if not, say cost is not directly exposed by the current OpenClaw telemetry you can access
- then offer the best substitute: session occupancy, model distribution, and active-session usage summary

Do not blur token occupancy with billed cost.
