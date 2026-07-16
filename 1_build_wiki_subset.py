"""
Step 6: Build wiki source pages from a keyword filter over
output/metadata_with_fulltext.parquet. Writes one markdown "source page" per matching
document under wiki/sources/ (skipping documents already materialized there). These
source pages are the citation targets that topic pages (wiki/topics/*.md, hand-authored
per wiki/AGENT_INSTRUCTIONS.md) link back to.

A source page is a short citation card, NOT a dump of the PDF's cleaned text layer: title,
date/office/type, a link to the original publication, and the publication's own summary/
abstract if one exists. The full fulltext is deliberately not rendered — PDF-extracted body
text comes out as unreadable page-fragment soup (running headers, footnote markers, table
cells) that is worse than no body at all. The fulltext stays available for search/embedding
via the parquet file; it just isn't fit for human reading on the page itself.

This script only writes source pages — it does not touch wiki/sources/index.md or
wiki/topics/index.md. After running it (and updating/authoring topic pages), always run
`python 2_refresh_wiki_index.py` to regenerate both index files from what's on disk.

Usage:
  python 1_build_wiki_subset.py                         # default keyword, all matches
  python 1_build_wiki_subset.py --keyword biofuel --limit 10   # latest 10 new matches
"""
import argparse
import glob
import os
import re
import pandas as pd

from config import PAGES_PARQUET_OUT, WIKI_SOURCES_DIR, WIKI_SUBSET_FILTER

FRONTMATTER_TMPL = """---
id: {id}
title: "{title}"
date: {date}
office: {office}
publication_type: {publication_type}
article_url: {article_url}
pdf_url: {pdf_url}
doc_ids: [{doc_ids}]
---
"""

_FRONTMATTER_FIELD_RE = re.compile(r"^article_url:\s*(.+)$", re.MULTILINE)


def _yaml_str(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "null"
    return str(val)


def _slugify(title, fallback_id):
    slug = re.sub(r"[^a-z0-9]+", "-", str(title).lower()).strip("-")
    return slug[:80] or fallback_id


def _select_representative(group: pd.DataFrame) -> pd.Series:
    """When one article has multiple docs (HTML + PDF), keep the longest fulltext
    as the body but record every contributing doc id for provenance."""
    lengths = group["fulltext"].fillna("").map(len)
    rep = group.loc[lengths.idxmax()].copy()
    rep["doc_ids"] = list(group["ID"])
    return rep


def _existing_article_urls() -> set:
    """Article URLs already materialized as source pages, so re-running with a new
    keyword doesn't duplicate a source that was already pulled in by a prior filter."""
    urls = set()
    for path in glob.glob(os.path.join(WIKI_SOURCES_DIR, "*.md")):
        if os.path.basename(path) == "index.md":
            continue
        text = open(path, encoding="utf-8").read()
        m = _FRONTMATTER_FIELD_RE.search(text)
        if m:
            urls.add(m.group(1).strip())
    return urls


def build_subset(keyword: str = WIKI_SUBSET_FILTER, limit: int = None):
    df = pd.read_parquet(PAGES_PARQUET_OUT)
    mask = df["fulltext"].str.contains(keyword, case=False, na=False)
    subset = df.loc[mask].copy()
    if subset.empty:
        print(f"No documents matched '{keyword}'.")
        return []

    group_key = subset["Article URL"].fillna(subset["ID"]).rename("_group_key")
    reps = subset.groupby(group_key, sort=False).apply(_select_representative)
    reps = reps.reset_index(drop=True)

    existing = _existing_article_urls()
    reps = reps[~reps["Article URL"].isin(existing)]
    if reps.empty:
        print(f"All documents matching '{keyword}' are already in {WIKI_SOURCES_DIR}.")
        return []

    reps["_date_sort"] = pd.to_datetime(reps["Publication Date"], errors="coerce")
    reps = reps.sort_values("_date_sort", ascending=False)
    if limit:
        reps = reps.head(limit)

    os.makedirs(WIKI_SOURCES_DIR, exist_ok=True)
    written = []

    for _, row in reps.iterrows():
        title = row["Title"] or f"Doc {row['ID']}"
        slug = _slugify(title, row["ID"])
        filename = f"{slug}.md"
        path = os.path.join(WIKI_SOURCES_DIR, filename)

        frontmatter = FRONTMATTER_TMPL.format(
            id=row["ID"],
            title=title.replace('"', "'"),
            date=_yaml_str(row["Publication Date"]),
            office=_yaml_str(row["Office"]),
            publication_type=_yaml_str(row["Publication Type"]),
            article_url=_yaml_str(row["Article URL"]),
            pdf_url=_yaml_str(row["PDF URL"]),
            doc_ids=", ".join(row["doc_ids"]),
        )
        date_str = _yaml_str(row["Publication Date"])[:10]
        office = _yaml_str(row["Office"])
        pub_type = _yaml_str(row["Publication Type"])
        meta_line = " · ".join(p for p in (pub_type, office, date_str) if p and p != "null")

        article_url = _yaml_str(row["Article URL"])
        pdf_url = _yaml_str(row["PDF URL"])
        links = []
        if article_url != "null":
            links.append(f"[Read the original publication]({article_url})")
        if pdf_url != "null" and pdf_url != article_url:
            links.append(f"[PDF]({pdf_url})")

        with open(path, "w", encoding="utf-8") as f:
            f.write(frontmatter)
            f.write("\n")
            f.write(f"# {title}\n\n")
            if meta_line:
                f.write(f"*{meta_line}*\n\n")
            if links:
                f.write(" · ".join(links) + "\n\n")
            summary = row["Summary"]
            if summary and summary.strip().lower() != "no summary":
                f.write(f"> {summary}\n")
            else:
                f.write("*(No abstract available for this publication.)*\n")

        written.append(filename)
        print(f"Wrote {path}")

    print(f"\n{len(written)} new source page(s) written. Now run "
          f"`python 2_refresh_wiki_index.py` to rebuild the index files.")
    return written


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", default=WIKI_SUBSET_FILTER)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    build_subset(keyword=args.keyword, limit=args.limit)
