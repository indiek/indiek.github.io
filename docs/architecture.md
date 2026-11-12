---
title: "Architecture"
description: "How the IndieK pieces fit together: the indiek SDK and ik CLI, the local API, the web UI and the IndieK Desktop App."
---

# Architecture

IndieK is one format and four pieces of free software built on it. Each
piece is useful on its own, and each builds on the one below it:

```text
┌──────────────────────────────────────────────────────────────────────┐
│ IndieK Desktop App (Tauri)  — one installer for macOS, Windows, Linux │
│   ┌──────────────────────────────┐   ┌─────────────────────────────┐ │
│   │ window: the web UI           │──►│ sidecar: local API + ik CLI │ │
│   │ (graph explorer)             │   │ (127.0.0.1 only)            │ │
│   └──────────────────────────────┘   └──────────────┬──────────────┘ │
└─────────────────────────────────────────────────────┼────────────────┘
                                                      ▼
                                   indiek SDK ──► archive folder on disk
                                                  (often a git repository)
```

| Piece | What it is | For whom | Where it is published |
| --- | --- | --- | --- |
| **`indiek`** | The Python SDK and the `ik` command line; the reference implementation of the [format](/docs/format/) | Python developers, command-line users | [PyPI](https://pypi.org/project/indiek/) · [GitHub](https://github.com/indiek/indiek) |
| **`indiek-api`** | The [local API](/docs/api/): an HTTP server on your own computer that opens archives with the SDK and serves the web UI | The desktop app; developers building their own interface | [PyPI](https://pypi.org/project/indiek-api/) · [GitHub](https://github.com/indiek/indiek-api) |
| **Web UI** | The [graph explorer](/docs/web-ui/): browse, filter and write a knowledge graph in a browser window | Everyone | [GitHub Releases](https://github.com/indiek/indiek-webui/releases) (a built bundle) |
| **IndieK Desktop** | The [desktop app](/docs/desktop/): the API, the web UI and the `ik` command in one installer, with no Python or Node.js to install | Everyone | [GitHub Releases](https://github.com/indiek/indiek-desktop/releases) |

All four are licensed under the [Apache License 2.0](/docs/license/).

## The archive is the source of truth

Every piece reads and writes the same thing: an archive folder, through the
`indiek` SDK. None of them keeps a database or a copy of your data of its
own. Caches and indexes can be deleted at any time, since they are rebuilt from
the signed logs.

So the tools are interchangeable. You can write a node in the desktop app,
supersede it with `ik`, pull a collaborator's changes with `git`, and the
app shows the result. It re-verifies the archive whenever its logs change
on disk, whoever changed them.

## How the desktop app runs

1. You start IndieK. The window shows "Starting the local IndieK server…".
2. The app starts its **sidecar**, one bundled program that contains the
   local API and the `ik` command line. The sidecar listens on `127.0.0.1`
   only, on a random free port.
3. The sidecar sends the app, privately through a pipe, a single-use
   **launch link**. The window opens it and is logged in; nobody else can
   reuse the link.
4. The window shows the web UI, served by the sidecar. Every action in the
   UI is an HTTP call to the sidecar, which performs it with the SDK.
5. When you quit, the app closes the pipe and the sidecar stops. If the app
   crashes, the operating system closes the pipe and the sidecar stops too:
   no server is left running in the background.

The page in the window gets no special access to your computer. It talks
only to the local API, and the window may only navigate to the local server.

## Local and offline

- Everything runs on your computer. The API refuses connections from the
  network and requests addressed to any host name other than the local one.
- No account, no sign-in, no cloud service: the app works without an
  internet connection.
- Your archives stay where they are. The app edits archive folders **in
  place** and only remembers *which* folders you opened (in
  `~/.indiek/workspaces.json`). Removing one from the list never touches
  its files.

## One signing key for every tool

Writes are signed with your author key (an Ed25519 key pair; see
[authors and signatures](/docs/intro/#authors-and-signatures)). The desktop
app keeps it in your operating system's keychain, in the item with service
`indiek` and account `author-seed`, the same item `ik keygen --keychain` uses.
A key created in the app therefore also works with `ik`, and the other way
round.

The app's **Install ik Command…** menu item puts the bundled `ik` on your
command line. It is the same program as the app, so the keychain does not
ask again for permission.

The secret key never reaches the web page. The API signs on its behalf, and
key backups are encrypted with your password before they leave the API.

## Versions and releases

Each piece has its own repository, its own version number and its own
changelog, so each can improve at its own pace. The desktop repository holds
no component code. It **pins** an exact, tested release of each:

| Pinned in the desktop repository | Pins |
| --- | --- |
| `pyproject.toml` | `indiek-api` and `indiek` (from PyPI) |
| `web-ui.lock.json` | the web UI release, with the SHA-256 of its bundle |

A new SDK, API or web UI release reaches users when the desktop app moves
its pin and publishes a new release. Every desktop release states the
versions it bundles in its changelog.

Release outputs:

| Piece | A release produces |
| --- | --- |
| `indiek` | a package on PyPI |
| `indiek-api` | a package on PyPI |
| Web UI | `custom-graph-explorer-<version>-out.tar.gz` and its `.sha256`, attached to a GitHub Release |
| IndieK Desktop | installers for macOS (`.dmg`), Windows (`.msi`, `.exe`) and Linux (`.AppImage`, `.deb`), with `SHA256SUMS.txt`, attached to a GitHub Release |

## Where to go next

- [IndieK Desktop](/docs/desktop/): install the app and start using it.
- [Web UI guide](/docs/web-ui/): everything the graph explorer can do.
- [Local API](/docs/api/): run the server yourself, its configuration,
  security model and routes.
- [Get started](/docs/intro/): the concepts, and the SDK and CLI.
- [Contributing](/docs/contributing/): how to work on any of the pieces.
