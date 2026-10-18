# indiek.org — website sources

Sources of [indiek.org](https://indiek.org), the documentation website of the
IndieK archive format and of the `indiek` Python package (SDK and `ik` CLI).
The site is built with Jekyll (GitHub Pages, kramdown in GFM mode, Rouge
highlighting).

## Layout

| Path | Content |
| --- | --- |
| `index.md` | Home page (`home: true`: hero layout, no sidebars). |
| `docs/mission.md` | Vision. |
| `docs/intro.md` | Get started: install, first archive, concepts. |
| `docs/examples.md` | Worked examples (executed by `scripts/check_site.py`). |
| `docs/sdk.md`, `docs/cli.md`, `docs/format.md` | **Generated** by `scripts/sync_docs.py` — do not edit. |
| `docs/contributing.md`, `docs/license.md` | Project pages. |
| `_layouts/default.html` | The only layout: top bar, docs sidebar, "On this page" TOC. |
| `_data/nav.yml` | Top-bar and sidebar navigation. |
| `assets/css/style.css`, `assets/js/site.js` | Styles (incl. Pygments-style highlighting), TOC and copy buttons. |
| `scripts/` | Generation and checks (excluded from the site). |

## Updating the generated reference pages

The format page is the package's normative `SPEC.md`; the SDK and CLI pages
are sections of the package `README.md` (whose examples the package tests
execute). After changing either, regenerate from the site root, with the
package folder next to the site as `../public_archive`:

```bash
uv run --project ../public_archive python scripts/sync_docs.py
```

## Checking the site

```bash
uv run --project ../public_archive python scripts/check_site.py
```

checks that every internal link and anchor resolves, that no stray `<…>` text
would be swallowed as HTML, that no list or table is glued to a paragraph
(kramdown would not render it), and runs the Python examples of the Get
started and Examples pages in a temporary folder.

To preview locally: `bundle install && bundle exec jekyll serve` (needs a
recent Ruby).
