# Protocol and Schema v0.5

## Unified Termination / Escalation Protocol

Apply to both TIMEOUT and NON_TIMEOUT_FAIL.

### Status Enum
- `PASS`
- `PASS_WITH_RISK`
- `TIMEOUT`
- `NON_TIMEOUT_FAIL`
- `ABORT_WITH_REPORT`
- `REQUEST_HUMAN_DECISION`

### Loop Limit Rule
- `max_loops = 2` by default.
- If loop limit reached and still not pass:
  - Must emit `REQUEST_HUMAN_DECISION` or `ABORT_WITH_REPORT`.
  - Must not continue autonomous retry.

### Escalation Payload (Unified)
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "stage": "livemore|enkidu|taishi|jarvis",
  "status": "TIMEOUT|NON_TIMEOUT_FAIL|REQUEST_HUMAN_DECISION|ABORT_WITH_REPORT",
  "loop_count": 0,
  "elapsed_min": 0,
  "partial_result": ["done work"],
  "blocking_reasons": ["reason1"],
  "remaining_work": ["todo1"],
  "options": ["degraded_continue", "human_decision", "abort"],
  "recommended_option": "human_decision"
}
```

## Machine-Checkable JSON Schemas (compact)

Use these schemas as runtime lint contracts.

### 1) livemore_handoff
```json
{
  "type": "object",
  "required": ["schema_version", "task_id", "agent", "summary", "execution_brief", "assumptions", "out_of_scope", "evidence", "risk", "confidence", "next_action"],
  "properties": {
    "schema_version": {"const": "handoff.v1"},
    "task_id": {"type": "string"},
    "agent": {"const": "livemore"},
    "summary": {"type": "string"},
    "execution_brief": {"type": "array", "items": {"type": "string"}},
    "assumptions": {"type": "array", "items": {"type": "string"}},
    "out_of_scope": {"type": "array", "items": {"type": "string"}},
    "evidence": {"type": "array", "items": {"type": "string"}},
    "risk": {"type": "array", "items": {"type": "string"}},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "next_action": {"const": "handoff_to_enkidu"}
  },
  "additionalProperties": false
}
```

### 2) enkidu_handoff
```json
{
  "type": "object",
  "required": ["schema_version", "task_id", "agent", "summary", "execution_log", "artifacts", "limitations", "risk", "confidence", "next_action"],
  "properties": {
    "schema_version": {"const": "handoff.v1"},
    "task_id": {"type": "string"},
    "agent": {"const": "enkidu"},
    "summary": {"type": "string"},
    "execution_log": {"type": "array", "items": {"type": "string"}},
    "artifacts": {"type": "array", "items": {"type": "string"}},
    "limitations": {"type": "array", "items": {"type": "string"}},
    "risk": {"type": "array", "items": {"type": "string"}},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "next_action": {"const": "handoff_to_taishi"}
  },
  "additionalProperties": false
}
```

### 3) taishi_handoff
```json
{
  "type": "object",
  "required": ["schema_version", "task_id", "agent", "verdict", "scores", "fix_list", "release_blockers", "acceptance_check", "security_check", "next_action"],
  "properties": {
    "schema_version": {"const": "handoff.v1"},
    "task_id": {"type": "string"},
    "agent": {"const": "taishi"},
    "verdict": {"type": "string", "enum": ["pass", "fail", "pass_with_risk"]},
    "scores": {
      "type": "object",
      "required": ["quality", "security", "completeness", "total"],
      "properties": {
        "quality": {"type": "integer", "minimum": 0, "maximum": 5},
        "security": {"type": "integer", "minimum": 0, "maximum": 5},
        "completeness": {"type": "integer", "minimum": 0, "maximum": 5},
        "total": {"type": "integer", "minimum": 0, "maximum": 15}
      },
      "additionalProperties": false
    },
    "fix_list": {"type": "array", "items": {"type": "string"}},
    "release_blockers": {"type": "array", "items": {"type": "string"}},
    "acceptance_check": {"type": "array", "items": {"type": "string"}},
    "security_check": {"type": "array", "items": {"type": "string"}},
    "next_action": {"const": "return_to_jarvis"}
  },
  "additionalProperties": false
}
```

### 4) final_decision
```json
{
  "type": "object",
  "required": ["schema_version", "goal", "outcome", "evidence", "risks_boundaries", "completed", "needs_human_confirmation", "next_steps"],
  "properties": {
    "schema_version": {"const": "final.v1"},
    "goal": {"type": "string"},
    "outcome": {"type": "string"},
    "evidence": {"type": "array", "items": {"type": "string"}},
    "risks_boundaries": {"type": "array", "items": {"type": "string"}},
    "completed": {"type": "array", "items": {"type": "string"}},
    "needs_human_confirmation": {"type": "array", "items": {"type": "string"}},
    "next_steps": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```
