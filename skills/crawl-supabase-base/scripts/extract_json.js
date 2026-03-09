#!/usr/bin/env node
/**
 * Placeholder extraction helper.
 * In practice: agent gets page content via OpenClaw browser/web_fetch,
 * then produces JSON matching a chosen schema.
 *
 * This script currently wraps input into the standard envelope so storage is consistent.
 */

function die(msg){ console.error(msg); process.exit(1); }

const [,, schema, sourceUrl, rawText] = process.argv;
if (!schema || !sourceUrl) {
  die('Usage: extract_json.js <schema> <source_url> [raw_text]');
}

const observed_at = new Date().toISOString();
const schema_version = 1;

const out = {
  schema,
  schema_version,
  source_url: sourceUrl,
  observed_at,
  raw_excerpt: rawText ? String(rawText).slice(0, 2000) : undefined,
};

console.log(JSON.stringify(out, null, 2));
