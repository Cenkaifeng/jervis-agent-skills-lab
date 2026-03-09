#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

CONFIRM_TOKEN = "I_UNDERSTAND_APPLY_RESTORE"


def is_safe_relpath(p: str) -> bool:
    return not (p.startswith("/") or ".." in Path(p).parts or p.startswith(".git/"))


def is_git_tracked(repo: Path, rel: str) -> bool:
    proc = subprocess.run(["git", "ls-files", "--error-unmatch", "--", rel], cwd=repo, capture_output=True, text=True)
    return proc.returncode == 0


def main():
    ap = argparse.ArgumentParser(description="Run saga compensation for changed files")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo-root", default="/root/.openclaw/workspace")
    ap.add_argument("--apply", action="store_true", help="apply restore to HEAD (default dry-run)")
    ap.add_argument("--confirm-apply", default="", help="required when --apply. must equal I_UNDERSTAND_APPLY_RESTORE")
    args = ap.parse_args()

    if args.apply and args.confirm_apply != CONFIRM_TOKEN:
        raise SystemExit("--apply requires --confirm-apply I_UNDERSTAND_APPLY_RESTORE")

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    repo = Path(args.repo_root).resolve()
    changed = manifest.get("changed_files", [])

    actions = []
    status = "COMPENSATED"

    for f in changed:
        if not is_safe_relpath(f):
            actions.append(f"blocked_unsafe_path:{f}")
            status = "COMPENSATION_FAILED"
            continue

        fp = (repo / f).resolve()
        try:
            fp.relative_to(repo)
        except ValueError:
            actions.append(f"blocked_outside_repo:{f}")
            status = "COMPENSATION_FAILED"
            continue

        if not fp.exists():
            actions.append(f"skip_missing:{f}")
            continue

        if not is_git_tracked(repo, f):
            actions.append(f"blocked_untracked:{f}")
            status = "COMPENSATION_FAILED"
            continue

        if args.apply:
            cmd = ["git", "restore", "--source", "HEAD", "--", f]
            p = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
            if p.returncode == 0:
                actions.append(f"restored:{f}")
            else:
                actions.append(f"restore_failed:{f}:{p.stderr.strip()}")
                status = "COMPENSATION_FAILED"
        else:
            actions.append(f"dryrun_restore:{f}")

    report = {
        "task_id": manifest.get("task_id", "UNKNOWN"),
        "stage": manifest.get("stage", "unknown"),
        "status": status,
        "trigger": manifest.get("trigger", "non_timeout_fail"),
        "actions": actions,
        "artifacts": [str(Path(args.out).name)],
        "next_action": "retry" if status == "COMPENSATED" else "escalate",
    }
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
