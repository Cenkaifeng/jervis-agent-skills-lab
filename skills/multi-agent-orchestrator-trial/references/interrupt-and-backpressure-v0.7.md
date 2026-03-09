# Interrupt & Backpressure Policy (v0.7)

## Problem Scenario
When a long-running task is in progress, a new urgent task is inserted (加塞). This may cause:
- delayed responses
- low-value padding updates
- context drift and retry waste

## Control Model
Use a single active pipeline + explicit queue:
- one task in `RUNNING`
- others in `QUEUED`
- urgent tasks can preempt only at safe checkpoints

## Task Priority
- P0: emergency/security/production blocker
- P1: high urgency user-requested
- P2: normal work

## Preemption Rule
A queued task may preempt only if:
1. priority of new task is higher than running task, and
2. running stage reaches checkpoint boundary (`stage_end`), and
3. jarvis emits state snapshot before switch.

No hard preempt in the middle of a stage execution.

## Checkpoint Snapshot Contract
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "status": "PAUSED_FOR_PREEMPT",
  "stage": "livemore|enkidu|taishi|jarvis",
  "progress": "short progress summary",
  "artifact_index": ["path#section"],
  "resume_hint": ["next step 1", "next step 2"],
  "eta_remaining_min": 0
}
```

## Anti-Padding Response Policy
During long tasks, avoid frequent low-value updates. Only send updates when one of these triggers occurs:
- stage completed
- risk/blocker detected
- preemption happened
- human confirmation needed
- timeout/escalation

Heartbeat-style update format (max 4 bullets):
1. current stage
2. done since last update
3. blocker/risk (if any)
4. next checkpoint ETA

## Resume Rule
When interrupted task resumes:
1. load latest checkpoint snapshot
2. continue from `resume_hint`
3. do not regenerate finished stage outputs
4. apply delta-only output policy

## Queue Discipline
- default scheduling: highest priority first, then FIFO
- starvation guard: if a P2 task waits too long, jarvis must request user decision to continue defer/preempt policy.
