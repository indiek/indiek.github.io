---
title: "Vision"
description: "Why IndieK exists: fostering knowledge creation, in one mind and between minds that disagree."
---

# Vision

## The mission

**To foster knowledge creation and knowledge management.**

Human cognition can do far more in its interaction with the digital world
than what exists today. Operating systems, apps, the web and AI still only
scratch the surface of what a person can build when they think with a
machine.

There is a big difference between *having a ton of information online* — as
an encyclopedia does — and *understanding*, at a technical and individual
level, a complex topic the way a molecular biologist understands their field.
Access to information is not understanding. IndieK is built around that
distinction.

IndieK aims at fostering **knowledge creation at the level of individual
minds**, and **collaborative knowledge generation through debate**.

## The vision

Two movements, one substrate:

1. **The individual.** A person building genuine understanding of a complex
   topic needs to externalise structure, not just store documents. They need
   to connect, contradict, revise and re-read their own thinking over years —
   without their work being trapped in a vendor's database or in a format that
   dies with the app that wrote it.
2. **The collective.** Understanding sharpens against opposition. IndieK treats
   **debate** as a first-class, knowledge-generating activity rather than as
   noise, and models it on the same substrate as individual thought: a claim,
   a rebuttal and the edge between them are all signed, attributable and
   revisable.

Both rest on the same technical foundation: a durable, verifiable,
implementation-independent knowledge graph archive that its authors own.

## The bet

IndieK bets on **knowledge graphs with very loose restrictions on the data
format**:

- Versatile data may be attached to **both nodes and edges**. An edge is not a
  bare pointer: it carries content, and can be argued about, tagged and
  revised exactly like a node.
- **Tags are designed freely** for both nodes and edges. IndieK ships no fixed
  ontology, no mandatory schema and no imposed taxonomy. You invent the
  vocabulary your topic needs.

This looseness is deliberate. A rigid schema encodes someone else's
understanding of your domain; premature structure is the enemy of knowledge
creation. IndieK constrains *durability* — content-addressed data, a signed
append-only history, archival-safe media types — and leaves *meaning* to you.

## Built for the long run

An archive should outlive the software that wrote it, the company that
published that software, and the cryptography it was signed with. That goal
drives every technical choice:

| Principle | Consequence in the format |
| --- | --- |
| Your archive must outlive our software | Plain folders and UTF-8 text logs; every archive carries its own specification, schemas and test vectors |
| The spec must be reimplementable | One canonical JSON form (a subset of RFC 8785), SHA-256, Ed25519, an RFC 6962 Merkle tree — nothing exotic |
| History is knowledge, not clutter | Append-only logs; nothing is edited or deleted, only *superseded* |
| Data belongs to nodes *and* edges | Both carry content: managed in the archive, a URI, or a fingerprinted local file |
| Debate requires attribution | Every event is signed by its author; only an item's author may revise it |
| Tampering must be detectable | Hash-chained events, content-addressed blobs, annotations anchored to the history they annotate |
| Checking must not depend on anyone | Seals: one published hash lets anyone verify a copy offline |
| Cryptography ages | Every hash and signature names its algorithm; *transcription* events re-attest old history under new algorithms |
| A flipped bit must not destroy an archive | Line-oriented text: damage stays local and is always reported precisely |

The details are in the [format specification](/docs/format/).

## What exists today

Everything described on this site is free and open source:

- **The IndieK archive format**, version 3.0 — the [specification](/docs/format/).
- **The `indiek` Python package**, version 1.0.0: a [Python SDK](/docs/sdk/)
  and the [`ik` command-line tool](/docs/cli/), the reference implementation
  for creating, reading, verifying, sealing and exporting archives.
- **This website**, with [examples](/docs/examples/).

A local, fully offline desktop application built on the same format is in
development.

## Roadmap

| Date | Milestone |
| --- | --- |
| 31 October 2026 | `indiek` 1.0 on PyPI, with complete documentation |
| 1 November 2026 | The project opens to external adoption and contributions |
| In progress | A local desktop application for browsing and editing archives |

From version 1.0 on, every archive written in a published format version
stays readable by later versions.

## Where to go next

- [Get started](/docs/intro/) — install, create your first archive, core concepts
- [Examples](/docs/examples/) — notebooks, debates, publishing and checking archives
- [Format specification](/docs/format/) — the archive format in full
- [Contributing](/docs/contributing/) — how to get involved
