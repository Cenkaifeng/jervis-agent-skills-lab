#!/usr/bin/env node
/**
 * Minimal Supabase REST upsert helper (no deps)
 * Uses SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY.
 *
 * Examples:
 *  node supabase_upsert.js upsert products '{"source":"x","external_id":"1","title":"t"}' --on=source,external_id
 *  node supabase_upsert.js insert product_observations '{"product_id":1,"observed_at":"...","payload":{...}}'
 */

function die(msg) {
  console.error(msg);
  process.exit(1);
}

const [,, cmd, table, jsonStr, ...rest] = process.argv;
if (!cmd || !table || !jsonStr) {
  die('Usage: supabase_upsert.js <upsert|insert> <table> <json> [--on=col1,col2]');
}

const SUPABASE_URL = process.env.SUPABASE_URL;
const KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !KEY) {
  die('Missing env: SUPABASE_URL and/or SUPABASE_SERVICE_ROLE_KEY');
}

let body;
try { body = JSON.parse(jsonStr); } catch { die('Invalid JSON'); }

const onArg = rest.find(x => x.startsWith('--on='));
const onConflict = onArg ? onArg.slice('--on='.length) : null;

const url = new URL(`${SUPABASE_URL.replace(/\/$/, '')}/rest/v1/${table}`);
if (cmd === 'upsert') {
  url.searchParams.set('on_conflict', onConflict || 'id');
}

const headers = {
  'apikey': KEY,
  'Authorization': `Bearer ${KEY}`,
  'Content-Type': 'application/json',
  'Prefer': cmd === 'upsert' ? 'resolution=merge-duplicates,return=representation' : 'return=representation',
};

const method = 'POST';
const payload = Array.isArray(body) ? body : [body];

(async () => {
  const res = await fetch(url, { method, headers, body: JSON.stringify(payload) });
  const txt = await res.text();
  if (!res.ok) {
    die(`Supabase REST error ${res.status}: ${txt}`);
  }
  console.log(txt || '[]');
})();
