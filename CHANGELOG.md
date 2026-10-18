# Changelog

All notable changes to the indiek.org website are documented here.

## 2026-10-18 — website licensed under Apache-2.0

### Changed
- The website is now licensed under the Apache License 2.0 (owner decision 2026-10-18), like the format specification and the `indiek` package: `LICENSE` replaced (was the GNU AGPL v3) by the same Apache-2.0 text as the package's; `docs/license.md`, the `docs/contributing.md` project table and the footer updated.

## 2026-10-18 — documentation for indiek 1.0.0 and format 3.0

### Added
- New design: sticky top bar, documentation sidebar, "On this page" table of contents, copy buttons on code blocks, Pygments-style syntax colours, responsive layout (`_layouts/default.html`, `_data/nav.yml`, `assets/css/style.css`, `assets/js/site.js`).
- New home page (hero, why IndieK, archive layout, shell and Python examples, status).
- `docs/sdk.md` and `docs/cli.md`: complete SDK and CLI references, and `docs/format.md`: the normative format 3.0 specification with a `MANIFEST.json` appendix — all three generated from the `indiek` package by `scripts/sync_docs.py`.
- `docs/examples.md`: six worked examples (research notebook, two-author debate, publishing and checking a seal, reading an archive without IndieK, long-term custody, bulk import).
- `docs/license.md`.
- `scripts/check_site.py`: internal links and anchors, stray HTML, kramdown list/table pitfalls, and execution of the Python examples.
- `CHANGELOG.md`.

### Changed
- `docs/mission.md` is now the Vision page: updated roadmap (indiek 1.0 by 31 October 2026, contributions open 1 November 2026), format 3.0, the long-term design principles.
- `docs/intro.md` is now Get started: install, first archive from the shell and from Python, concepts.
- `docs/contributing.md` expanded: projects, workflow, rules, format changes, opening date.
- `_config.yml`: title "IndieK", GFM kramdown and Rouge set explicitly, the unused `docs` collection removed, sources and scripts excluded from the build.
- Navigation links use the `/docs/<page>/` form (the old `/docs/<page>.html` links returned 404 under `permalink: pretty`).
