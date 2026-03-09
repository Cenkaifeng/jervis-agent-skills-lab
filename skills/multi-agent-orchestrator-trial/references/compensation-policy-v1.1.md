# Compensation Policy (v1.1)

## Purpose
Define reversible actions for each stage when orchestration fails or requires rollback.

## Stage Compensation Map

### jarvis (planning/orchestration)
- Failure type: invalid plan, wrong routing, budget breach
- Compensation:
  1. Mark current plan as `REVOKED`
  2. Emit corrected minimal plan
  3. Reset downstream execution tokens

### livemore (research/scoping)
- Failure type: invalid assumptions, stale evidence, scope drift
- Compensation:
  1. Invalidate outdated evidence pointers
  2. Re-issue execution brief with changed assumptions highlighted
  3. Preserve unchanged assumptions as stable baseline

### enkidu (execution)
- Failure type: bad file changes, failed script ops, unsafe side effects
- Compensation:
  1. Revert modified files to pre-task checkpoint (git restore / backup snapshot)
  2. Emit rollback report with file list
  3. Re-run only corrected delta steps

### taishi (review/audit)
- Failure type: scoring contract mismatch, false pass, missed blocker
- Compensation:
  1. Force verdict=`fail`
  2. Emit `[P0] audit_contract_failure`
  3. Require second-pass review (or dual-review if L3)

## Compensation Contract
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "stage": "jarvis|livemore|enkidu|taishi",
  "status": "COMPENSATED|COMPENSATION_FAILED",
  "trigger": "timeout|non_timeout_fail|manual_abort",
  "actions": ["action1", "action2"],
  "artifacts": ["path#section"],
  "next_action": "retry|escalate|abort"
}
```

## Rules
1. Compensation must be idempotent.
2. Compensation cannot bypass human confirmation gates.
3. If compensation fails twice, escalate to `REQUEST_HUMAN_DECISION`.
