---
title: Mission & Vision
layout: default
---

# Mission & Vision

## The mission

**To foster knowledge creation and knowledge management.**

The human psyche and human cognition have the potential to do much more — in
particular when it comes to their interaction with the digital world — than what
currently exists. The current digital ecosystem (operating systems, apps, the
web, AI) still only scratches the surface of the potential of human cognition.

There is a big difference between *having a ton of information online* — as
Wikipedia does — and *understanding*, at a technical and individual level, a
complex topic the way a molecular biologist understands their field. Access to
information is not understanding. IndieK is built around that distinction.

IndieK aims at fostering **knowledge creation at the level of individual
psyches**. It also targets **collaborative knowledge generation, via debating**.

## The vision

Two movements, one substrate:

1. **The individual.** A person building genuine understanding of a complex
   topic needs to externalise structure, not just store documents. They need to
   connect, contradict, revise, and re-read their own thinking over years —
   without their work being trapped in a vendor's database or in a format that
   dies with the app that wrote it.

2. **The collective.** Understanding sharpens against opposition. IndieK treats
   **debate** as a first-class knowledge-generating activity rather than as
   social noise, and models it on the same substrate as individual thought.

Both rest on the same technical foundation: a durable, verifiable,
implementation-independent knowledge graph archive that a person owns.

## The bet

IndieK's current bet is to **leverage knowledge graphs with very loose
restrictions on the data format**:

- Versatile data may be attached to **both nodes and edges**. An edge is not a
  bare pointer — it carries content, and can be argued about, tagged and revised
  exactly like a node.
- **Tags may be designed freely** for both edges and nodes. IndieK ships no
  fixed ontology, no mandatory schema, and no imposed taxonomy. You invent the
  vocabulary your topic needs.

This looseness is deliberate. A rigid schema encodes someone else's
understanding of your domain; premature structure is the enemy of knowledge
creation. IndieK constrains *durability* (content-addressed data, signed
append-only history, archival-safe media types) and leaves *meaning* to you.

## What that implies technically

The bet above is what produces the design choices documented in the
[format specification](/docs/format/):

| Principle | Consequence in the format |
| --- | --- |
| Your archive must outlive our software | Plain directories, NDJSON, a self-describing `MANIFEST.json` |
| History is knowledge, not clutter | Append-only event log; nothing is ever edited or deleted, only *superseded* |
| Data belongs to nodes *and* edges | Both carry a resource (blob, URI, or local-file reference) |
| Debate requires attribution | Every event is Ed25519-signed by its author |
| Tampering must be detectable | Hash-chained events, content-addressed blobs |
| Vocabulary is yours | Free-form tags, modelled as a separate "meta-network" graph |
| Collaboration should not need a server | An archive is a directory — so git handles collaboration |

## The products

IndieK is an ecosystem, split along a clear line: **the format and the local
tools are free and open source; the hosted, networked services are
proprietary.** See [Introduction](/docs/intro/) for how the pieces fit together
and [Licenses](/docs/license/) for the legal terms.

### Free and open source

- **The IndieK archival format** — the specification on this site. Apache-2.0.
- **`ik`, the Python CLI** — the reference implementation for creating, reading,
  verifying and exporting archives. Apache-2.0. See the
  [CLI reference](/docs/cli/).
- **The IndieK Desktop App** — a packaged backend + frontend that runs **100%
  locally and fully offline**, taking local repositories as input. Because an
  archive is just a directory, a knowledge graph can be built collaboratively
  using nothing but git.
- **indiek.org** — this documentation site.

### Proprietary

- **Cloud-hosted knowledge-graph management web apps.**
- **A debating platform** powered by a knowledge-graph backend.
- **Premium tiers** for cloud functionality.

The proprietary layer is built *on top of* the open format. It does not extend
it, fork it, or gate it: an archive produced by a paid IndieK service is
readable by the FOSS CLI, and vice versa.

## Roadmap

| Date | Milestone |
| --- | --- |
| 30 September 2026 | `ik` CLI published to PyPI with complete FOSS documentation |
| 30 September 2026 | FOSS IndieK Desktop App released (packaged, fully offline-capable) |
| 1 October 2026 | The FOSS layer opens for external adoption and contribution |

Until 1 October 2026 the specification and the CLI should be treated as
**pre-1.0 and subject to change**. The archival format is at version `2.0`.

## Where to go next

- [Introduction](/docs/intro/) — what IndieK is, all products, and how it works
- [Format specification](/docs/format/) — the archival format in full
- [CLI reference](/docs/cli/) — every `ik` command
- [Contributing](/docs/contributing/) — how to get involved
- [Licenses](/docs/license/) — Apache-2.0 terms and what they cover
