# Documentation project instructions

## About this project

- Public docs for the **FocusAlpha Data API** (`https://api.focusalpha.ai`), served at docs.focusalpha.ai
- Built on [Mintlify](https://mintlify.com): MDX pages with YAML frontmatter, configuration in `docs.json`
- The API surface is defined by the `focusalpha-backend` repo (NestJS controllers and DTOs); coverage windows and caveats come from `mcp-server/src/catalog.ts` there — never invent parameters, response fields, coverage dates, or credit costs

## Terminology

- Plans are **Free**, **Professional**, and **Fund** — never "enterprise", "explore", or "internal" in public copy
- Usage is metered in **credits** per call: 1 for most datasets, 2 for retrieval / documents / screeners / 13F / ETFs / news, 0 for the company registry, calendar and discovery/vocabulary endpoints (see concepts/plans-credits.mdx)
- The canonical company identifier is the **`cmp_…` id**; company-scoped routes also accept ticker, CIK, or ISIN
- API keys have the prefix `fa_live_`; use `$FOCUSALPHA_API_KEY` as the placeholder in examples

## Style preferences

- Use active voice and second person ("you")
- Sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, endpoints, and parameters
- Base URL in examples is always `https://api.focusalpha.ai`; auth header is `Authorization: Bearer $FOCUSALPHA_API_KEY`
- Endpoint sections are H2 headings in the form `## GET /v1/...`

## Content boundaries

- Document only customer-facing, API-key-authenticated endpoints
- Never document or mention: internal or administrative endpoints or headers of any kind, dashboard-session endpoints, environment variables, feature flags, deployment infrastructure, or backend source file paths
- No dollar pricing in docs — link to https://app.focusalpha.ai/settings instead
- Never include real API keys, customer IDs, or emails other than support@focusalpha.ai

## Agent-friendliness (keep these in sync on every page change)

- Every dataset page names its MCP tool twice: in frontmatter `keywords` (e.g. `keywords: ["get_guidance"]`) and in the Plan/Credits box (`· **MCP tool:** \`get_guidance\``)
- A new tool gets a row in `mcp-tools.mdx` (tool, what it answers, key arguments, REST endpoint, docs page); a dataset that sounds like another one also gets a row in its "Pick the right tool" table
- `description` says in plain words what question the page answers — it is the line agents read in `llms.txt`
- After adding, renaming or retitling a page, run `python3 scripts/build_llms_txt.py` and commit the regenerated `llms.txt`
- No exact coverage counts (companies, filers, rows, articles, categories) and no "measured on <date>" stamps — they drift. Rounded figures ("about 17,000 listings") are fine
- Claims about data quality and source links must match `concepts/data-quality.mdx`; China and Taiwan statement rows carry no document link yet
