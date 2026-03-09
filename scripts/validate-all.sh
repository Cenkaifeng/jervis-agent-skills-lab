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

  if [ ! -f "$skill_file" ]; then
    echo "[x] $name: missing SKILL.md"
    failed=1
    continue
  fi

  if ! grep -q '^name:' "$skill_file"; then
    echo "[x] $name: frontmatter missing name"
    failed=1
  fi

  if ! grep -q '^description:' "$skill_file"; then
    echo "[x] $name: frontmatter missing description"
    failed=1
  fi

done

if [ "$failed" -ne 0 ]; then
  echo "[validate] failed"
  exit 1
fi

echo "[validate] ok"
