#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import importlib.util

core_path = ROOT / "finance_toolkit" / "core.py"
spec = importlib.util.spec_from_file_location("finance_core", core_path)
finance_core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finance_core)
get_market_data = finance_core.get_market_data
validate_data = finance_core.validate_data


def classify_status(data: dict, quality: dict):
    issues = []
    codes = []

    if not quality.get("is_valid", False):
        codes.append("validation_failed")

    if not data.get("gold"):
        codes.append("empty_gold")
    if not data.get("a_shares"):
        codes.append("empty_a_shares")

    exchange = data.get("exchange", {})
    if exchange.get("source") == "备用值":
        codes.append("exchange_fallback")

    issues.extend(quality.get("issues", []))

    if "validation_failed" in codes or ("empty_gold" in codes and "empty_a_shares" in codes):
        return "fail", codes, issues
    if codes:
        return "partial", codes, issues
    return "success", codes, issues


def main():
    now = datetime.utcnow()
    data = get_market_data()
    quality = validate_data(data)
    status, codes, issues = classify_status(data, quality)

    out = {
        "timestamp": now.isoformat() + "Z",
        "status": status,
        "failure_codes": codes,
        "quality": quality,
        "issues": issues,
        "data": data,
    }

    fn = f"market_snapshot_{now.strftime('%Y%m%d_%H%M%S')}_{status}.json"
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(fn)


if __name__ == "__main__":
    main()
