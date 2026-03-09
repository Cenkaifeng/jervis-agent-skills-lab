# Supabase connection info (where to get it)

You will need **at least**:
- `SUPABASE_URL` (Project URL)
- `SUPABASE_SERVICE_ROLE_KEY` (server-side key; keep secret)

Optional (nice to have):
- Direct Postgres connection string / pooler info for bulk operations
- Storage bucket name for evidence (HTML/screenshot)

## Where to find these in Supabase dashboard

1) **Project URL + anon key**
- Supabase Dashboard → **Project Settings** → **API**
  - **Project URL** → use as `SUPABASE_URL`
  - **Project API keys** → `anon` key (NOT enough for server-side upserts unless RLS policies allow it)

2) **Service role key (recommended for this skill base)**
- Same page: **Project Settings → API**
  - **service_role** key → use as `SUPABASE_SERVICE_ROLE_KEY`
- Treat it like root: do not paste into public repos.

3) **Database connection string** (optional)
- Supabase Dashboard → **Project Settings** → **Database**
  - Connection string / host / port / db name / password
- Alternatively use the **Connection Pooler** settings if enabled.

4) **Storage bucket** (optional)
- Supabase Dashboard → **Storage** → create/select bucket
  - Store evidence files (HTML, screenshots, raw JSON) keyed by run_id.

## Recommended secret handling

Put secrets into environment variables (do NOT commit):
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

Example:
```bash
export SUPABASE_URL="https://xxxx.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="<service_role>"
```

If using OpenClaw gateway service env, prefer putting them in the service environment rather than hardcoding.
