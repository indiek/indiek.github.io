---
title: "Contributing"
description: "How to contribute to IndieK: the projects, the development workflow and the rules every change follows."
---

# Contributing

IndieK opens to external contributions on **1 November 2026**. Until then,
this page describes how the project works, so you can get familiar with the
code and the format; the channels for issues and contributions will be
announced here on that date.

## The projects

| Project | What it is | License |
| --- | --- | --- |
| `indiek` (Python package) | The SDK (`indiek`), the `ik` CLI, the normative specification (`src/indiek/spec/SPEC.md`) and its test vectors | Apache-2.0 |
| indiek.org | This website | Apache-2.0 |

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

The project uses [uv](https://docs.astral.sh/uv/) for everything Python.

```bash
uv sync                                       # create the environment
uv run pytest                                 # the test suite
uv run pytest -m slow                         # the 10,000-event performance test
uv run ruff check src tests scripts           # lint
uv run ruff format --check src tests scripts  # formatting
uv run ik --help                              # the CLI from your working copy
```

## Rules for every change

- **Tests first.** Every feature and every bug fix comes with tests; the
  suite must stay green, lint and formatting clean.
- **A changelog entry** in `CHANGELOG.md`, in the section of the upcoming
  release.
- **Versioning.** The package follows semantic versioning: a new feature
  bumps the minor version, a fix the patch version.
- **Small, focused changes**, with modern, fully typed Python.
- **The README examples are executed by the tests**: keep them runnable.
- **The SDK never imports CLI dependencies** (`rich`, `python-dotenv`); a
  test enforces it.

## Changing the format

The format is the part of IndieK that must last, so changes to it follow
stricter rules:

1. Update `SPEC.md`, the normative specification, in the same change as the
   code.
2. Regenerate the test vectors with
   `uv run python scripts/make_test_vectors.py` and explain any changed value.
3. A change that alters what is valid needs a new format version. From
   format 3.0 on, every published version stays readable.
4. Prefer established standards (RFC 8785, RFC 8032, RFC 6962, RFC 9562) over
   new constructions.

This website's [format page](/docs/format/), [SDK](/docs/sdk/) and
[CLI](/docs/cli/) references are generated from the package's `SPEC.md` and
`README.md` (`scripts/sync_docs.py` in the website's sources); fix the
source, not the generated page.
