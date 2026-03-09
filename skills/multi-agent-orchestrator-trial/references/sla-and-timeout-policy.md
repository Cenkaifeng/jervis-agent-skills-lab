# SLA and Timeout Policy (v0.4)

## Default Stage Budgets (L2)
- jarvis planning: 5 min
- livemore research/scoping: 10 min
- enkidu execution: 20 min
- taishi audit: 8 min
- jarvis final synthesis: 5 min

Target end-to-end (L2): <= 48 min

## Budget by Task Class

### L1
- Skip livemore stage
- Target end-to-end: <= 30 min

### L2
- Full serial chain
- Target end-to-end: <= 48 min

### L3
- Full chain + one controlled enkidu fix loop
- Target end-to-end: <= 75 min

## Timeout Handling

If a stage exceeds budget:
1. Mark stage as `TIMEOUT` with current partial output.
2. Retry same stage once with reduced scope.
3. If second timeout, escalate to jarvis with options:
   - A) continue with degraded confidence
   - B) request user decision
   - C) abort with blockers report

## Scope Reduction Rules (for retry)
- Keep acceptance criteria fixed.
- Drop non-critical enhancements first.
- Preserve security/compliance checks; do not skip taishi.

## Escalation Payload (TIMEOUT)
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "stage": "livemore|enkidu|taishi",
  "status": "TIMEOUT",
  "elapsed_min": 0,
  "partial_result": ["what is done"],
  "remaining_work": ["what is left"],
  "options": ["degraded_continue", "user_decision", "abort"],
  "recommended_option": "user_decision"
}
```
