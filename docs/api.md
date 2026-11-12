---
title: "Local API"
description: "indiek-api, the local HTTP server behind the IndieK web UI and desktop app: install, run, configure, its security model, routes and errors."
---

# Local API

`indiek-api` is a small HTTP server that runs **on your own computer**. It
opens archive folders in place with the [`indiek` SDK](/docs/sdk/), verifies
them, and exposes their current state and the write operations over HTTP.
It serves the [web UI](/docs/web-ui/), and the [desktop app](/docs/desktop/)
bundles it.

```text
web UI (browser or app window) ──HTTP──► indiek-api (127.0.0.1 only) ──► indiek SDK ──► archive folder
```

Use it directly to:

- run the web UI in your own browser, without the desktop app;
- build another interface or script on top of a stable HTTP contract;
- embed the API in your own Python application.

It is free software ([Apache-2.0](/docs/license/)), published on
[PyPI](https://pypi.org/project/indiek-api/) and
[GitHub](https://github.com/indiek/indiek-api).

## Install and run

It needs Python 3.14 or newer.

```bash
uvx indiek-api                    # run it once, without installing
uv tool install indiek-api        # or install the indiek-api command
indiek-api --no-browser
```

The server picks a random free port on `127.0.0.1` and prints a one-time
**launch link**:

```text
IndieK Desktop: open http://127.0.0.1:51234/api/session?token=…
```

Open it once in your browser (by default it opens by itself): it logs that
browser in and redirects to the UI. Each restart prints a new link, and a
link works only once.

Interactive API documentation is served at `/docs`, the OpenAPI schema at
`/openapi.json`.

### Serve the web UI

The server serves a built web UI when `INDIEK_API_STATIC_DIR` points at it:

```bash
mkdir web-ui && tar -xzf custom-graph-explorer-<version>-out.tar.gz -C web-ui
INDIEK_API_STATIC_DIR="$PWD/web-ui" indiek-api
```

Download the bundle from the
[web UI releases](https://github.com/indiek/indiek-webui/releases). The
server then answers `/api/*` and `/health` itself and serves every other
path from that folder. Restart the server after replacing the folder:
the security policy is computed from the UI files at startup.

## Configuration

All settings are environment variables. A `.env` file is read too
(`INDIEK_API_ENV_FILE`); real environment variables win.

| Variable | Default | Meaning |
| --- | --- | --- |
| `IK_AUTHOR_PRIVATE_KEY` | none | The 64-hex Ed25519 secret that signs writes (same variable as `ik`). Takes precedence over the keychain key. Without either, reads work and writes fail with `author_key_missing` |
| `INDIEK_API_ENV_FILE` | `.env` | Dotenv file loaded at startup |
| `INDIEK_API_REGISTRY` | `~/.indiek/workspaces.json` | The list of opened archive folders |
| `INDIEK_API_PORT` | a random free port | A fixed port (the host is always `127.0.0.1`) |
| `INDIEK_API_TOKEN` | random, per launch | A fixed token, **for development and tests only** (16 characters or more); its launch link stays reusable |
| `INDIEK_API_OPEN_BROWSER` | `1` | `0` only prints the launch link (same as `--no-browser`) |
| `INDIEK_API_STATIC_DIR` | none | The built web UI to serve at `/` |
| `INDIEK_API_CSP_REPORT_ONLY` | `0` | `1` reports Content-Security-Policy violations in the browser console instead of blocking (debugging) |
| `INDIEK_API_CORS_ORIGINS` | none | Comma-separated origins allowed to call the API from another origin |
| `IK_CACHE_DIR` | the SDK's default | Where the SDK keeps its verification cache ([SDK](/docs/sdk/)) |

To experiment without touching your real workspace list:

```bash
INDIEK_API_REGISTRY=/tmp/ik-registry.json indiek-api
```

### Command-line flags

| Flag | Effect |
| --- | --- |
| `--no-browser` | Print the launch link, do not open a browser |
| `--handshake` | Print exactly one JSON line on stdout, `{"indiek_api": "<version>", "port": <port>, "launch_url": "<url>"}`, send all logs to stderr and never open a browser. For a parent program (the desktop app) that reads the launch link through a pipe |
| `--exit-on-stdin-eof` | Stop when stdin closes, so the server never outlives its parent program |

## Security model

The server can sign in your name, so it defends itself even against other
programs and web pages on the same computer:

- **Loopback only.** It binds to `127.0.0.1` and answers only requests whose
  `Host` is `127.0.0.1`, `localhost` or `[::1]`. This defeats DNS-rebinding
  attacks from web pages.
- **A per-launch token.** Every `/api/*` route needs it, either as
  `Authorization: Bearer <token>` or as the session cookie set by the launch
  link (`HttpOnly`, `SameSite=Strict`). The launch link works once.
  `/health` and the UI files are public.
- **A header on every write.** `POST`, `PUT`, `PATCH` and `DELETE` on
  `/api/*` also need `X-IndieK-Request: 1`. A page from another origin would
  need a CORS preflight to send it, and the server never grants one.
- **A strict Content-Security-Policy.** Only the UI's own scripts, listed
  by hash, may run; no inline or `eval` code. Archived content (blobs) is
  served under a sandboxed policy with `nosniff`, so a hostile file in an
  archive cannot run code in the UI.
- **The secret key never leaves the server.** `/api/identity` returns the
  public key only; key backups are encrypted (Argon2id) before they are
  sent.

## Routes

Archive routes live under `/api/workspaces/{workspace_id}` (written `…`
below). Item references accept a UUID or an alias (`e3`); tag references a
UUID or an `m` alias (`m1`). The schemas of every request and response are
at `/docs`.

### Server and session

| Method and path | Body | Response |
| --- | --- | --- |
| `GET /health` | | `{"status": "ok", "api_version": "<version>"}` (no token needed) |
| `GET /api/session?token=…` | | `303` to `/` with the session cookie; `401` if the token is wrong or used |

### Author key

| Method and path | Body | Response |
| --- | --- | --- |
| `GET /api/identity` | | `{public_key, source, keychain_available}`, source `env`, `keychain` or `none` |
| `POST /api/identity/generate` | `{replace?}` | `201`: a new key, stored in the OS keychain |
| `POST /api/identity/import` | `{seed_hex}` or `{backup, password}`, plus `replace?` | `201` |
| `POST /api/identity/backup` | `{password}` (12+ characters) | The encrypted backup file `indiek-key-<8 hex>.ikkey` |

### Workspaces

| Method and path | Body | Response |
| --- | --- | --- |
| `GET /api/workspaces` | | `[{workspace_id, name, path, created_at}]` |
| `POST /api/workspaces` | `{path, create?}`; `create: true` starts an archive in a new or empty folder | `201` registered, `200` already known |
| `DELETE /api/workspaces/{id}` | | `204`: forgets the folder; its files are never touched |

### Reading an archive

| Method and path | Response |
| --- | --- |
| `GET …/graph` | `{head, meta_head, nodes[], edges[], tags[]}`: current state, supersedes applied, with aliases and tag kinds |
| `GET …/blobs/{sha256}` | The content's bytes, with its media type (a hash prefix is accepted) |
| `GET …/events` | The base and meta event logs in log order (like `ik read`) |

### Writing to an archive

| Method and path | Body | Response |
| --- | --- | --- |
| `POST …/nodes` | `{content, title?, media_type?}` (managed), `{resource_type: "uri", uri, title?}` or `{resource_type: "local_file", path, title?}` | `201 {id, alias}` |
| `PUT …/nodes/{id}` | `{content, title?}` (stored as Markdown) | `{id, alias}`: supersedes the node |
| `POST …/edges` | `{source, target, content?}`; no `content` for an edge without content | `201 {id, alias}` |
| `PUT …/edges/{id}` | `{content?}`; `null` removes the content | `{id, alias}`: supersedes the edge |
| `POST …/tags` | `{name, description, kind}` with kind `node` or `edge` | `201 {id, alias}` |
| `POST …/tags/{tag}/assignments` | `{target}` | `201 {target, tags[]}`; the tag kind must match the target, and only the tag's author may assign it |

Example, with a fixed development token:

```bash
TOKEN=dev-token-0123456789
INDIEK_API_PORT=8765 INDIEK_API_TOKEN=$TOKEN indiek-api --no-browser &

curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8765/api/workspaces
curl -s -X POST http://127.0.0.1:8765/api/workspaces/<id>/nodes \
  -H "Authorization: Bearer $TOKEN" -H "X-IndieK-Request: 1" \
  -H "Content-Type: application/json" \
  -d '{"content": "Understanding is not retrieval", "title": "Thesis"}'
```

## Errors

Every error is `{"detail": "<message>", "code": "<stable code>"}`. Programs
should branch on `code`; `detail` is for people.

| Status | `code` | When |
| --- | --- | --- |
| 400 | `invalid_host` | The `Host` header is not a loopback name |
| 401 | `unauthorized` | No valid token or session, or a wrong or used launch link |
| 403 | `missing_request_header` | A write without `X-IndieK-Request: 1` |
| 403 | `forbidden` | Assigning another author's tag |
| 404 | `workspace_not_found`, `item_not_found`, `blob_not_found`, `archive_not_found` | Unknown workspace, item, alias or hash, or the folder does not exist |
| 409 | `ambiguous_archive` | The folder contains several archives; `candidates` lists them |
| 409 | `archive_integrity` | Broken chain, bad signature or missing content: the archive on disk is inconsistent |
| 409 | `archive_locked` | Another program held the archive's write lock (`.ik.lock`) for more than 10 s; retry |
| 409 | `key_exists` | Generating or importing a key while one is stored, without `replace` |
| 422 | `archive_rule` | The SDK refused the operation (for example a tag kind that does not match the target) |
| 422 | `invalid_key`, `invalid_backup`, `weak_password` | A malformed key, a wrong backup password or damaged file, a password under 12 characters |
| 422 | none | Request validation; `detail` lists the problems |
| 503 | `author_key_missing` | A write without an author key |
| 503 | `keychain_unavailable` | No usable OS keychain; set `IK_AUTHOR_PRIVATE_KEY` instead |

## Consistency with `ik`

The API writes exactly what `ik` would write: same events, same signatures,
same aliases; the API's test suite compares both. Archives stay shared:

- The API re-verifies an archive (chain, signatures, content) whenever its
  logs change on disk, whoever changed them: the API, `ik`, or `git pull`.
- Writes from the API and from `ik` exclude each other through the SDK's
  write lock, `.ik.lock` in the archive folder.

## Embedding as a library

`indiek_api.app.create_app(settings=None, *, workspaces=None, signer=None)`
returns the FastAPI application. Pass your own objects to change where
workspaces come from and who signs; they only need to match the protocols of
`indiek_api.providers`:

| Protocol | Methods | Default |
| --- | --- | --- |
| `WorkspaceProvider` | `list`, `register`, `remove`, `service` | the JSON workspace list |
| `Signer` | `author`, `author_or_none` | environment key, else the OS keychain |
| `KeyManager` (optional) | `status`, `store`, `backup`, `read_backup` | as above; the `/api/identity` routes exist only when the signer is also a `KeyManager` |

## Contributing

Code layout, test fixtures, conventions and the recipe for adding a route:
the [API repository's README](https://github.com/indiek/indiek-api#readme).
