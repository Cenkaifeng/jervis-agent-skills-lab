---
name: finance-daily-orchestrator
description: Orchestrate daily finance pipeline steps (fetch -> validate -> render -> deliver) with retries, idempotency, and alert hooks. Use when replacing ad-hoc cron scripts with a controlled workflow.
---

# Finance Daily Orchestrator

1. Execute stages in strict order: fetch, validate, render, deliver.
2. Assign idempotency key by date/time window to prevent duplicate delivery.
3. Fail fast on critical missing data; degrade gracefully on non-critical sections.
4. Emit run summary including status, retries, and output artifacts.

## Scripts
- `scripts/run_daily_pipeline.sh`

## References
- `references/runbook.md`
