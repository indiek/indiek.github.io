---
title: "IndieK"
home: true
---

<section class="hero">
<div class="hero-inner">
<div>
<h1>Knowledge graphs, archived to last.</h1>
<p>IndieK is an open archival format for knowledge graphs: plain files, signed
by their authors, append-only, and verifiable by anyone — with nothing but a
published specification and standard cryptography.</p>
<div class="buttons">
<a class="button primary" href="/docs/intro/">Get started</a>
<a class="button secondary" href="/docs/mission/">Read the vision</a>
<a class="button secondary" href="/docs/format/">The specification</a>
</div>
</div>
<div markdown="1">

```python
from indiek import Archive, Author

ik = Archive.open("my-archive", author=Author.generate())

theorem = ik.create_node("Gödel's first incompleteness theorem")
proof = ik.create_node("Diagonalisation over provability.")
ik.create_edge(proof, theorem, "proves")

tag = ik.create_tag("theorem", "A proven statement", kind="node")
ik.set_tag(tag, theorem)

print(ik.seal().hash)  # one hash commits to everything
```

</div>
</div>
</section>

<section class="section">
<h2>Why IndieK</h2>
<div class="cards">
<div class="card"><h3>Plain files</h3><p>An archive is a folder of UTF-8 text logs and content-addressed files. No database, no server, no proprietary container.</p></div>
<div class="card"><h3>Signed and chained</h3><p>Every event is signed with its author's Ed25519 key and linked to the previous one by a hash. Any change to the history is detected.</p></div>
<div class="card"><h3>Nothing is overwritten</h3><p>Revisions are new events; earlier versions stay in the log. How your understanding evolved is part of the knowledge.</p></div>
<div class="card"><h3>Edges carry content</h3><p>A connection between two ideas has its own text, author, tags and history. "Why are these linked?" gets a first-class answer.</p></div>
<div class="card"><h3>Your vocabulary</h3><p>No fixed ontology. Tags are designed freely, for nodes and for edges, and anyone can annotate a graph with their own key.</p></div>
<div class="card"><h3>Built to be checked</h3><p>Seals commit to a whole archive in one short hash. Publish it, and anyone can verify their copy — offline, without trusting anyone.</p></div>
</div>
</section>

<section class="section soft">
<div class="two-col">
<div markdown="1">

## An archive in thirty seconds

```text
my-archive/
├── events/…/events.ndjson       the knowledge graph
├── meta/events/…/events.ndjson  tags on it
├── blobs/sha256/71/a0/71a0b5…   content, named by its hash
├── seals/seals.ndjson           signed checkpoints
├── SPEC.md                      the specification itself
└── MANIFEST.json                layout and JSON Schemas
```

</div>
<div markdown="1">

## Durable by design

The signed event logs and the blobs *are* the archive; every index or view is
rebuilt from them. Archives carry their own specification and test vectors,
so a reader in fifty years needs neither this website nor our code. Hashes
and signatures name their algorithms, and *transcription* events let future
generations re-attest old history with newer cryptography.

[How the format works →](/docs/format/)

</div>
</div>
</section>

<section class="section">
<div class="two-col">
<div markdown="1">

## From the shell

```bash
uv tool install 'indiek[cli]'
ik keygen --write
ik config --set-archive-path ~/archives/notes
ik create_node --content "Understanding is not retrieval"
ik create_node --content ./notes/limits.md
ik create_edge --source-node e2 --target-node e1 --content "illustrates"
ik seal
ik verify
```

[CLI reference →](/docs/cli/)

</div>
<div markdown="1">

## From Python

```python
from indiek import Archive

reader = Archive.open("my-archive")  # read-only
for item in reader.index.items.values():
    print(item.alias, item.kind, item.author[:8])

print(reader.verify())       # full check, latest seal
print(reader.fsck().blob_files)
```

[SDK reference →](/docs/sdk/) · [Examples →](/docs/examples/)

</div>
</div>
</section>

<section class="section soft">
<div markdown="1">

## Status

<div class="status">
<span><strong>indiek 1.0.0</strong> — Python SDK and <code>ik</code> CLI</span>
<span><strong>Format 3.0</strong> — first public version</span>
<span><strong>1 November 2026</strong> — contributions open</span>
<span><strong>Desktop app</strong> — development is underway</span>
</div>

The format specification and the `indiek` package are free and open source
under the Apache License 2.0. Read [the vision](/docs/mission/), then
[get started](/docs/intro/).

</div>
</section>
