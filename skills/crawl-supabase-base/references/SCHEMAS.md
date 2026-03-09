# Baseline schemas (suggested)

This skill base assumes a **3-table** minimal pattern:

## 1) entities (current state)
Example: `products`
- natural key: `source` + `external_id` (or canonical URL hash)
- columns: title/price/stock/seller/etc
- last_seen_at

## 2) observations (append-only snapshots)
Example: `product_observations`
- `product_id` FK
- `observed_at`
- `payload` (jsonb)
- `source_url`

## 3) cursors (incremental progress)
Example: `cursors`
- `scope` (site/category/query)
- `cursor` (string/json)
- `updated_at`

## Common fields
- `run_id` (string/uuid) to trace a pipeline execution
- `schema_version` (int)

## Extraction JSON conventions
All extracted JSON must include:
- `source_url` (string)
- `observed_at` (ISO-8601 string)
- `schema` (string)
- `schema_version` (int)
