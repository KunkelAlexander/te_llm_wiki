"""
Step 7: Refresh the wiki's cross-reference indexes.

Regenerates wiki/topics/index.md and wiki/sources/index.md from the frontmatter and citation
links already present in wiki/topics/*.md and wiki/sources/*.md. This is the file an agent should
check before adding or updating anything: topics/index.md lists every topic with a one-line
summary and which sources it already cites, and sources/index.md lists every source with which
topics already cite it, so an agent processing a new/unprocessed source can see at a glance which
existing topic pages are relevant instead of opening every topic file.

Run this after authoring or updating any topic page (see wiki/AGENT_INSTRUCTIONS.md, update
workflow step 5-6). It does not call an LLM or touch topic/source content — it only reflects
links and frontmatter that are already there.
"""
import glob
import os
import re
from collections import defaultdict

# Mirrors config.WIKI_SOURCES_DIR / config.WIKI_TOPICS_DIR. Not imported from config.py directly
# to avoid pulling in that module's langchain_community dependency for a two-constant read.
WIKI_SOURCES_DIR = os.path.join("wiki", "sources")
WIKI_TOPICS_DIR = os.path.join("wiki", "topics")

CITATION_RE = re.compile(r"\]\(\.\./sources/([^)]+\.md)\)")


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-frontmatter reader: handles `key: value` and folded (`>`) block scalars,
    which is all this wiki's frontmatter uses. Avoids a PyYAML dependency for a two-field read."""
    if not text.startswith("---"):
        return {}
    end = text.index("\n---", 3)
    lines = text[3:end].split("\n")
    data = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or ":" not in line:
            i += 1
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val == ">":
            i += 1
            parts = []
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                if lines[i].strip():
                    parts.append(lines[i].strip())
                i += 1
            data[key] = " ".join(parts)
            continue
        data[key] = val.strip('"')
        i += 1
    return data


def _load(dir_path):
    entries = {}
    for path in sorted(glob.glob(os.path.join(dir_path, "*.md"))):
        filename = os.path.basename(path)
        if filename == "index.md":
            continue
        text = open(path, encoding="utf-8").read()
        entries[filename] = {"frontmatter": parse_frontmatter(text), "body": text}
    return entries


def refresh():
    topics = _load(WIKI_TOPICS_DIR)
    sources = _load(WIKI_SOURCES_DIR)

    cited_by = defaultdict(list)  # source filename -> [topic filenames]
    for t_filename, t in topics.items():
        cites = list(dict.fromkeys(CITATION_RE.findall(t["body"])))  # dedup, keep order
        t["cites"] = cites
        for s_filename in cites:
            cited_by[s_filename].append(t_filename)

    # — topics/index.md —
    topics_path = os.path.join(WIKI_TOPICS_DIR, "index.md")
    ordered_topics = sorted(
        topics.items(), key=lambda kv: kv[1]["frontmatter"].get("first_seen", "")
    )
    with open(topics_path, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Topics\n---\n\n# Topics\n\n")
        f.write("Check this table before adding a new source: it shows what each topic already "
                "covers and which sources it cites, so you know which pages might need updating "
                "rather than duplicating.\n\n")
        f.write("| Topic | Type | Summary | Sources cited | First seen | Last updated |\n")
        f.write("|---|---|---|---|---|---|\n")
        for filename, t in ordered_topics:
            fm = t["frontmatter"]
            title = fm.get("title", filename)
            summary = fm.get("summary", "")
            cite_links = ", ".join(
                f"[{sources.get(c, {}).get('frontmatter', {}).get('title', c)}](../sources/{c})"
                for c in t["cites"]
            )
            f.write(
                f"| [{title}]({filename}) | {fm.get('type', '')} | {summary} | {cite_links} "
                f"| {fm.get('first_seen', '')} | {fm.get('last_updated', '')} |\n"
            )
    print(f"Wrote {topics_path}  ({len(topics)} topics)")

    # — sources/index.md —
    sources_path = os.path.join(WIKI_SOURCES_DIR, "index.md")
    ordered_sources = sorted(
        sources.items(), key=lambda kv: kv[1]["frontmatter"].get("date", "") or ""
    )
    with open(sources_path, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Sources\n---\n\n")
        f.write(f"# Sources ({len(sources)})\n\n")
        f.write("See `AGENT_INSTRUCTIONS.md` for how this list is built and maintained.\n\n")
        f.write("| Source | Date | Office | Cited by topics |\n")
        f.write("|---|---|---|---|\n")
        for filename, s in ordered_sources:
            fm = s["frontmatter"]
            title = fm.get("title", filename)
            date = (fm.get("date", "") or "")[:10]
            citing_topics = ", ".join(
                f"[{topics[t]['frontmatter'].get('title', t)}](../topics/{t})"
                for t in cited_by.get(filename, [])
            ) or "*(none yet)*"
            f.write(f"| [{title}]({filename}) | {date} | {fm.get('office', '')} | {citing_topics} |\n")
    print(f"Wrote {sources_path}  ({len(sources)} sources)")


if __name__ == "__main__":
    refresh()
