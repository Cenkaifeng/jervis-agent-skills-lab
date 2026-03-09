---
name: finance-report-render
description: Render normalized finance JSON data into consistent report outputs (HTML/email text) using reusable templates. Use when generating daily or intraday reports without duplicating HTML in Python scripts.
---

# Finance Report Render

1. Keep templates in `assets/templates/`.
2. Keep renderer script pure (input JSON -> output HTML/text).
3. Separate data fetch from rendering.
4. Mark missing data explicitly in report sections.

## Scripts
- `scripts/render_html_report.py`

## Assets
- `assets/templates/daily_report.html`
