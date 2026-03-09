---
name: finance-data-fetch
description: Fetch finance market data (gold, A-share indices, FX, news) with unified retry/timeout/fallback policy and normalized JSON output. Use when building or running data collection pipelines, replacing duplicated fetch logic across scripts.
---

# Finance Data Fetch

1. Prefer shared functions from `finance_toolkit/core.py` before writing new fetchers.
2. Keep data source policy explicit: primary source, fallback source, failure behavior.
3. Never fabricate market data in production output.
4. Output normalized JSON fields:
   - `symbol`, `current`, `change`, `change_pct`, `time`, `source`, `quality`
5. When source fails, return `quality=degraded` and include reason.

## Scripts
- `scripts/fetch_market_snapshot.py`: wrapper that calls finance_toolkit and writes JSON snapshot.

## References
- `references/source-policy.md`: approved source/fallback matrix.
