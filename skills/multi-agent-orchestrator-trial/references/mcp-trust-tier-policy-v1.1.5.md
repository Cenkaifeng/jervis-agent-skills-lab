# MCP Trust Tier Policy (v1.1.5)

## Goal
Apply zero-trust controls for MCP tools/servers.

## Tiers
- **Trusted**: vetted internal servers
- **Restricted**: external but reviewed servers
- **Untrusted**: unknown/new servers

## Capability Matrix
| Action | Trusted | Restricted | Untrusted |
|---|---|---|---|
| Read-only tool calls | ✅ | ✅ | ✅ (sandboxed) |
| File write operations | ✅ | ✅ (allowlist paths) | ❌ |
| External sends/public actions | ✅ (with human gate) | ❌ | ❌ |
| Permission/config mutation | ✅ (with human gate) | ❌ | ❌ |

## Required Metadata
Each MCP call should log:
- `server_id`
- `trust_tier`
- `tool_name`
- `requested_action`
- `approved_by_gate` (boolean)

## Default Rule
Unknown MCP server defaults to `Untrusted`.
