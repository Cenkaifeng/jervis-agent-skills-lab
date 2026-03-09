---
name: crawl-supabase-base
description: End-to-end web data collection base (browser automation + structured extraction + persistence). Use when you need a reusable pipeline to: (1) browse dynamic pages (login, infinite scroll, JS rendering), (2) extract page content into a strict JSON schema, and (3) upsert results + cursors into Supabase/Postgres for traceability, incremental crawling, and audit.
---

# Crawl Supabase Base

## What this skill is
A standard “tool base” for agents to do web collection as a pipeline:

1) **Navigate** (dynamic web, login/session, pagination) via OpenClaw browser tooling
2) **Extract** (page → JSON) with strict schemas
3) **Store** (upsert + cursors + evidence pointers) in **Supabase (Postgres)**

Use it whenever you want crawling to be **repeatable, incremental, and auditable**.

## Quick start (recommended workflow)

### 0) Prereqs
- Configure Supabase secrets (see `references/SUPABASE.md`).
- Decide your target schema (start from `references/SCHEMAS.md`).

### 1) Browse / fetch the page (dynamic friendly)
- Prefer OpenClaw `browser` tool for sites with JS rendering, login, or anti-bot friction.
- Save the canonical URL and the timestamp.

### 2) Extract page → JSON
- Use `scripts/extract_json.js` with a schema name.
- Output MUST include `source_url` and `observed_at`.

### 3) Upsert into Supabase + write cursor
- Use `scripts/supabase_upsert.js` to write:
  - entity rows (e.g., product)
  - observation rows (immutable snapshots)
  - cursor updates (incremental)

## Failure handling conventions
- Always store failures in `errors` table (or log file) with: `run_id`, `stage` (navigate|extract|store), `url`, `error_class`, `message`.
- For anti-bot / transient failures: backoff + retry; for schema failures: store raw excerpt + mark `needs_fix`.

## Bundled resources
- `references/SUPABASE.md`: how to obtain Supabase connection info + recommended permissions
- `references/SCHEMAS.md`: baseline tables + JSON schemas
- `scripts/extract_json.js`: schema-driven extraction helper (agent-assisted extraction)
- `scripts/supabase_upsert.js`: minimal Supabase REST upsert client (no external deps)
