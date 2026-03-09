#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$ROOT/skills"

echo "[validate] scanning skills in $SKILLS_DIR"

if [ ! -d "$SKILLS_DIR" ]; then
  echo "[validate] skills directory not found"
  exit 1
fi

failed=0

for d in "$SKILLS_DIR"/*; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  skill_file="$d/SKILL.md"

  # 1) skill dir naming
  if ! [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "[x] $name: directory name must be kebab-case"
    failed=1
  fi

  # 2) required file
  if [ ! -f "$skill_file" ]; then
    echo "[x] $name: missing SKILL.md"
    failed=1
    continue
  fi

  # 3) forbid obvious external markers
  if [ -f "$d/.clawhub/origin.json" ]; then
    echo "[x] $name: external-source marker found (.clawhub/origin.json)"
    failed=1
  fi

  # 4) forbid noisy files that violate local standard
  for f in README.md CHANGELOG.md PUBLISH.md PUBLISHING_CHECKLIST.md CHANNELLOG.md; do
    if [ -f "$d/$f" ]; then
      echo "[x] $name: forbidden file $f"
      failed=1
    fi
  done

  if find "$d" -type d -name '__pycache__' | grep -q .; then
    echo "[x] $name: contains __pycache__"
    failed=1
  fi
  if find "$d" -type f -name '*.pyc' | grep -q .; then
    echo "[x] $name: contains .pyc files"
    failed=1
  fi

  # 5) top-level structure allowlist
  while IFS= read -r item; do
    base="$(basename "$item")"
    case "$base" in
      SKILL.md|scripts|references|assets) ;;
      *)
        echo "[x] $name: unexpected top-level entry '$base'"
        failed=1
        ;;
    esac
  done < <(find "$d" -mindepth 1 -maxdepth 1)

  # 6) frontmatter checks: name + description + name match dir
  if ! python3 - "$skill_file" "$name" <<'PY'
import sys
from pathlib import Path

p = Path(sys.argv[1])
dir_name = sys.argv[2]
text = p.read_text(encoding='utf-8', errors='replace')
lines = text.splitlines()

if len(lines) < 3 or lines[0].strip() != '---':
    print(f"[x] {dir_name}: missing YAML frontmatter")
    raise SystemExit(1)

end = None
for i in range(1, len(lines)):
    if lines[i].strip() == '---':
        end = i
        break
if end is None:
    print(f"[x] {dir_name}: frontmatter not closed")
    raise SystemExit(1)

fm = lines[1:end]
name = None
desc = None
for line in fm:
    s = line.strip()
    if s.startswith('name:'):
        name = s.split(':',1)[1].strip().strip('"\'')
    elif s.startswith('description:'):
        desc = s.split(':',1)[1].strip().strip('"\'')

ok = True
if not name:
    print(f"[x] {dir_name}: frontmatter missing name")
    ok = False
elif name != dir_name:
    print(f"[x] {dir_name}: frontmatter name '{name}' must match directory")
    ok = False

if not desc or len(desc) < 20:
    print(f"[x] {dir_name}: description missing or too short")
    ok = False

raise SystemExit(0 if ok else 1)
PY
  then
    failed=1
  fi

done

if [ "$failed" -ne 0 ]; then
  echo "[validate] failed"
  exit 1
fi

echo "[validate] ok"
