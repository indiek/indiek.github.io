---
title: Format specification
layout: default
---

## Overview

A FAF archive is a directory containing:

1. `manifest.json` — JSON metadata describing the archive contents and provenance.
2. `source/` — the source tree (preferably at a tagged revision).
3. `patches/` — optional patches applied to the source for archival reasons.
4. `licenses/` — SPDX-compatible license documents.

### Manifest schema (example)

```json
{
  "format": "faf-1",
  "name": "example-project",
  "version": "1.0.0",
  "created_at": "2026-01-01T00:00:00Z",
  "sources": [
    {"type":"git","url":"https://github.com/example/repo.git","ref":"v1.0.0"}
  ]
}
```

See the examples section for complete sample archives.
