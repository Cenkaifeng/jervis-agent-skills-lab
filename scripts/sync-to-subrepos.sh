#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INDEX="$ROOT/manifests/skills-index.yaml"
FILTER_SKILL="${1:-}"
WORKDIR="$ROOT/.tmp/sync"
mkdir -p "$WORKDIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[sync] python3 is required"
  exit 1
fi

mapfile -t ENTRIES < <(python3 - "$INDEX" <<'PY'
import sys
from pathlib import Path
idx=Path(sys.argv[1])
try:
    import yaml
except Exception:
    print("__PY_YAML_MISSING__")
    raise SystemExit(0)

data=yaml.safe_load(idx.read_text(encoding='utf-8')) or {}
for s in data.get('skills', []):
    sub=s.get('subrepo') or {}
    if sub.get('enabled'):
        name=s.get('name','')
        path=s.get('path',f"skills/{name}")
        repo=sub.get('repo')
        branch=sub.get('branch','main')
        if repo:
            print(f"{name}\t{path}\t{repo}\t{branch}")
PY
)

if [[ "${#ENTRIES[@]}" -eq 1 && "${ENTRIES[0]}" == "__PY_YAML_MISSING__" ]]; then
  echo "[sync] missing dependency: pyyaml (pip install pyyaml)"
  exit 1
fi

if [ "${#ENTRIES[@]}" -eq 0 ]; then
  echo "[sync] no enabled subrepo mappings in $INDEX"
  exit 0
fi

synced=0
for line in "${ENTRIES[@]}"; do
  IFS=$'\t' read -r name path repo branch <<<"$line"

  if [ -n "$FILTER_SKILL" ] && [ "$name" != "$FILTER_SKILL" ]; then
    continue
  fi

  SRC="$ROOT/$path"
  if [ ! -d "$SRC" ]; then
    echo "[sync] skip $name: source not found ($SRC)"
    continue
  fi

  target="$WORKDIR/$name"
  rm -rf "$target"

  repo_url="https://${repo#https://}"
  if git clone --depth 1 --branch "$branch" "$repo_url" "$target" >/dev/null 2>&1; then
    :
  else
    # fallback for empty repos or missing branch
    git clone "$repo_url" "$target" >/dev/null 2>&1 || git clone "$repo_url" "$target"
    pushd "$target" >/dev/null
    git checkout -B "$branch" >/dev/null 2>&1 || true
    popd >/dev/null
  fi

  find "$target" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  rsync -a --delete --exclude='.git' "$SRC/" "$target/"

  pushd "$target" >/dev/null
  if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "chore(sync): update $name from jervis-agent-skills-lab"
    git push origin "$branch"
    echo "[sync] pushed $name -> $repo@$branch"
    synced=$((synced+1))
  else
    echo "[sync] no changes for $name"
  fi
  popd >/dev/null

done

echo "[sync] done, pushed $synced skill(s)"
