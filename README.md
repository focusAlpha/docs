# FocusAlpha docs

Source for [docs.focusalpha.ai](https://docs.focusalpha.ai) — public documentation for the FocusAlpha Data API (`api.focusalpha.ai`), built on [Mintlify](https://mintlify.com).

## Structure

```
docs.json            # Site config: navigation, branding, navbar/footer
index.mdx            # Introduction
quickstart.mdx       # Key creation + first request
authentication.mdx   # API keys, headers, security
concepts/            # Plans & credits, rate limits, errors, pagination,
                     # company identifiers, coverage & freshness
api-reference/       # One page per endpoint group
```

## Local preview

```bash
npm i -g mint
mint dev            # http://localhost:3000
```

## Publishing

Pushes to `main` deploy to production automatically via the Mintlify GitHub app. Open a PR to get a preview deployment first.

## Keeping docs accurate

The API surface is defined by the `focusalpha-backend` repo (NestJS controllers + DTOs). When endpoints change there, update the matching page here. Per-dataset coverage windows and caveats live in `mcp-server/src/catalog.ts` in that repo — treat it as the source of truth for coverage prose.
