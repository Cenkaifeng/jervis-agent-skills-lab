# Tool Routing Matrix (v1.1)

## Purpose
Route tasks to the minimal reliable toolchain with explicit fallback.

## Routing Table

### T1: File read/write/refactor
- Primary: read/edit/write
- Fallback: exec (sed/python for batch transforms)
- Avoid: browser/web tools unless source is remote

### T2: Structured shell validation
- Primary: exec
- Fallback: none (escalate on command restrictions)
- Guard: no destructive commands without confirmation

### T3: Web content research
- Primary: web_search + web_fetch
- Fallback: local docs + previously cached references
- Guard: if API key missing -> mark `RESEARCH_LIMITED`

### T4: UI interaction
- Primary: browser snapshot + act
- Fallback: web_fetch for read-only pages
- Guard: keep same tab targetId; avoid unstable waits

### T5: Multi-agent orchestration
- Primary: sessions_spawn / sessions_send
- Fallback: single-agent degraded mode for L1
- Guard: max loop=2, enforce escalation contract

### T6: Messaging actions
- Primary: message tool
- Fallback: none
- Guard: require human gate for external/public sends

## Router Decision Contract
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "task_type": "T1|T2|T3|T4|T5|T6",
  "primary_tools": ["tool1"],
  "fallback_tools": ["tool2"],
  "constraints": ["constraint1"],
  "status": "ROUTED|RESEARCH_LIMITED|ESCALATED"
}
```
