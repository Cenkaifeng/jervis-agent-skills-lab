# Trace Event Spec (v1.1.4)

## Purpose
Standardize trace events across jarvis/livemore/enkidu/taishi for observability and replay.

## Required Event Fields
```json
{
  "trace_id": "TR-YYYYMMDD-XX",
  "run_id": "RUN-...",
  "task_id": "T-...",
  "span_id": "SP-...",
  "stage": "jarvis|livemore|enkidu|taishi",
  "event": "plan_start|plan_end|tool_call|tool_result|handoff|review|escalate|complete|error",
  "ts_utc": "2026-02-26T08:00:00Z",
  "status": "ok|warn|error",
  "latency_ms": 0,
  "meta": {
    "tool": "optional",
    "token_source": "real|mixed|proxy",
    "retry": 0
  }
}
```

## Stage Minimum Events
- jarvis: `plan_start`, `plan_end`, `handoff`
- livemore: `tool_call/tool_result` (optional), `handoff`
- enkidu: `tool_call/tool_result`, `handoff`
- taishi: `review`, `complete|escalate`

## Artifact Path
- `reports/multi-agent-regression/traces/<run_id>.jsonl`
