---
title: "Web UI guide"
description: "Everything the IndieK graph explorer can do: open archives, explore the graph, filter and colour by tags, write nodes, edges and tags, and manage your author key."
---

# Web UI guide

The **graph explorer** is IndieK's graphical interface. It shows an
archive's knowledge graph, lets you read every node and edge, filter by tags
and write new content, all signed with your [author key](/docs/desktop/#your-author-key).

You normally get it inside the [desktop app](/docs/desktop/). Developers can
also run it in a browser, served by the [local API](/docs/api/)
([Run it yourself](#run-it-yourself)).

## The home screen

Type the **absolute path** of a folder, then:

| Button | Does |
| --- | --- |
| **Open workspace** | Opens an existing archive. The path may be the archive itself or a folder containing exactly one archive; if there are several, the UI lists them to pick from |
| **New archive** | Creates an empty archive in a new or empty folder |

A *workspace* is simply a folder the app remembers. The list below the field
shows them; open one with a click, or remove it from the list. Removing a
workspace never touches its files.

The **Home** button in the header brings you back here and clears the current
view (selection, filters, colours).

## The workspace view

| Area | Shows |
| --- | --- |
| **Header** | The workspace name, the buttons **Create node**, **Create edge** and **Create tag**, and your author-key chip |
| **Graph** (left, top) | The nodes and edges, with a minimap |
| **Tags** (left, bottom) | Node tags and edge tags, with search, filters and colours |
| **Item detail** (right) | The selected node or edge: content, metadata, tags and actions |

Each pane can be collapsed to a thin strip and reopened from it, to give the
graph more room.

## Exploring the graph

### Mouse

| Action | Effect |
| --- | --- |
| Click a node or an edge | Selects it and shows it in the item detail pane |
| Click empty space | Clears the selection |
| Drag empty space | Moves the view; the scroll wheel zooms |
| Drag a node | Moves it |
| Double-click empty space | Opens the node editor to create a node **at that spot** |
| Drag the **+** handle of the selected node | Draws an arrow; click another node to create an edge to it, click elsewhere or press Esc to cancel |

### Keyboard

Click the graph once to give it the keyboard focus, then:

| Keys | Effect |
| --- | --- |
| Arrow | Follow an **outgoing** edge in that direction on screen |
| Space + Arrow | Follow an **incoming** edge in that direction |
| Shift + Arrow | Select the edge in that direction |
| N / Shift + N | Cycle through the other candidates of the last move |
| Esc | Drop the cycle, or cancel drawing an edge |

Tab is deliberately not captured, so the keyboard can always leave the
graph.

### Graph settings

The ⚙ button above the graph opens **Graph settings**:

- **Layout**: *Continuous force* (default), *Directed chain* (follows the
  edge direction) or *Preset*. **↻ Re-layout** arranges everything again.
- **Style**: node size and shape, edge labels, and other display options.
- **Tag style**: the style applied to items carrying a given tag.

The layout runs only when a workspace opens, when you change it, or on
**↻ Re-layout**. Creating items or filtering never moves the nodes already on
screen: new nodes appear in free space (or where you double-clicked).

## Reading items

The item detail pane shows the selected item:

- **Nodes**: the title and content. Markdown is rendered (CommonMark plus
  GitHub tables, lists and strikethrough); PNG and JPEG images display inline
  and open in a zoomable viewer; PDF and TIFF files are offered as downloads
  (an in-app PDF viewer is planned). `uri` nodes show their link;
  `local_file` nodes show the recorded path, size and hash.
- **Edges**: their source and target, and their content, if they have any.
- For both: the alias (`e1`, `e2`, …), the author's key (abbreviated; hover
  for the full key), the creation and last-update dates, and the tags.

To see an item's full history of versions, use `ik read` on the command line.

The UI never runs scripts or HTML contained in archived content.

## Writing

Every write is a signed event appended to the archive, exactly as `ik` would
write it. Nothing is ever overwritten: revisions keep the history (see
[Revisions](/docs/intro/#revisions)). Writing needs an author key; without
one, the UI opens the **Author key** dialog.

### Nodes

**Create node** (or double-click the graph) opens the node editor:

| Kind | Content | Stored as |
| --- | --- | --- |
| **Text** | Markdown or plain text, with a preview tab | a `managed` node: the text is copied into the archive |
| **URL** | a link | a `uri` node: recorded, never fetched |
| **Local file** | the path of a file on your computer | a `local_file` node: path, size and SHA-256 recorded; the file stays where it is |

An optional **title** applies to every kind. Images and PDFs can be archived
with `ik create_node --content <file>` for now; creating them from the UI is
planned.

### Revising a node

**Supersede** in the item detail pane opens the editor with the current
content; your edit becomes a new version of the same node (same identifier,
same alias). Only the node's author can supersede it. Text nodes can be
superseded from the UI; images and PDFs not yet.

### Edges

- **Create edge** in the header, **New edge from here** in the item detail
  pane, or the **+** handle on the graph.
- Pick the source and the target (by alias or title) and, optionally, the
  edge's text: "proves", "contradicts", "is an example of". An edge may have
  no content at all.
- **Supersede** on a selected edge changes its content, or removes it. The
  endpoints of an edge never change.

### Tags

- **Create tag**: a name, a description and a kind, *node* tag or *edge*
  tag.
- **Assign tag** in the item detail pane: pick a tag of the matching kind.
  You can assign only the tags you created; anyone can create their own.

## Tags pane: filter and colour

- **Search** tags by name.
- Node tags and edge tags are listed in two columns.
- **Filter**: toggle tags to show only the items carrying them; clear the
  filters to see everything again.
- **Colour**: pick a colour per tag to colour the items carrying it.

Filters, colours, graph settings and node positions are not saved yet: they
reset when you reload or reopen the workspace.

## Author key

The chip in the header shows your public key and its source (`keychain` or
`env`). Click it to open the **Author key** dialog:

- **Create** a key (stored in the OS keychain), then download its encrypted
  backup;
- **Import** a key from a backup file or from its hexadecimal secret;
- **Back up** the current key into a password-encrypted `.ikkey` file.

The secret key never reaches the page: the local API stores it, signs with
it, and encrypts backups before sending them. Details and safe deletion:
[Keep your key safe](/docs/desktop/#keep-your-key-safe).

## Current limitations

- Filters, colours, graph settings and positions are not persisted.
- PDF and TIFF nodes are downloads, not previews.
- Image and PDF nodes cannot yet be created or superseded from the UI (use
  `ik`).
- Folders are opened by typing their path; a folder picker is planned.

## Run it yourself

The graph explorer is a Next.js application exported as static files: it
has no server of its own and talks only to the [local API](/docs/api/), on
the same origin. Two ways to run it outside the desktop app:

- **Built**: download `custom-graph-explorer-<version>-out.tar.gz` from the
  [web UI releases](https://github.com/indiek/indiek-webui/releases), unpack
  it, and start the API with `INDIEK_API_STATIC_DIR` pointing at the folder
  ([Serve the web UI](/docs/api/#serve-the-web-ui)).
- **From source**, with hot reload: see the
  [web UI repository's README](https://github.com/indiek/indiek-webui#3-first-time-setup)
  (Node.js, `npm run dev`, a dev proxy to the API). The README also
  describes the code layout, state management, testing and how to add an
  API call.
