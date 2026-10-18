---
title: "Examples"
description: "Worked IndieK examples: a research notebook, a two-author debate, publishing and checking a seal, reading an archive without IndieK, long-term custody, bulk import."
---

# Examples

Each example is self-contained and runs as written, in an empty folder, once
`indiek` is installed (see [Get started](/docs/intro/)). The Python examples
can be pasted into one session in order; the last one uses the shell.

## 1. A research notebook

Claims, sources and doubts, linked by edges that say *how* they relate — and
a revision that keeps the original.

```python
from indiek import Archive, Author, ItemKind, ResourceType

me = Author.generate()
notebook = Archive.open("notebook", author=me)

claim = notebook.create_node("Sleep consolidates declarative memory.", title="Claim")
review = notebook.create_node(
    resource_type=ResourceType.URI,
    uri="https://doi.org/10.1038/nrn2762",
    title="Diekelmann & Born (2010), The memory function of sleep",
)
doubt = notebook.create_node(
    "Replication studies report smaller effects.", title="Doubt"
)
notebook.create_edge(review, claim, "reviews the evidence for")
notebook.create_edge(doubt, claim, "qualifies")

# Refine the claim: a new version is appended, the old one stays in the log.
notebook.supersede_node(
    claim, "Sleep *contributes to* the consolidation of declarative memory."
)

open_question = notebook.create_tag("open-question", "Needs more reading", kind="node")
notebook.set_tag(open_question, claim)

# Everything tagged "open-question", with its current text.
blobs = notebook.index.store.blobs
for item in notebook.index.items.values():
    if item.kind is ItemKind.NODE and open_question in item.tags:
        print(item.alias, item.body["title"], "—", blobs.get_text(item.body["blob_hash"]))

# The full history of the claim, oldest first.
for event in notebook.events():
    if event["body"].get("node_id") == str(claim):
        print(event["header"]["timestamp"], blobs.get_text(event["body"]["blob_hash"]))
```

## 2. Two authors, one graph

Alice states a thesis; Bob disputes it with his own node, edge and tag. Bob
can annotate Alice's work but cannot rewrite it.

```python
from indiek import Archive, Author, AuthorshipError

alice, bob = Author.generate(), Author.generate()

as_alice = Archive.open("debate", author=alice)
thesis = as_alice.create_node("Remote work raises productivity.")

as_bob = Archive.open("debate", author=bob)
rebuttal = as_bob.create_node("Not once commuting time is excluded from the measure.")
as_bob.create_edge(rebuttal, thesis, "disputes")
contested = as_bob.create_tag("contested", "Someone disputes this", kind="node")
as_bob.set_tag(contested, thesis)  # Bob's tag on Alice's node

try:
    as_bob.supersede_node(thesis, "Remote work lowers productivity.")
except AuthorshipError as error:
    print(error)  # Only the author of Node … may supersede it

# Alice's session must see Bob's events before writing again.
as_alice.refresh()
reply = as_alice.create_node("Commuting time is part of the cost of office work.")
as_alice.create_edge(reply, rebuttal, "answers")

authors = {alice.public_key_hex: "Alice", bob.public_key_hex: "Bob"}
for item in as_alice.index.items.values():
    print(item.alias, item.kind, "by", authors[item.author])
```

Every event records its author's public key and signature, so who said what
is part of the archive and cannot be forged. Refresh (`Archive.refresh()`)
before writing whenever another program or person may have written since you
opened the archive: each log is a single chain, and a write based on an old
view would break it.

## 3. Publishing a seal and checking a copy

A seal hash is one short string committing to the whole archive. Publish it —
on a web page, in a paper, in print — and anyone can check that their copy
holds exactly what you sealed.

```python
from indiek import Archive, IntegrityError

seal = as_alice.seal()
published = seal.hash
print(published)  # sha256:…

# Someone receives a copy, and the published hash through another channel.
copy = Archive.open("debate", trusted_seal=published)
print(copy.verify(expect=published).seq)  # 1: this copy contains the sealed state

# Change one stored text behind the archive's back…
blob_path = copy.index.store.blobs.path_for(copy.index.get(thesis).body["blob_hash"])
original = blob_path.read_bytes()
blob_path.write_bytes(b"Remote work lowers productivity.")
try:
    Archive.open("debate", verify="full")
except IntegrityError as error:
    print(error)  # File corrupted or missing!
blob_path.write_bytes(original)  # restore it
```

From the shell, the same check is `ik verify --expect <published hash>`.
A seal found inside an archive is always checked, never trusted: anyone can
seal, so only a hash you obtained from its author proves anything.

## 4. Reading an archive without IndieK

The format is meant to outlive this software. Here is a complete check of a
base log — chain links and signatures — with the Python standard library and
PyNaCl only, following the [specification](/docs/format/):

```python
import hashlib
import json
from pathlib import Path

from nacl.signing import VerifyKey


def canonical(value):
    """Canonical bytes: sorted keys, no whitespace, UTF-8."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256(value):
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


previous = None
for path in sorted(Path("debate/events").rglob("*ndjson"), key=str):
    for line in path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        expected = None if previous is None else sha256(previous)
        assert event["header"]["prev_hash"] == expected, "chain broken"
        unsigned = {key: value for key, value in event.items() if key != "signature"}
        signature = bytes.fromhex(event["signature"].removeprefix("ed25519:"))
        VerifyKey(bytes.fromhex(event["header"]["author"])).verify(
            canonical(unsigned), signature
        )
        previous = event

print("head:", sha256(previous))
print("same as IndieK:", sha256(previous) == Archive.open("debate").head)
```

A full independent implementation also checks the blobs, the meta anchors and
the seals, and must reproduce `test_vectors.json`.

## 5. Long-term custody

Before moving an archive to new storage, or years after it was written,
attest what you verified and make the archive self-describing:

```python
from pathlib import Path

curator = Archive.open("debate", author=Author.generate())
curator.transcribe(note="Re-verified before migration to new storage")
curator.write_manifest()

print(sorted(path.name for path in Path("debate").iterdir()))
# ['MANIFEST.json', 'SPEC.md', 'blobs', 'events', 'meta', 'seals', 'test_vectors.json']
report = curator.fsck()  # a full verification, then a summary
print(report.base_count, report.meta_count, report.seal_count, report.transcriptions)
# 6 3 1 {'base': 1, 'meta': 0}
```

The transcription is signed by the curator's key and records the head and
length of the log it verified. When SHA-256 or Ed25519 are one day retired,
transcriptions signed with their successors carry the chain of custody
forward. `SPEC.md` and `test_vectors.json` travel with the archive, so a
reader decades from now needs nothing else.

## 6. Importing a folder of notes

With the CLI: every file of a folder becomes a node titled by its name, and
a small CSV file declares the edges.

```bash
ik keygen --write
ik config --set-archive-path ~/archives/reading-notes

ls notes/
# attention.md  memory.md  sleep.txt

ik ingest --input-folder notes          # e1 attention, e2 memory, e3 sleep
printf 'e3,e2,supports\ne1,e2,is needed for\n' > edges.csv
ik ingest --edges-def-file edges.csv    # e4, e5

ik create_node_tag --name topic --description "A research topic"   # m1
ik set_tag --tag m1 --id e2
ik export --output-path reading-notes.graphml --tags m1
ik read
```

The GraphML file opens in graph tools such as Gephi or yEd. Hidden files
(such as `.DS_Store`) stop an import; remove them first.
