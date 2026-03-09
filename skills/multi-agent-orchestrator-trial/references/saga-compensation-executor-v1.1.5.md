# Saga Compensation Executor (v1.1.5)

## Goal
Execute compensating actions when a stage fails, with idempotent and auditable behavior.

## Manifest Input
`compensation_manifest.json`:
```json
{
  "task_id": "T-...",
  "stage": "enkidu",
  "changed_files": ["a.py", "b.py"],
  "notes": ["optional"]
}
```

## Behavior
- Default mode: dry-run (no file changes)
- Apply mode: restore changed files to `HEAD` (requires explicit confirm token)
- Path safety: block absolute paths, `..`, `.git/`, and untracked files
- Always emit `compensation_report.json`

## Safety
- Never bypass human confirmation gates
- If compensation fails twice -> escalate `REQUEST_HUMAN_DECISION`

## Script
Use:
- `scripts/run_saga_compensation_v1_1_5.py`
