# Research Parallel Mode (v1.1)

## Purpose
Allow controlled parallel exploration in research stage without breaking deterministic mainline execution.

## Scope
- Enabled only in livemore stage.
- Disabled for enkidu/taishi execution stages.

## Execution Model
1. jarvis defines research question set (RQ-1..RQ-n).
2. livemore spawns up to `max_parallel_research=3` sub-tasks.
3. each sub-task returns compact evidence pointers.
4. livemore aggregator merges findings and emits one canonical execution brief.

## Safety Rules
- No external sends in research subtasks.
- No file-destructive actions.
- Must include source confidence per RQ.

## Merge Contract
```json
{
  "task_id": "T-YYYYMMDD-XX",
  "research_parallel": {
    "enabled": true,
    "rq_count": 0,
    "subtasks": [
      {"rq": "RQ-1", "summary": "...", "evidence": ["path#sec"], "confidence": 0.0}
    ],
    "merged_summary": "...",
    "conflicts": ["c1"],
    "final_confidence": 0.0
  }
}
```

## Token Controls
- each subtask max 400 tokens (compact)
- aggregator max 700 tokens
- detail expansion only on conflict items
