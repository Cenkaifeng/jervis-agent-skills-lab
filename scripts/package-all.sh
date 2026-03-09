#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
SKILLS_DIR="$ROOT/skills"

mkdir -p "$DIST"

"$ROOT/scripts/validate-all.sh"

echo "[package] creating lightweight tarballs (placeholder for .skill packaging)"
for d in "$SKILLS_DIR"/*; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  tar -czf "$DIST/${name}.tar.gz" -C "$SKILLS_DIR" "$name"
  echo "[package] $name -> dist/${name}.tar.gz"
done

echo "[package] done"
