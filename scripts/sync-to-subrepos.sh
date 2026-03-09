#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INDEX="$ROOT/manifests/skills-index.yaml"

echo "[sync] planned source of truth: $INDEX"
echo "[sync] TODO: implement per-skill subrepo sync according to skills-index.yaml"
echo "[sync] example flow: export skill -> clone subrepo -> rsync -> commit -> push"
