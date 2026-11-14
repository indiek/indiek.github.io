#!/usr/bin/env bash
# Regenerate docs/sdk.md, docs/cli.md and docs/format.md from a RELEASED version
# of the indiek package, then check the site against that same version.
#
#   scripts/sync_docs_release.sh [TAG] [PACKAGE_REPO]
#
# TAG defaults to the newest X.Y.Z tag of PACKAGE_REPO (default ../public_archive).
# The tag is extracted with `git archive` (read-only) into a temporary folder:
# the package repository's branch and working copy are never touched, so
# unreleased work there never reaches the site.
set -euo pipefail

cd "$(dirname "$0")/.."
repo="${2:-../public_archive}"
tag="${1:-$(git -C "$repo" tag --list | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -t. -k1,1n -k2,2n -k3,3n | tail -n 1)}"
if [ -z "$tag" ]; then
    echo "No X.Y.Z tag found in $repo" >&2
    exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git -C "$repo" archive "$tag" | tar -x -C "$tmp"

echo "Syncing the reference pages from indiek $tag"
uv run --quiet --project "$tmp" python scripts/sync_docs.py "$tmp"
uv run --quiet --project "$tmp" python scripts/check_site.py
