---
layout: default
title: "IndieK"
---

# IndieK

**IndieK is a knowledge graph archival format and the ecosystem of tools built
around it.**

Its mission is to **foster knowledge creation and knowledge management** — both
inside a single mind and between minds that disagree. There is a big difference
between having a ton of information online and *understanding* a complex topic
at a technical, individual level. IndieK is built for the second thing.
Read the [full mission and vision](/docs/mission/).

## Start here

| If you want to… | Go to |
| --- | --- |
| Understand what IndieK is and why | [Mission & Vision](/docs/mission/) |
| See all the products and how they fit | [Introduction](/docs/intro/) |
| Implement or parse an archive | [Format specification](/docs/format/) |
| Use the reference tool | [CLI reference](/docs/cli/) |
| Contribute | [Contributing](/docs/contributing/) |
| Check the legal terms | [Licenses](/docs/license/) |

## An archive in thirty seconds

An IndieK archive is a **plain directory**. No database, no server, no
proprietary container:

```
my-archive/
├── MANIFEST.json          # self-describing: layout + schemas
├── events/                # signed, hash-chained, append-only NDJSON log
│   └── 2026/08/09/events.ndjson
├── meta/events/           # the same, for tags (the "meta-network")
│   └── 2026/08/09/events.ndjson
└── blobs/sha256/          # content-addressed data for nodes and edges
    └── 26/09/2609c7c2...85e2
```

The durable things are **the signed append-only event log** and **the blob
store**. Together they *are* the archive. Everything else — indexes, graph
projections, visualisations, UIs — is a rebuildable projection.

Three properties follow, and they are the whole point:

- **Verifiable.** Every event is Ed25519-signed by its author and carries the
  hash of the event before it. The hash of the last event is the archive's
  canonical identity: two archives are identical if and only if their last event
  hashes match.
- **Durable.** UTF-8 NDJSON, SHA-256 filenames, archival-safe media types, and a
  `MANIFEST.json` that documents the whole layout so a future reader needs no
  IndieK code at all.
- **Yours.** It is a directory of files on your disk. Collaboration is
  `git push`. There is no service to lose access to.

## Loose by design

IndieK ships **no fixed ontology**. Versatile data may be attached to **nodes
*and* edges**, and tags may be **designed freely** for both. A rigid schema
would encode someone else's understanding of your domain; IndieK constrains
durability and leaves meaning to you.

## Try it

```bash
uv tool install ik          # from source until the PyPI release (30 Sep 2026)
ik manifest                 # write MANIFEST.json into the archive
ik create_node --content "Understanding is not retrieval"
ik create_node --content "Wikipedia is retrieval"
ik create_edge --source-node e2 --target-node e1 --content "illustrates"
ik read --mini              # inspect the log
ik export --output-path graph.graphml
```

Full setup — including the two environment variables `ik` needs and how to
generate an author key — is in the [CLI reference](/docs/cli/).

## Status

Pre-1.0. The archival format is at version **2.0**. The specification and the
CLI are subject to change until **1 October 2026**, when the FOSS layer opens
for external adoption and contribution.

The format specification and the `ik` CLI are licensed under
**Apache License 2.0**. See [Licenses](/docs/license/).
