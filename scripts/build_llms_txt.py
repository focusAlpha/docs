#!/usr/bin/env python3
"""Build llms.txt from docs.json navigation and page frontmatter.

Run from the repo root after adding, renaming or retitling a page:
    python3 scripts/build_llms_txt.py
The MCP tools listed per page come from each page's `keywords` frontmatter
(entries that look like tool names).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://docs.focusalpha.ai"
TOOL = re.compile(r"^(get|list|search|screen|manage)_[a-z0-9_]+$|^retrieve$")

HEADER = """# FocusAlpha

> FocusAlpha serves company data for global equities from filings, earnings calls, market feeds and curated registries: financial statements as filed, management guidance with the quote it came from, analyst consensus, outside research, a live company event and news feed, ownership, ETFs, investment advisers, macro data and exchange disclosures across the US, Japan, Korea, Taiwan, Hong Kong and mainland China. Use it through the REST API (`https://api.focusalpha.ai`, `Authorization: Bearer <key>`) or the MCP server (`https://mcp.focusalpha.ai/mcp`), where every dataset is a tool.

## For AI agents: start here

- [Guide for AI agents]({base}/concepts/agent-guide.md): Which tool to call first, how to resolve a company, and the rules that keep an answer from reporting a wrong number.
- [MCP tool reference]({base}/mcp-tools.md): Every MCP tool with what it answers, its key arguments, its REST endpoint and its docs page, plus a table for picking between tools that sound alike.
- [Connect via MCP]({base}/mcp-setup.md): Add the MCP server to Claude, ChatGPT, Cursor, VS Code or any MCP client.
- [Data quality and sources]({base}/concepts/data-quality.md): Figures as filed, continuous cleaning, and which rows link back to their filing.

Routing in one breath: numbers come from structured tools (statements, `get_guidance`, `get_consensus`, `get_8k_earnings_results`, segments, ownership); what management said comes from `retrieve`; what analysts wrote comes from `get_research`; what just happened comes from `get_company_events`; when unsure, call `list_datasets` (free). A null means not reported and an empty result means not covered — never zero.

Every page below is also available as Markdown at the linked `.md` URL; `{base}/llms-full.txt` has the whole site in one file.
"""


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        v = v.strip()
        if k.strip() == "keywords":
            out["keywords"] = json.loads(v) if v.startswith("[") else []
        elif v:
            out[k.strip()] = v.strip('"')
    return out


def walk(node, groups, current=None):
    if isinstance(node, str):
        groups.setdefault(current, []).append(node)
        return
    if isinstance(node, dict):
        name = node.get("group") or current
        for key in ("tabs", "groups", "pages", "anchors", "dropdowns"):
            for child in node.get(key, []):
                walk(child, groups, name if key == "pages" else current)


def top_level_groups(nav):
    """Map each page to its top-level sidebar group, preserving order."""
    order, pages = [], {}

    def rec(node, top):
        if isinstance(node, str):
            pages.setdefault(top, [])
            if node not in pages[top]:
                pages[top].append(node)
            return
        for key in ("tabs", "groups", "pages", "anchors", "dropdowns"):
            for child in node.get(key, []):
                t = top
                if isinstance(child, dict) and child.get("group") and top is None:
                    t = child["group"]
                    if t not in order:
                        order.append(t)
                rec(child, t)

    rec(nav, None)
    return order, pages


def main():
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    order, pages = top_level_groups(docs["navigation"])
    seen = set()
    lines = [HEADER.format(base=BASE)]
    for group in order:
        entries = []
        for page in pages.get(group, []):
            if page in seen:
                continue
            seen.add(page)
            fm = frontmatter(ROOT / f"{page}.mdx")
            title = fm.get("title", page)
            desc = fm.get("description", "")
            tools = [k for k in fm.get("keywords", []) if TOOL.match(k)]
            line = f"- [{title}]({BASE}/{page}.md)"
            if desc:
                line += f": {desc}"
            if tools:
                line += " MCP: " + ", ".join(f"`{t}`" for t in tools) + "."
            entries.append(line)
        if entries:
            lines.append(f"## {group}\n\n" + "\n".join(entries) + "\n")
    (ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"llms.txt: {len(seen)} pages")


if __name__ == "__main__":
    main()
