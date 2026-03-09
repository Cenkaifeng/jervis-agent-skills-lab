#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path


def build_summary(payload: dict) -> dict:
    data = payload.get("data", {})
    quality = payload.get("quality", {})
    return {
        "status": payload.get("status", "unknown"),
        "failure_codes": payload.get("failure_codes", []),
        "is_valid": quality.get("is_valid", False),
        "issue_count": len(payload.get("issues", []) or []),
        "gold_items": len(data.get("gold", {}) or {}),
        "a_share_items": len(data.get("a_shares", {}) or {}),
        "exchange_source": (data.get("exchange", {}) or {}).get("source", "unknown"),
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: render_html_report.py <input.json> <output.html>")
        sys.exit(1)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    tpl = Path(__file__).resolve().parent.parent / "assets" / "templates" / "daily_report.html"

    payload = json.loads(src.read_text(encoding="utf-8"))
    summary = build_summary(payload)

    html = tpl.read_text(encoding="utf-8")
    html = html.replace("{{generated_at}}", datetime.utcnow().isoformat() + "Z")
    html = html.replace("{{status}}", summary["status"])
    html = html.replace("{{is_valid}}", str(summary["is_valid"]))
    html = html.replace("{{failure_codes}}", ", ".join(summary["failure_codes"]) or "none")
    html = html.replace("{{gold_items}}", str(summary["gold_items"]))
    html = html.replace("{{a_share_items}}", str(summary["a_share_items"]))
    html = html.replace("{{exchange_source}}", summary["exchange_source"])
    html = html.replace("{{issue_count}}", str(summary["issue_count"]))

    out.write_text(html, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
