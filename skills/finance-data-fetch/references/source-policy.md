# Source Policy (v1)

- Primary (gold): Yahoo Finance API (`XAUUSD=X`)
- Fallback (gold): `api.gold-api.com/price/XAU` -> `stooq.com/q/l/?s=xauusd&i=d`
- Primary (FX): ExchangeRate-API
- If all sources fail: mark missing/degraded; do not estimate random values
- Log source, latency, retry count, and fallback_used
