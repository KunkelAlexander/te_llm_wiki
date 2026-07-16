"""
Step 1: Build wiki source pages from a keyword filter over
output/metadata_with_fulltext.parquet. Writes one markdown "source page" per matching
document under wiki/sources/ (skipping documents already decided in wiki/sources/PROCESSED.csv,
the log of every article this script has ever considered — see below). These source pages are
the citation targets that topic pages (wiki/topics/*.md, hand-authored per
wiki/AGENT_INSTRUCTIONS.md) link back to.

A source page is a short citation card, NOT a dump of the PDF's cleaned text layer: title,
date/office/type, a link to the original publication, and the publication's own summary/
abstract if one exists. The full fulltext is deliberately not rendered — PDF-extracted body
text comes out as unreadable page-fragment soup (running headers, footnote markers, table
cells) that is worse than no body at all. The fulltext stays available for search/embedding
via the parquet file; it just isn't fit for human reading on the page itself.

Near-duplicate handling: T&E often publishes the same underlying work twice — a press
release/news post announcing it, and the report/briefing itself. When a new candidate's title
closely matches an announcement/substantive pair within a short date window (see
PUB_TYPE_SUBSTANTIVENESS / WIKI_DUP_* in config.py), only the more substantial one gets a source
page. The announcement is not materialized — it's logged in PROCESSED.csv as a dropped
duplicate, pointing at the source page that supersedes it, so nothing is silently lost.

Processed-article log (wiki/sources/PROCESSED.csv): every article this script has ever decided
on — included or dropped as a duplicate — is logged here, one row per Article URL. This is what
makes re-running the script over a growing corpus (thousands of articles, many keyword passes)
cheap and idempotent: candidates already in the log are skipped up front rather than re-read and
re-decided every run, and a dropped duplicate stays dropped instead of reappearing as "new" the
next time a keyword filter happens to match it again.

This script only writes source pages and PROCESSED.csv — it does not touch wiki/sources/index.md
or wiki/topics/index.md. After running it (and updating/authoring topic pages), always run
`python 2_refresh_wiki_index.py` to regenerate both index files from what's on disk.

Usage:
  python 1_build_wiki_subset.py                         # default keyword, all matches
  python 1_build_wiki_subset.py --keyword biofuel --limit 10   # latest 10 new matches
"""
import argparse
import csv
import os
import re
import sys

import pandas as pd

try:
    # Some titles contain characters (e.g. the CO₂ subscript) outside a narrow Windows console
    # codepage (cp1252); without this, printing them mid-run crashes the whole batch instead of
    # just garbling that one line.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from config import (
    DEFAULT_PUB_TYPE_SUBSTANTIVENESS,
    PAGES_PARQUET_OUT,
    PUB_TYPE_SUBSTANTIVENESS,
    WIKI_ANNOUNCEMENT_TIER_MAX_RANK,
    WIKI_DUP_DATE_WINDOW_DAYS,
    WIKI_DUP_TITLE_SIMILARITY,
    WIKI_PROCESSED_LOG,
    WIKI_SOURCES_DIR,
    WIKI_SUBSET_FILTER,
)

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

PROCESSED_LOG_FIELDS = [
    "article_url", "title", "date", "publication_type", "status",
    "source_file", "duplicate_of",
]


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


def _load_processed_log() -> dict:
    """article_url -> row dict, for every article this script has ever decided on. Bootstraps
    itself from existing wiki/sources/*.md the first time it's run, so pages materialized before
    this log existed count as already-processed rather than needing to be re-decided."""
    if os.path.exists(WIKI_PROCESSED_LOG):
        with open(WIKI_PROCESSED_LOG, newline="", encoding="utf-8") as f:
            return {row["article_url"]: row for row in csv.DictReader(f)}

    import glob
    field_re = {
        "title": re.compile(r'^title:\s*"?(.+?)"?$', re.MULTILINE),
        "date": re.compile(r"^date:\s*(.+)$", re.MULTILINE),
        "publication_type": re.compile(r"^publication_type:\s*(.+)$", re.MULTILINE),
    }
    bootstrapped = {}
    for path in glob.glob(os.path.join(WIKI_SOURCES_DIR, "*.md")):
        filename = os.path.basename(path)
        if filename == "index.md":
            continue
        text = open(path, encoding="utf-8").read()
        m = _FRONTMATTER_FIELD_RE.search(text)
        if not m:
            continue
        url = m.group(1).strip()
        fields = {k: (r.search(text).group(1).strip() if r.search(text) else "")
                  for k, r in field_re.items()}
        bootstrapped[url] = {
            "article_url": url, "title": fields["title"], "date": fields["date"],
            "publication_type": fields["publication_type"],
            "status": "included", "source_file": filename, "duplicate_of": "",
        }
    if bootstrapped:
        _append_processed_log({}, list(bootstrapped.values()))
        print(f"Bootstrapped {WIKI_PROCESSED_LOG} from {len(bootstrapped)} existing source page(s).")
    return bootstrapped


def _append_processed_log(existing: dict, new_rows: list):
    combined = {**existing, **{r["article_url"]: r for r in new_rows}}
    os.makedirs(os.path.dirname(WIKI_PROCESSED_LOG), exist_ok=True)
    with open(WIKI_PROCESSED_LOG, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PROCESSED_LOG_FIELDS)
        writer.writeheader()
        for row in sorted(combined.values(), key=lambda r: r.get("date") or ""):
            writer.writerow({k: row.get(k, "") for k in PROCESSED_LOG_FIELDS})


def _pub_type_rank(pub_type) -> int:
    return PUB_TYPE_SUBSTANTIVENESS.get(str(pub_type), DEFAULT_PUB_TYPE_SUBSTANTIVENESS)


# Generic words that recur across unrelated T&E titles ("X on track to meet Y target") and
# would otherwise inflate similarity between titles about genuinely different subjects.
_TITLE_STOPWORDS = frozenset("""
    the a an eu on to for and of in is are meet track tracks target targets co2 its her still
    new report briefing letter news press release oped op-ed analysis study opinion finds warns
    warned says say said with by from that this will would could should must not no yes at as
    it be than more most all their they he she we you your our
""".split())
_TITLE_WORD_RE = re.compile(r"[a-zA-Z']+")
_TITLE_STEM_LEN = 6  # crude stemmer: truncate so "carmaker"/"carmakers" collide, cheap and dep-free


def _title_tokens(title) -> set:
    words = _TITLE_WORD_RE.findall(str(title).lower())
    return {w[:_TITLE_STEM_LEN] for w in words if len(w) >= 3 and w not in _TITLE_STOPWORDS}


def _title_similarity(a, b) -> float:
    """Jaccard similarity over stemmed, stopword-filtered title tokens. Word-level overlap of
    the distinctive nouns (which entity, which vehicle segment, which policy) discriminates far
    better here than character-level ratio (difflib.SequenceMatcher): validated against the real
    corpus, two titles sharing a generic template ("X on track to meet CO2 target") scored a
    *higher* character-level ratio against each other than the true announcement/report pair did,
    because the template overlap outweighed the one distinctive word ("carmakers" vs "truck
    makers") that actually tells them apart. Token overlap doesn't have that problem: it either
    shares the distinctive word or it doesn't."""
    ta, tb = _title_tokens(a), _title_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _cluster_duplicates(reps: pd.DataFrame):
    """Match each low-substantiveness candidate (press release/news/post) against its single
    best-matching substantive candidate (report/briefing/etc.) published nearby, and drop the
    announcement in favor of that one companion. Returns (kept_df, dropped_records) where
    dropped_records each carry which winner superseded them.

    Each announcement is matched independently — this deliberately does NOT chain matches
    transitively (e.g. via a union-find over all pairs). Validated against the real corpus: two
    *different* substantive articles (a truck-CO2 op-ed and a car-CO2 report, published 4 days
    apart) each separately resembled the same press release closely enough to match it, which a
    transitive-closure approach would merge into one cluster and wrongly drop the op-ed — even
    though the op-ed and the report never resembled each other and cover different vehicle
    segments entirely. Matching each announcement to its own best companion, independently of
    every other announcement, avoids that.

    Candidates are sorted by date and compared through a sliding window bounded by
    WIKI_DUP_DATE_WINDOW_DAYS, rather than every pair against every other pair — an O(n^2) title
    scan over a few thousand articles takes minutes; date-bucketing first (true duplicates are
    always close in time) cuts that to roughly O(n * window size), since it only pays the
    title-token-overlap cost within a candidate's own date neighborhood."""
    rows = reps.copy()
    rows["_date"] = pd.to_datetime(rows["Publication Date"], errors="coerce")
    rows["_rank"] = rows["Publication Type"].map(_pub_type_rank).fillna(DEFAULT_PUB_TYPE_SUBSTANTIVENESS)
    rows = rows.sort_values("_date", kind="stable").reset_index(drop=True)
    records = rows.to_dict("records")
    n = len(records)

    def is_announcement(k):
        return records[k]["_rank"] <= WIKI_ANNOUNCEMENT_TIER_MAX_RANK

    window = pd.Timedelta(days=WIKI_DUP_DATE_WINDOW_DAYS)
    best_match = {}  # announcement index -> (similarity, substantive index)
    for i in range(n):
        if pd.isna(records[i]["_date"]):
            continue
        for j in range(i + 1, n):
            if pd.isna(records[j]["_date"]):
                continue
            if records[j]["_date"] - records[i]["_date"] > window:
                break  # sorted by date: nothing further out will be in-window either
            if is_announcement(i) == is_announcement(j):
                continue  # only cross-tier pairs count as an announcement/substantive match
            ann, sub = (i, j) if is_announcement(i) else (j, i)
            sim = _title_similarity(records[ann]["Title"], records[sub]["Title"])
            if sim < WIKI_DUP_TITLE_SIMILARITY:
                continue
            if ann not in best_match or sim > best_match[ann][0]:
                best_match[ann] = (sim, sub)

    dropped_idx = set(best_match.keys())
    kept_idx = [i for i in range(n) if i not in dropped_idx]
    dropped = [(rows.iloc[ann], rows.iloc[sub]) for ann, (_, sub) in best_match.items()]

    return rows.iloc[kept_idx], dropped


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

    processed = _load_processed_log()
    reps = reps[~reps["Article URL"].isin(processed.keys())]
    if reps.empty:
        print(f"All documents matching '{keyword}' are already decided (see {WIKI_PROCESSED_LOG}).")
        return []

    reps["_date_sort"] = pd.to_datetime(reps["Publication Date"], errors="coerce")
    reps = reps.sort_values("_date_sort", ascending=False)
    if limit:
        reps = reps.head(limit)

    kept, dropped_dups = _cluster_duplicates(reps)

    os.makedirs(WIKI_SOURCES_DIR, exist_ok=True)
    written = []
    log_rows = []

    for _, row in kept.iterrows():
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
        log_rows.append({
            "article_url": article_url, "title": title,
            "date": _yaml_str(row["Publication Date"]),
            "publication_type": pub_type, "status": "included",
            "source_file": filename, "duplicate_of": "",
        })

    for loser, winner in dropped_dups:
        winner_title = winner["Title"] or f"Doc {winner['ID']}"
        winner_slug = _slugify(winner_title, winner["ID"])
        print(
            f"Dropped duplicate: '{loser['Title']}' ({loser['Publication Type']}) "
            f"superseded by '{winner_title}' ({winner['Publication Type']})"
        )
        log_rows.append({
            "article_url": _yaml_str(loser["Article URL"]), "title": loser["Title"] or "",
            "date": _yaml_str(loser["Publication Date"]),
            "publication_type": _yaml_str(loser["Publication Type"]), "status": "dropped_duplicate",
            "source_file": "", "duplicate_of": f"{winner_slug}.md",
        })

    _append_processed_log(processed, log_rows)

    print(f"\n{len(written)} new source page(s) written, {len(dropped_dups)} duplicate(s) dropped. "
          f"Now run `python 2_refresh_wiki_index.py` to rebuild the index files.")
    return written


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", default=WIKI_SUBSET_FILTER)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    build_subset(keyword=args.keyword, limit=args.limit)
