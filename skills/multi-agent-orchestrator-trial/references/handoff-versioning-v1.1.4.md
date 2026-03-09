# Handoff Versioning Policy (v1.1.4)

## Purpose
Prevent silent contract drift across multi-agent stage handoffs.

## Required Version Fields
- livemore -> enkidu: `schema_version = "handoff.v1"`
- enkidu -> taishi: `schema_version = "handoff.v1"`
- taishi -> jarvis: `schema_version = "handoff.v1"`
- final decision: `schema_version = "final.v1"`

## Compatibility Rules
1. Minor-compatible upgrades keep prefix and bump patch (`handoff.v1.1`, `handoff.v1.2`).
2. Breaking changes require major bump (`handoff.v2`) and explicit migration entry.
3. Runtime lint must reject unknown major versions by default.

## Migration Requirement
Any schema change must include:
- changed fields list
- migration impact (producers/consumers)
- rollback plan
