---
title: Format specification
layout: default
---

## Overview

A IAF archive is a directory containing:

1. `MANIFEST.json` — JSON metadata describing the archival format.
2. `events/` — an append-only Merkle DAG event log enabling anyone to reconstruct the knowledge graph (without the underlying data attached to the nodes and edges).
3. `blobs/` — optional blob store containing content-addressed binary data attached to the nodes and edges of the graph.
4. `meta/` — an append-only merkle DAG event log that only contains metadata corresponding to tags.

A small example archive can look like this for example:
```
archive/
├── blobs
│   └── sha256
│       └── 26
│           └── 09
│               └── 2609c7c28788898a337c063ff1c3b92275832bddeda014a790d109fad3ba85e2
├── events
│   └── 2026
│       └── 08
│           └── 09
│               └── events.ndjson
├── MANIFEST.json
└── meta
    └── events
        └── 2026
            └── 08
                └── 09
                    └── events.ndjson

```

### Manifest schema (example)

```json
{
  "format": "IndieK Public Archive",
  "format_version": "2.0",
  "description": "This MANIFEST.json documents the layout and schemas of an IndieK archive.  It is intended to allow any consumer to parse the archive independently of the original software, now or in the future.",
  "authors": [
    {
      "public_key": "51e6d165f6f2db95f08fe87b577b4c9fc9d5be9b878f87fdb1d1a1a57d5eefbb",
      "algorithm": "Ed25519"
    }
  ],
  "blob_store": {
    "description": "Content-addressed blob store.  Every blob is immutable once written.",
    "root": "<archive_root>/blobs/sha256/",
    "path_pattern": "<root>/<hex[0:2]>/<hex[2:4]>/<sha256_hex>",
    "example": "blobs/sha256/ab/cd/abcd1234...ef",
    "notes": [
      "The filename is the full 64-character SHA-256 hex digest of the blob bytes.",
      "The two-level sharding (first 2 + next 2 hex chars) keeps directories small.",
      "To retrieve a blob referenced by 'sha256:XXXX' in an event, strip the 'sha256:' prefix and navigate to blobs/sha256/<XXXX[0:2]>/<XXXX[2:4]>/<XXXX>."
    ]
  },
  "event_log": {
    "description": "Append-only event log stored as date-sharded NDJSON files.  Reading ALL files in chronological order (by filesystem path) produces the complete, ordered event sequence.",
    "base_event_log_root": "<archive_root>/events/",
    "meta_event_log_root": "<archive_root>/meta/events/",
    "path_pattern": "<log_root>/YYYY/MM/DD/events.ndjson",
    "file_format": "NDJSON (one JSON object per line, UTF-8 encoded)",
    "ordering": "Sort all ndjson file paths lexicographically before reading.  Within a file, events are in append order (top = oldest).",
    "chain_integrity": "Each event's header.prev_hash is the SHA-256 of the *entire* preceding event JSON (keys sorted, compact).  The genesis event has prev_hash=null.  The hash of the final event is the canonical unique identifier for the archive at that point in time: two archives are identical iff their last event hashes match.",
    "signature_algorithm": {
      "signing_curve": "Ed25519",
      "library_reference": "PyNaCl / libsodium",
      "what_is_signed": "SHA-256 digest of the event body serialised as compact JSON with keys sorted alphabetically (json.dumps(body, sort_keys=True)).",
      "signature_encoding": "lowercase hex string"
    }
  },
  "schemas": {
    "EventHeader": {
      "description": "Header present in every event and meta-event.",
      "fields": {
        "version": {
          "type": "string",
          "description": "Format version string (for example '2.0'). Consumers MUST reject events whose version they do not recognise."
        },
        "prev_hash": {
          "type": "string | null",
          "description": "SHA-256 hex digest (64 lower-case hex characters) of the *entire* preceding event JSON object, serialised with keys sorted alphabetically and no extra whitespace.  null for the genesis event."
        },
        "timestamp": {
          "type": "string",
          "format": "ISO-8601 datetime with timezone",
          "description": "Wall-clock time at which the event was written by the author."
        },
        "author": {
          "type": "string",
          "description": "64-character hex-encoded Ed25519 public key of the event author.  This key MUST appear in MANIFEST.json > authors."
        }
      }
    },
    "EventBody": {
      "description": "Body of a base-network event.  Exactly one of the body types below is present, discriminated by the body_type field.",
      "body_types": {
        "node": {
          "discriminator": "body_type = 'node'",
          "fields": {
            "body_type": {
              "const": "node"
            },
            "event_type": {
              "const": "create_node"
            },
            "node_id": {
              "type": "UUID v7 string",
              "description": "Unique identifier for the node."
            },
            "title": {
              "type": "string | null",
              "description": "Optional human-readable title."
            },
            "media_type": {
              "type": "string | null",
              "enum": [
                "text/plain; charset=utf-8",
                "text/markdown; charset=utf-8",
                "image/tiff",
                "image/png",
                "image/jpeg",
                "application/pdf; profile=pdfa"
              ],
              "description": "Required for managed and local_file resources; optional URI hint."
            },
            "resource_type": {
              "type": "string",
              "enum": [
                "managed",
                "uri",
                "local_file"
              ],
              "default": "managed",
              "description": "Missing in format 1.0 events implies managed."
            },
            "blob_hash": {
              "type": "string | null",
              "pattern": "^sha256:[0-9a-f]{64}$",
              "description": "Content-address of the managed blob. Present only when resource_type is managed."
            },
            "uri": {
              "type": "string | null",
              "description": "Required external URI when resource_type is uri."
            },
            "path": {
              "type": "string | null",
              "description": "Required local path when resource_type is local_file."
            },
            "file_size": {
              "type": "integer | null",
              "minimum": 0,
              "description": "Verified byte length for local_file."
            },
            "file_hash": {
              "type": "string | null",
              "pattern": "^sha256:[0-9a-f]{64}$",
              "description": "SHA-256 fingerprint for local_file."
            },
            "last_verified": {
              "type": "string | null",
              "format": "ISO-8601 datetime",
              "description": "Time local_file metadata was last verified."
            }
          },
          "resource_rules": {
            "managed": "requires blob_hash and media_type; excludes uri/local-file fields",
            "uri": "requires uri; media_type is an optional hint; excludes blob_hash/local-file fields",
            "local_file": "requires path, file_size, file_hash, last_verified, and media_type; excludes uri/blob_hash"
          }
        },
        "edge": {
          "discriminator": "body_type = 'edge'",
          "fields": {
            "body_type": {
              "const": "edge"
            },
            "event_type": {
              "const": "create_edge"
            },
            "edge_id": {
              "type": "UUID v7 string"
            },
            "source_node": {
              "type": "UUID v7 string",
              "description": "node_id of the edge's source node."
            },
            "target_node": {
              "type": "UUID v7 string",
              "description": "node_id of the edge's target node."
            },
            "title": {
              "type": "string | null"
            },
            "resource_type": {
              "$ref": "node.resource_type"
            },
            "media_type": {
              "$ref": "node.media_type"
            },
            "blob_hash": {
              "$ref": "node.blob_hash"
            },
            "uri": {
              "$ref": "node.uri"
            },
            "path": {
              "$ref": "node.path"
            },
            "file_size": {
              "$ref": "node.file_size"
            },
            "file_hash": {
              "$ref": "node.file_hash"
            },
            "last_verified": {
              "$ref": "node.last_verified"
            }
          }
        },
        "supersede_node": {
          "discriminator": "body_type = 'supersede_node'",
          "fields": {
            "body_type": {
              "const": "supersede_node"
            },
            "event_type": {
              "const": "supersede_node"
            },
            "node_id": {
              "type": "UUID v7 string",
              "description": "ID of an existing node to supersede."
            },
            "title": {
              "type": "string | null"
            },
            "resource_type": {
              "$ref": "node.resource_type"
            },
            "media_type": {
              "$ref": "node.media_type"
            },
            "blob_hash": {
              "$ref": "node.blob_hash"
            },
            "uri": {
              "$ref": "node.uri"
            },
            "path": {
              "$ref": "node.path"
            },
            "file_size": {
              "$ref": "node.file_size"
            },
            "file_hash": {
              "$ref": "node.file_hash"
            },
            "last_verified": {
              "$ref": "node.last_verified"
            }
          }
        },
        "supersede_edge": {
          "discriminator": "body_type = 'supersede_edge'",
          "fields": {
            "body_type": {
              "const": "supersede_edge"
            },
            "event_type": {
              "const": "supersede_edge"
            },
            "edge_id": {
              "type": "UUID v7 string",
              "description": "ID of an existing edge to supersede."
            },
            "source_node": {
              "type": "UUID v7 string",
              "description": "Must equal the existing edge source."
            },
            "target_node": {
              "type": "UUID v7 string",
              "description": "Must equal the existing edge target."
            },
            "title": {
              "type": "string | null"
            },
            "resource_type": {
              "$ref": "node.resource_type"
            },
            "media_type": {
              "$ref": "node.media_type"
            },
            "blob_hash": {
              "$ref": "node.blob_hash"
            },
            "uri": {
              "$ref": "node.uri"
            },
            "path": {
              "$ref": "node.path"
            },
            "file_size": {
              "$ref": "node.file_size"
            },
            "file_hash": {
              "$ref": "node.file_hash"
            },
            "last_verified": {
              "$ref": "node.last_verified"
            }
          }
        }
      }
    },
    "MetaEventBody": {
      "description": "Body of a meta-network event.  The meta-network encodes node/edge tagging as a graph of its own.  body_type discriminates the variant.",
      "body_types": {
        "tag": {
          "discriminator": "body_type = 'tag'",
          "event_types": [
            "create_node_tag",
            "create_edge_tag"
          ],
          "fields": {
            "body_type": {
              "const": "tag"
            },
            "event_type": {
              "enum": [
                "create_node_tag",
                "create_edge_tag"
              ]
            },
            "node_id": {
              "type": "UUID v7 string"
            },
            "name": {
              "type": "string"
            },
            "description": {
              "type": "string"
            }
          }
        },
        "representation": {
          "discriminator": "body_type = 'representation'",
          "event_types": [
            "create_node_representation",
            "create_edge_representation"
          ],
          "description": "A shadow node in the meta-network that stands for a base-network node or edge, allowing tags to be attached via meta-edges.",
          "fields": {
            "body_type": {
              "const": "representation"
            },
            "event_type": {
              "enum": [
                "create_node_representation",
                "create_edge_representation"
              ]
            },
            "node_id": {
              "type": "UUID v7 string"
            },
            "underlying_id": {
              "type": "UUID v7 string",
              "description": "ID of the base-network node or edge being represented."
            }
          }
        },
        "edge": {
          "discriminator": "body_type = 'edge'",
          "event_types": [
            "set_node_tag",
            "set_edge_tag"
          ],
          "description": "A directed edge in the meta-network from a tag node to a representation node, meaning: 'this tag is applied to that item'.",
          "fields": {
            "body_type": {
              "const": "edge"
            },
            "event_type": {
              "enum": [
                "set_node_tag",
                "set_edge_tag"
              ]
            },
            "edge_id": {
              "type": "UUID v7 string"
            },
            "source_node": {
              "type": "UUID v7 string",
              "description": "node_id of the tag."
            },
            "target_node": {
              "type": "UUID v7 string",
              "description": "node_id of the representation."
            }
          }
        }
      }
    },
    "EventModel": {
      "description": "Top-level structure of every NDJSON line in the base event log.",
      "fields": {
        "header": {
          "$ref": "EventHeader"
        },
        "body": {
          "$ref": "EventBody"
        },
        "signature": {
          "type": "string | null",
          "description": "Hex-encoded Ed25519 signature produced by signing the SHA-256 digest of the body serialised as compact JSON with keys sorted alphabetically."
        }
      }
    },
    "MetaEventModel": {
      "description": "Top-level structure of every NDJSON line in the meta event log.",
      "fields": {
        "header": {
          "$ref": "EventHeader"
        },
        "body": {
          "$ref": "MetaEventBody"
        },
        "signature": {
          "$ref": "EventModel.signature"
        }
      }
    }
  }
}
```

See the examples section for complete sample archives.
