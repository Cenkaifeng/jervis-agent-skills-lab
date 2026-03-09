#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, date
from pathlib import Path


def _normalize(s):
    return str(s).strip().lower().replace(" ", "").replace("_", "")


def _pick_column(columns, candidates):
    norm_map = {_normalize(c): c for c in columns}
    for cand in candidates:
        nc = _normalize(cand)
        if nc in norm_map:
            return norm_map[nc]
    # fuzzy contains
    for c in columns:
        nc = _normalize(c)
        for cand in candidates:
            if _normalize(cand) in nc or nc in _normalize(cand):
                return c
    return None


def _to_date(v):
    if v in (None, ""):
        return None
    if isinstance(v, (datetime, date)):
        return v.date() if isinstance(v, datetime) else v
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def _clean_text(v):
    if v is None:
        return ""
    s = str(v).strip()
    if s.lower() in ("", "nan", "none", "null", "nat"):
        return ""
    return s


def _to_progress(v):
    if v in (None, ""):
        return None
    s = str(v).strip().replace("%", "")
    if s.lower() in ("nan", "none", "null", "nat"):
        return None
    try:
        x = float(s)
        if x <= 1:
            x *= 100
        return max(0, min(100, round(x, 1)))
    except ValueError:
        return None


def load_dataframe(path, sheet=None, encoding="utf-8"):
    suffix = Path(path).suffix.lower()
    try:
        import pandas as pd
    except Exception as e:
        raise RuntimeError("pandas is required. Install with: pip install pandas openpyxl") from e

    if suffix == ".csv":
        return pd.read_csv(path, encoding=encoding)
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path, sheet_name=sheet)
    raise ValueError(f"Unsupported file type: {suffix}")


def main():
    parser = argparse.ArgumentParser(description="Analyze project table and generate PM insights")
    parser.add_argument("--input", required=True, help="CSV/XLSX file path")
    parser.add_argument("--output", required=True, help="JSON output path")
    parser.add_argument("--sheet", default=None, help="Sheet name for XLSX")
    parser.add_argument("--encoding", default="utf-8", help="CSV encoding")
    args = parser.parse_args()

    df = load_dataframe(args.input, sheet=args.sheet, encoding=args.encoding)
    columns = list(df.columns)

    c_task = _pick_column(columns, ["任务", "事项", "task", "title", "工作项"])
    c_owner = _pick_column(columns, ["负责人", "owner", "assignee"])
    c_status = _pick_column(columns, ["状态", "status"])
    c_priority = _pick_column(columns, ["优先级", "priority"])
    c_start = _pick_column(columns, ["开始时间", "start", "start_date"])
    c_due = _pick_column(columns, ["截止时间", "deadline", "due", "due_date"])
    c_progress = _pick_column(columns, ["进度", "progress"])
    c_risk = _pick_column(columns, ["风险", "risk"])
    c_blocker = _pick_column(columns, ["阻塞", "blocker", "issue", "卡点"])

    today = date.today()
    records = []
    delayed = 0
    at_risk = 0

    for _, row in df.iterrows():
        task = _clean_text(row.get(c_task, "")) if c_task else ""
        owner = _clean_text(row.get(c_owner, "")) if c_owner else ""
        status = _clean_text(row.get(c_status, "")) if c_status else ""
        priority = _clean_text(row.get(c_priority, "")) if c_priority else ""
        risk = _clean_text(row.get(c_risk, "")) if c_risk else ""
        blocker = _clean_text(row.get(c_blocker, "")) if c_blocker else ""

        due = _to_date(row.get(c_due)) if c_due else None
        progress = _to_progress(row.get(c_progress)) if c_progress else None

        is_delayed = bool(due and due < today and (progress is None or progress < 100))
        is_at_risk = bool((risk and risk.lower() not in ("none", "", "低")) or blocker)

        if is_delayed:
            delayed += 1
        if is_at_risk:
            at_risk += 1

        records.append(
            {
                "task": task,
                "owner": owner,
                "status": status,
                "priority": priority,
                "due_date": due.isoformat() if due else None,
                "progress": progress,
                "risk": risk,
                "blocker": blocker,
                "is_delayed": is_delayed,
                "is_at_risk": is_at_risk,
            }
        )

    total = len(records)
    if total == 0:
        health = "unknown"
    elif delayed / total > 0.2:
        health = "delayed"
    elif (delayed + at_risk) / total > 0.3:
        health = "at_risk"
    else:
        health = "on_track"

    high_priority = [r for r in records if _normalize(r.get("priority", "")) in ("p0", "p1", "high", "高")]
    next_actions = sorted(
        [r for r in records if r["is_delayed"] or r["is_at_risk"]],
        key=lambda x: (x.get("due_date") or "9999-12-31"),
    )[:10]

    result = {
        "summary": {
            "total_tasks": total,
            "delayed_tasks": delayed,
            "at_risk_tasks": at_risk,
            "health": health,
            "high_priority_tasks": len(high_priority),
            "generated_at": datetime.utcnow().isoformat() + "Z",
        },
        "mapped_columns": {
            "task": c_task,
            "owner": c_owner,
            "status": c_status,
            "priority": c_priority,
            "start": c_start,
            "due": c_due,
            "progress": c_progress,
            "risk": c_risk,
            "blocker": c_blocker,
        },
        "next_actions": next_actions,
        "records": records,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
