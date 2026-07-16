---
title: T&E Policy Wiki
---

{% assign topic_pages = site.pages | where_exp: "p", "p.path contains 'topics/' and p.name != 'index.md'" %}
{% assign source_pages = site.pages | where_exp: "p", "p.path contains 'sources/' and p.name != 'index.md'" %}

# T&E Policy Wiki

A topic-based reference to Transport & Environment's published research. Pages are organized
around **subjects** — fuels, vehicle segments, policy dossiers — rather than individual
publications, tracking how T&E's positions and estimates have evolved over time. Every claim
links back to the publication it's drawn from.

**{{ topic_pages.size }}** topic pages, drawn from **{{ source_pages.size }}** source publications.

- [Browse topics](topics/index.md)
- [Browse sources](sources/index.md)

Use the search box above to find pages by keyword.

**Coverage note:** this is currently a small test subset of T&E's output (a handful of
2021-2024 trucking/van reports plus most of 2025), not the full publication archive — see
[Sources](sources/index.md) for exactly what's included. Topic pages describe how positions
evolved *across the sources cited on that page*, which for most topics means within 2025 so far,
not necessarily T&E's full history on the subject.
