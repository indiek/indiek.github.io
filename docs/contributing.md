---
title: "Contributing"
description: "How to contribute to IndieK: the projects, the development workflow and the rules every change follows."
---

# Contributing

IndieK opens to external contributions on **1 November 2026**. This page describes how the project works, so you can get familiar with the
code and the format. Issues and contributions go to the repository of the
project concerned (table below); when in doubt, use the
[`indiek` repository](https://github.com/indiek/indiek).

## The projects

| Project | What it is | Stack | License |
| --- | --- | --- | --- |
| [`indiek`](https://github.com/indiek/indiek) (Python package) | The SDK (`indiek`), the `ik` CLI, the normative specification (`src/indiek/spec/SPEC.md`) and its test vectors | Python, uv | Apache-2.0 |
| [`indiek-api`](https://github.com/indiek/indiek-api) | The [local API](/docs/api/) | Python, FastAPI, uv | Apache-2.0 |
| [`indiek-webui`](https://github.com/indiek/indiek-webui) | The [web UI](/docs/web-ui/) (graph explorer) | TypeScript, Next.js (static export), React, Tailwind CSS, Cytoscape.js, Vitest | Apache-2.0 |
| [`indiek-desktop`](https://github.com/indiek/indiek-desktop) | The [desktop app](/docs/desktop/): a Tauri shell, the frozen sidecar (PyInstaller) and the installer builds; no component code, only pinned releases of the three above | Rust, Tauri 2, Python | Apache-2.0 |
| indiek.org | This website | Jekyll | Apache-2.0 |

How they depend on each other, and how releases flow from one to the next:
[Architecture](/docs/architecture/). Each repository's `README.md` explains
its setup, code layout and tests in detail.

## The `indiek` package

Inside the package:

```text
src/indiek/
├── __init__.py      the public API (indiek.__all__)
├── sdk.py           the Archive facade
├── cli.py, read.py  the ik command-line tool
├── core/            format models, canonical bytes, signing, storage,
│                    verification, seals, Merkle tree, index, cache
├── ops/             write operations: nodes, edges, tags, seals, ingest, export, manifest
└── spec/            SPEC.md and test_vectors.json
tests/
├── sdk/             SDK tests (never import the CLI)
└── cli/             CLI tests
scripts/             test-vector generator and helpers
```

## Development workflow

The Python projects use [uv](https://docs.astral.sh/uv/) exclusively.

`indiek`:

```bash
uv sync                                       # create the environment
uv run pytest                                 # the test suite
uv run pytest -m slow                         # the 10,000-event performance test
uv run ruff check src tests scripts           # lint
uv run ruff format --check src tests scripts  # formatting
uv run ik --help                              # the CLI from your working copy
```

`indiek-api`:

```bash
uv sync
uv run ruff check . && uv run ruff format --check . && uv run pytest
uv run python -m indiek_api                   # the server from your working copy
uv run --with-editable ../indiek pytest       # against an unreleased indiek checkout
```

`indiek-webui` (Node.js and npm):

```bash
npm install
npx tsc --noEmit && npm run lint && npm test && npm run build
npm run dev                                   # hot reload; proxies /api/* to a running indiek-api
```

`indiek-desktop` (Rust, Node.js, uv):

```bash
npm install && uv sync && uv run pytest
cd src-tauri && cargo fmt --check && cargo clippy --all-targets && cargo test
```

Every repository runs these checks in GitHub Actions on each push.

## Rules for every change

- **Tests first.** Every feature and every bug fix comes with tests; the
  suite must stay green, lint and formatting clean.
- **A changelog entry** in `CHANGELOG.md`, in the section of the upcoming
  release.
- **Versioning.** Every project follows semantic versioning: a new feature
  bumps the minor version, a fix the patch version. Release tags are the
  bare version (`1.4.0`, no `v`) and must equal the version in the project's
  metadata.
- **Small, focused changes**, with modern, fully typed code (strict type
  hints in Python, strict TypeScript).
- **The API and the web UI change together.** The web UI mirrors the API's
  contract in `src/lib/types.ts` and `src/lib/api.ts`; a route change
  updates both sides and their tests.
- **The API never listens beyond `127.0.0.1`** and never logs or returns a
  secret.
- In the `indiek` package: **the README examples are executed by the
  tests** (keep them runnable), and **the SDK never imports CLI
  dependencies** (`rich`, `python-dotenv`); a test enforces it.

## Changing the format

The format is the part of IndieK that must last, so changes to it follow
stricter rules:

1. Update `SPEC.md`, the normative specification, in the same change as the
   code.
2. Regenerate the test vectors with
   `uv run python scripts/make_test_vectors.py` and explain any changed value.
3. A change that alters what is valid needs a new format version. From
   format 3.0 on, every published version stays readable (3.1, for
   example, only added content-less edges).
4. Prefer established standards (RFC 8785, RFC 8032, RFC 6962, RFC 9562) over
   new constructions.

This website's [format page](/docs/format/), [SDK](/docs/sdk/) and
[CLI](/docs/cli/) references are generated from the package's `SPEC.md` and
`README.md` (`scripts/sync_docs.py` in the website's sources); fix the
source, not the generated page.
