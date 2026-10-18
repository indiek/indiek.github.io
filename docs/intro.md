---
title: "Get started"
description: "Install the indiek package, create and verify your first IndieK archive, and learn the core concepts."
---

# Get started

This page takes you from nothing to a signed, sealed knowledge graph, then
explains the handful of concepts behind it. For the *why*, read the
[vision](/docs/mission/); for every detail, the [SDK](/docs/sdk/) and
[CLI](/docs/cli/) references.

## Install

IndieK needs Python 3.14 or newer. The `indiek` package contains both the
Python SDK and the `ik` command-line tool. It is [hosted on GitHub](https://github.com/indiek/indiek) and [distributed through PyPI](https://pypi.org/project/indiek/).

```bash
uv tool install 'indiek[cli]'   # the ik command
uv add indiek                   # the SDK, as a dependency of your project
pip install 'indiek[cli]'       # or with pip
```

The SDK depends only on `pydantic` and `pynacl`; the `cli` extra adds `rich`
(tables) and `python-dotenv` (configuration files).

## Your first archive, from the shell

`ik` reads two settings, from the environment or from a `.env` file in the
current folder: where the archive is, and the key you sign with.

```bash
ik keygen --write                                   # creates your key, stored in .env
ik config --set-archive-path ~/archives/first       # stored in .env too
```

Your key is your signing identity: back up `.env` privately and never share
it. Now add two ideas and the link between them:

```bash
ik create_node --content "Understanding is not retrieval" --title "Thesis"   # e1
ik create_node --content "An encyclopedia answers questions; it does not understand them"  # e2
ik create_edge --source-node e2 --target-node e1 --content "illustrates"     # e3
ik create_node_tag --name claim --description "A statement to defend"         # m1
ik set_tag --tag m1 --id e1
ik read --mini
```

`e1`, `e2`, `e3` are *aliases*: short names the tool assigns to nodes and
edges in creation order (`m1`, `m2`, … for tags). Revise a node without
losing its history, then seal and verify:

```bash
ik supersede_node --node-id e1 --content "Understanding is **not** retrieval"
ik seal       # Seal 1 created: sha256:…  — the hash to publish
ik verify     # Archive verified: 4 base events, 3 meta events, 1 seals
```

## The same, from Python

```python
from indiek import Archive, Author

author = Author.generate()  # author.seed_hex is the secret to keep
ik = Archive.open("first", author=author)

thesis = ik.create_node("Understanding is not retrieval", title="Thesis")
example = ik.create_node(
    "An encyclopedia answers questions; it does not understand them"
)
ik.create_edge(example, thesis, "illustrates")

claim = ik.create_tag("claim", "A statement to defend", kind="node")
ik.set_tag(claim, thesis)
ik.supersede_node(thesis, "Understanding is **not** retrieval")

seal = ik.seal()
print(ik.index.alias_of(thesis), seal.hash)

reader = Archive.open("first")  # anyone can open it read-only
item = reader.index.get("e1")
print(item.body["title"], reader.index.store.blobs.get_text(item.body["blob_hash"]))
```

## Concepts

### Archives are folders

An archive is a folder of plain files. The **base log** (`events/`) holds the
knowledge graph; the **meta log** (`meta/events/`) holds tags; the **blob
store** (`blobs/`) holds content, each file named after the SHA-256 of its
bytes; the **seal log** (`seals/`) holds signed checkpoints. `ik manifest`
adds a copy of the specification, a `MANIFEST.json` and test vectors, so the
archive documents itself.

Each log is a sequence of **events**, one JSON object per line. Nothing is
ever edited in place: every change appends an event. The logs and the blobs
are the archive; everything else (aliases, indexes, views) is rebuilt from
them.

### Authors and signatures

An author is an Ed25519 key pair. Every event records its author's public key
and is signed by the matching private key, and every event carries the hash
of the one before it. Change a single byte anywhere in the history and
verification names the problem: `Chain broken!`, `Data tampered or bad
author!`, `File corrupted or missing!`, ….

Several authors may write to one archive, each with their own key. Anyone may
add nodes, edges and tags; only an item's creator may revise it, and only a
tag's creator may assign it.

### Nodes and edges

A **node** holds content of one of three kinds:

| Resource type | The content… | Durability |
| --- | --- | --- |
| `managed` (default) | is copied into the blob store | fully self-contained |
| `uri` | is an external link, recorded but never fetched | depends on the external host |
| `local_file` | stays on your disk; its path, size and SHA-256 are recorded | changes are detectable |

Managed content uses archival-safe media types: plain text, Markdown, PNG,
JPEG, TIFF and PDF/A. An **edge** goes from one node to another and carries
its own text — "proves", "contradicts", "is an example of". Its endpoints
never change.

### Revisions

`supersede_node` and `supersede_edge` append new content for an existing
item, which keeps its identifier and alias. Every earlier version stays in
the log, so the history of your thinking is part of the archive.

### Identifiers and aliases

Every item has a UUID. Aliases are shorthands computed by replaying the logs:
`e1`, `e2`, … for nodes **and** edges, `m1`, `m2`, … for tags, the
*representations* tagging creates, and tag assignments. Any command that
takes an ID accepts either.

### Tags: the meta network

A tag is defined once — for nodes or for edges — and then assigned. Tags live
in their own log, which *annotates* the base: each annotation records which
version of the base its author had seen, so rewriting history invalidates
the annotations made on it. The base never refers to the meta log, so a base
can be shared on its own, and anyone can annotate someone else's graph with
their own vocabulary.

### Verification and seals

Opening an archive verifies it. By default, IndieK skips only the signature
checks your own machine already performed — the hash chain is always
recomputed — so reopening a large archive is fast; `--verify full` checks
everything.

A **seal** is a signed checkpoint of both logs and of the blobs they use. Its
hash commits to the entire archive: publish it, and anyone holding a copy can
run `ik verify --expect <hash>` to check that their copy contains exactly
what you sealed.

### Transcriptions

Cryptography ages. A **transcription** event, signed with current
algorithms, attests "I verified this log up to here, on this date". Over
generations, transcriptions carry an archive's chain of custody forward.

## Where to go next

- [Examples](/docs/examples/) — research notebooks, two-author debates,
  publishing and checking archives, reading an archive without IndieK.
- [Python SDK reference](/docs/sdk/) and [`ik` CLI reference](/docs/cli/).
- [Format specification](/docs/format/) — for implementers.
