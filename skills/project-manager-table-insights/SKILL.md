---
name: project-manager-table-insights
description: Read spreadsheet files (CSV/XLSX), identify project status, risks, blockers, owners, and deadlines, then output project-manager style summaries and action plans. Use when users ask to analyze table data, generate progress reports, find delays, prioritize tasks, or produce PM updates from tabular project data.
---

# Project Manager Table Insights

Use this skill to convert tabular project data into PM-ready outputs.

## Workflow

1. Inspect input file type and columns.
2. Run the analyzer script to generate a structured JSON result.
3. Convert the JSON into the user-requested format (daily report / weekly update / risk log / stakeholder brief).
4. If key fields are missing, state assumptions clearly.

## Run analyzer

Use this script:

```bash
python3 skills/project-manager-table-insights/scripts/pm_table_analyzer.py \
  --input <path/to/file.csv_or_xlsx> \
  --output <path/to/result.json>
```

Optional parameters:

- `--encoding utf-8` (for CSV)
- `--sheet <sheet_name>` (for XLSX)

## Generate PM report (Markdown)

After analyzer output is generated, render a PM-style report:

```bash
python3 skills/project-manager-table-insights/scripts/generate_pm_report.py \
  --input <path/to/result.json> \
  --output <path/to/weekly-report.md> \
  --title "项目周报"
```

## Expected columns (best effort mapping)

The script auto-maps common Chinese/English columns:

- Task name: `任务`, `事项`, `task`, `title`
- Owner: `负责人`, `owner`, `assignee`
- Status: `状态`, `status`
- Priority: `优先级`, `priority`
- Start date: `开始时间`, `start_date`
- Due date: `截止时间`, `due_date`, `deadline`
- Progress: `进度`, `progress`
- Risk: `风险`, `risk`
- Blocker: `阻塞`, `blocker`, `issue`

If no direct match exists, use fuzzy partial matching on headers.

## Output guidance

Always provide these PM sections when possible:

1. Overall health (on-track / at-risk / delayed)
2. Milestone and deadline view
3. Top risks and blockers
4. Priority next actions (owner + deadline)
5. Suggested stakeholder update (short, executive-friendly)

## Report templates

For polished output patterns, read:

- `references/output-templates.md`
