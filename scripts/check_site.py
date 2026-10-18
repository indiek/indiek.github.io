"""Check the indiek.org sources without a Jekyll installation.

    uv run --project ../public_archive python scripts/check_site.py

Run from the site root.  Checks, for ``index.md`` and every ``docs/*.md``:

1. every internal link (``](/…)``, ``href="/…"``, ``](#…)``) points to an
   existing page and, with ``#anchor``, to an existing heading id;
2. no ``<word`` outside code would be swallowed as an HTML tag (docs pages);
3. no list or table directly follows a paragraph line (kramdown then renders
   it as plain text);
4. the Python examples of ``docs/intro.md`` and ``docs/examples.md`` run, in
   order, in a temporary folder.

Exits 1 on any problem.
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_docs import gfm_id, headings  # noqa: E402

SITE = Path(__file__).resolve().parents[1]
EXECUTED = ["docs/intro.md", "docs/examples.md"]
LIST_ITEM = re.compile(r"^(\s*)([-*+]|\d+\.) ")
HTML_ALLOWED = {"br", "code", "div", "span", "strong", "em", "a", "section", "h1", "h2", "h3", "p"}

problems: list[str] = []


def pages() -> dict[str, Path]:
    found = {"/": SITE / "index.md"}
    for path in sorted((SITE / "docs").glob("*.md")):
        found[f"/docs/{path.stem}/"] = path
    return found


def body(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0] == "---":
        lines = lines[lines.index("---", 1) + 1 :]
    return lines


def prose(lines: list[str]) -> list[tuple[int, str]]:
    """(line number, text) outside code fences, with inline code removed."""
    out, fenced = [], False
    for number, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append((number, re.sub(r"`[^`]*`", "", line)))
    return out


def anchors(lines: list[str]) -> set[str]:
    ids: set[str] = set()
    for heading in headings(lines):
        base = candidate = gfm_id(re.sub(r"\[([^]]*)\]\([^)]*\)", r"\1", heading.title))
        n = 0
        while candidate in ids:
            n += 1
            candidate = f"{base}-{n}"
        ids.add(candidate)
    return ids


def check_links(site_pages: dict[str, Path]) -> None:
    ids = {url: anchors(body(path)) for url, path in site_pages.items()}
    for url, path in site_pages.items():
        for number, text in prose(body(path)):
            targets = re.findall(r"\]\(([/#][^)\s]*)\)", text)
            targets += re.findall(r'href="([/#][^"]*)"', text)
            for target in targets:
                page, _, anchor = target.partition("#")
                page = page or url
                if page.startswith("/assets/"):
                    continue
                if page not in site_pages:
                    problems.append(f"{path.name}:{number}: no page for link {target}")
                elif anchor and anchor not in ids[page]:
                    problems.append(f"{path.name}:{number}: no heading #{anchor} in {page}")


def check_markup(site_pages: dict[str, Path]) -> None:
    for url, path in site_pages.items():
        lines = body(path)
        for number, text in prose(lines):
            if url != "/":
                for tag in re.findall(r"<(/?)([A-Za-z][\w-]*)", text):
                    if tag[1].lower() not in HTML_ALLOWED:
                        problems.append(f"{path.name}:{number}: stray <{tag[1]} outside code")
        fenced = False
        for index in range(1, len(lines)):
            line, previous = lines[index], lines[index - 1]
            if line.lstrip().startswith("```"):
                fenced = not fenced
            if fenced or not previous.strip() or previous.lstrip().startswith("```"):
                continue
            starts_block = bool(LIST_ITEM.match(line)) or line.startswith("|")
            previous_is_block = (
                bool(LIST_ITEM.match(previous))
                or previous.startswith(("|", "#", "<", " ", "\t"))
            )
            if starts_block and not previous_is_block and not line.startswith(" "):
                problems.append(f"{path.name}:{index + 1}: list or table glued to a paragraph")


def run_examples() -> None:
    for relative in EXECUTED:
        text = "\n".join(body(SITE / relative))
        blocks = re.findall(r"^```python\n(.*?)^```$", text, re.MULTILINE | re.DOTALL)
        namespace: dict[str, object] = {"__name__": "site_example"}
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.environ["IK_CACHE_DIR"] = str(Path(tmp) / ".cache")
            os.chdir(tmp)
            try:
                for number, block in enumerate(blocks, start=1):
                    try:
                        exec(compile(block, f"{relative} block {number}", "exec"), namespace)
                    except Exception as error:  # noqa: BLE001 - reported below
                        problems.append(f"{relative}: python block {number} failed: {error!r}")
                        break
            finally:
                os.chdir(cwd)
        print(f"{relative}: {len(blocks)} python block(s) executed")


def main() -> None:
    site_pages = pages()
    check_links(site_pages)
    check_markup(site_pages)
    run_examples()
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print(f"OK: {len(site_pages)} pages checked")


if __name__ == "__main__":
    main()
