---
title: Introduction
layout: default
---

# Introduction

This page explains **what IndieK is**, **what the products are**, and **how the
whole thing works**. If you want the *why* first, read
[Mission & Vision](/docs/mission/). If you want to parse an archive, jump to the
[format specification](/docs/format/).

## 1. What IndieK is

IndieK is a **knowledge graph (KG) archival format** and an ecosystem of tools
around it.

The format is the centre of gravity. Everything else — a CLI, a desktop app,
cloud services, a debating platform — is a *consumer* of the format. That
ordering is deliberate: applications are replaceable, archives are not.

An IndieK knowledge graph has three unusual properties:

1. **Edges carry content.** An edge is not a bare pointer from A to B. It has
   its own data, its own author, its own tags, and its own revision history.
   "Why are these two ideas connected?" is a first-class question with a
   first-class answer.
2. **Nothing is ever mutated.** The archive is an append-only, signed,
   hash-chained event log. Editing a node appends a `supersede_node` event; the
   previous version remains in the log forever. Your revisions *are* knowledge.
3. **Vocabulary is user-defined.** Tags are created freely by users and modelled
   as a graph of their own (the *meta-network*). There is no built-in taxonomy.

## 2. The two layers

IndieK is split along one clear line.

### The FOSS layer — the format and everything local

| Product | What it is | Status |
| --- | --- | --- |
| **IndieK archival format** | The specification documented on this site. Version `2.0`. | Published, pre-1.0 |
| **`ik` — the Python CLI** | Reference implementation: create, read, verify, ingest and export archives. See the [CLI reference](/docs/cli/). | Ships to PyPI by 30 Sep 2026 |
| **IndieK Desktop App** | A packaged backend + frontend that runs **100% locally and fully offline**. Takes local repositories as input. Handles basic write operations; the CLI remains the tool for fine-grained control. | Releases by 30 Sep 2026 |
| **indiek.org** | This documentation site. | Live |

All of it is **Apache-2.0** licensed. See [Licenses](/docs/license/).

### The proprietary layer — everything hosted

| Product | What it is |
| --- | --- |
| **Cloud KG management web apps** | Hosted graph browsing, editing and management |
| **Debating platform** | Collaborative knowledge generation through structured debate, backed by a knowledge graph |
| **Premium tiers** | Paid cloud functionality |

**The boundary is architectural, not just legal.** The proprietary layer is a
consumer of the same open format. It does not extend the format with private
fields, it does not gate any part of the specification, and it does not require
a hosted account to read your own data. An archive written by a paid IndieK
service is readable by the FOSS CLI, and an archive written by the CLI is
readable by the hosted apps.

### Collaboration without a server

Because an archive is a plain directory and the event log is append-only, **git
provides collaboration for free**. Several authors can build one knowledge graph
by pushing to a shared repository:

- Each author signs their own events with their own Ed25519 key, so authorship
  survives merging.
- Events are stored in date-sharded files (`events/YYYY/MM/DD/events.ndjson`),
  which keeps concurrent appends from colliding on the same file most of the
  time.
- Any reader can verify the whole chain locally.

This is the input model for the Desktop App: point it at local repositories that
contain collaboratively built graphs.

## 3. How it works

### 3.1 The durable core

> The durable thing is the signed append-only event history and the blob store.
> Everything else should be rebuildable projections.

Two stores, one archive:

- **The blob store** holds the actual data. Every piece of content attached to a
  node or an edge is a *blob*, and a blob's identity **is** its SHA-256 hash. A
  blob is immutable once written, and identical content is stored exactly once.
- **The event log** holds the metadata needed to reconstruct the entire graph.
  It is append-only, each event is signed, and each event references the hash of
  its predecessor.

Graph identifiers are **UUIDv7** — distinct from blob hashes. A node keeps its
UUID across every revision; the blob it points to changes.

### 3.2 The two networks

IndieK stores two logs, and they mean different things.

**The base network** (`events/`) is your knowledge graph: nodes, edges, and
their revisions.

- `create_node` — a new node
- `create_edge` — a new directed edge, with content, between two existing nodes
- `supersede_node` / `supersede_edge` — new content for an existing item, without
  allocating a new identifier. Edge endpoints can never change.

**The meta-network** (`meta/events/`) is the tagging graph. Rather than stuffing
tags into node records, IndieK models tagging as a graph in its own right:

- A **tag** is a meta-node with a name and a description (`create_node_tag` for
  tagging nodes, `create_edge_tag` for tagging edges).
- A **representation** is a shadow meta-node that stands for a base-network node
  or edge (`create_node_representation` / `create_edge_representation`).
- A **meta-edge** from a tag to a representation means *"this tag applies to
  that item"* (`set_node_tag` / `set_edge_tag`).

This costs one indirection and buys a lot: tags are addressable objects with
authors and descriptions, tagging is itself a signed historical event, and the
tag vocabulary can later grow its own structure (tags relating to tags) without
any format change.

### 3.3 Resources: three ways to attach data

Not everything should be copied into an archive. A node or edge declares a
`resource_type`:

| `resource_type` | Meaning | Durability |
| --- | --- | --- |
| `managed` | Content is copied into the archive's blob store and content-addressed | Fully self-contained |
| `uri` | The archive records an external URL and does not fetch it | Depends on the external host |
| `local_file` | The archive records a path plus size, SHA-256 fingerprint and verification timestamp — without importing the file | The file stays where it is; drift is detectable |

`managed` is the default and the only fully archival option. `local_file` is the
pragmatic middle ground for large media you do not want duplicated: IndieK
remembers enough to *prove* whether the file has changed.

To stay archival, managed content is restricted to a short list of media types:
`text/plain`, `text/markdown`, `image/png`, `image/jpeg`, `image/tiff`, and
PDF/A.

### 3.4 Integrity

Three independent checks, all runnable offline:

1. **Chain integrity** — each event's `prev_hash` must equal the SHA-256 of the
   entire preceding event, canonically serialised. A broken link means insertion,
   deletion or reordering.
2. **Signatures** — each event's signature must verify against its author's
   Ed25519 public key over the canonical hash of the event body. This proves both
   authorship and that the body has not been altered.
3. **Blob integrity** — every referenced blob must exist on disk and hash to the
   value recorded in the event.

The reference CLI runs all three on **every invocation**, before doing anything
else. There is no "unverified" mode.

The hash of the final event is the archive's canonical identity at that point in
time. Two archives are identical if and only if their last event hashes match —
which makes archive comparison a 64-character string comparison.

### 3.5 Rebuildable projections

Because the log is the truth, everything convenient is derived:

- The **current graph state** — walk the log, apply creations, let supersedes
  overwrite the active projection.
- **Human-friendly IDs** — `e1`, `e2`, … for base-network items and `m1`, `m2`, …
  for meta-network items, assigned in log order so you can type `e4` instead of a
  UUID.
- **Tag assignments** — resolved by following meta-edges through representations
  back to base items.
- **Exports** — GraphML for external visualisation tools.

Delete every projection and you have lost nothing. Delete the log and you have
lost everything.

## 4. A worked example

Two authors, one small debate. `GENESIS` and `ANON` each have their own key and
their own `.env` file:

```bash
# GENESIS states two claims
ik --dot-env .env.genesis create_node --content "Dieu existe"                  # e1
ik --dot-env .env.genesis create_node --content "Donc je suis divin"           # e2

# ANON objects, and links the objection to the first claim
ik --dot-env .env.anonymous1 create_node --content "Je ne vois aucune preuve"  # e3
ik --dot-env .env.anonymous1 create_edge --source-node e3 --target-node e1 \
    --content "Pas d'accord"                                                   # e4

# ANON invents a vocabulary for edges and applies it to their own objection
ik --dot-env .env.anonymous1 create_edge_tag --name "reaction" \
    --description "reaction to others' words"                                  # m1
ik --dot-env .env.anonymous1 set_tag --tag m1 --id e4

# GENESIS invents a vocabulary for nodes and groups the two positions
ik --dot-env .env.genesis create_node_tag --name "discussion" \
    --description "discussion about God"                                       # m4
ik --dot-env .env.genesis set_tag --tag m4 --id e1
ik --dot-env .env.genesis set_tag --tag m4 --id e3
```

The result is a signed, attributable, tamper-evident debate in a directory you
can commit to git. Note that `set_tag` requires you to be the tag's own author —
you may apply *your* vocabulary to *anyone's* items, but you cannot apply
someone else's vocabulary on their behalf.

## 5. Where to go next

- [Format specification](/docs/format/) — the normative reference for
  implementers
- [CLI reference](/docs/cli/) — installation, configuration, every command
- [Contributing](/docs/contributing/) — how to help
- [Licenses](/docs/license/) — Apache-2.0
