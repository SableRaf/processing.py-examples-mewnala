#!/usr/bin/env python3
"""Mechanically convert Processing Python Mode examples to mewnala.

This is intentionally a first-pass converter, not a compatibility layer.

All identifiers are renamed from lowerCamelCase to snake_case, and a
``from mewnala import *`` statement is inserted after any leading module
docstring. The ``sketch.properties`` files are ignored, and all other files
are copied verbatim.

Every main sketch receives a ``run()`` call, including static sketches
where that may not be appropriate.

Some sketches may require additional manual edits to run correctly, and some
may not run at all, especially if they rely on parts of the API that mewnala
does not implement yet.
"""

from __future__ import annotations

import argparse
import io
import keyword
import re
import shutil
import sys
import tokenize
from collections import defaultdict
from pathlib import Path

DEFAULT_SRC = "examples-python-mode" # The default source directory for Processing.py examples.
DEFAULT_DST = "mewnala-examples" # The default destination directory for the converted mewnala examples.

NOTE = (
    "# AUTO-CONVERTED from Processing Python Mode to mewnala by "
    "convert_to_mewnala.py.\n"
    "# This is a first-pass mechanical conversion and has NOT been tested — "
    "review and run before relying on it.\n"
)

IMPORT = "from mewnala import *"
PYPROJECT = """\
[project]
name = "mewnala-examples"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "mewnala>=0.0.7",
]
"""
LOWER_CAMEL = re.compile(r"\b[a-z][A-Za-z0-9_]*[A-Z][A-Za-z0-9_]*\b")
SPECIAL_STATES = {
    "mousePressed": "mouse_is_pressed",
    "keyPressed": "key_is_pressed",
}
IGNORED_PREVIOUS_TOKEN_TYPES = {
    tokenize.COMMENT,
    tokenize.DEDENT,
    tokenize.ENCODING,
    tokenize.INDENT,
    tokenize.NEWLINE,
    tokenize.NL,
}


def snake_case(name: str) -> str:
    """Convert one lowerCamelCase identifier to the plan's snake_case form."""
    return re.sub(r"([A-Z])", r"_\1", name).lower()


def is_lower_camel(name: str) -> bool:
    return (
        bool(name)
        and name[0].islower()
        and any(character.isupper() for character in name)
        and not keyword.iskeyword(name)
    )


def token_conversion(source: str) -> tuple[str, int | None]:
    """Rename identifiers and return the module-docstring ending row, if any."""
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    first_significant = next(
        (token for token in tokens if token.type not in IGNORED_PREVIOUS_TOKEN_TYPES),
        None,
    )
    docstring_end_row = (
        first_significant.end[0]
        if first_significant is not None and first_significant.type == tokenize.STRING
        else None
    )

    edits: dict[int, list[tuple[int, int, str]]] = defaultdict(list)
    previous_significant: tokenize.TokenInfo | None = None
    for token in tokens:
        if token.type == tokenize.NAME and is_lower_camel(token.string):
            if token.string in SPECIAL_STATES and not (
                previous_significant is not None
                and previous_significant.type == tokenize.NAME
                and previous_significant.string == "def"
            ):
                replacement = SPECIAL_STATES[token.string]
            else:
                replacement = snake_case(token.string)
            edits[token.start[0]].append((token.start[1], token.end[1], replacement))

        if token.type not in IGNORED_PREVIOUS_TOKEN_TYPES and token.type != tokenize.ENDMARKER:
            previous_significant = token

    lines = source.splitlines(keepends=True)
    for row, row_edits in edits.items():
        for start, end, replacement in sorted(row_edits, reverse=True):
            lines[row - 1] = lines[row - 1][:start] + replacement + lines[row - 1][end:]
    return "".join(lines), docstring_end_row


def regex_conversion(source: str) -> str:
    """Best-effort whole-text fallback for files tokenize cannot consume."""
    def replace(match: re.Match[str]) -> str:
        name = match.group(0)
        if keyword.iskeyword(name):
            return name
        if name in SPECIAL_STATES:
            prefix = source[: match.start()]
            if not re.search(r"\bdef\s*$", prefix):
                return SPECIAL_STATES[name]
        return snake_case(name)

    return LOWER_CAMEL.sub(replace, source)


def fallback_docstring_end(source: str) -> int | None:
    """Locate a simple leading triple-quoted docstring after tokenization fails."""
    match = re.match(
        r"\A(?:[ \t]*(?:\#[^\r\n]*)?(?:\r?\n|\r))*"
        r"(?:[rubfRUBF]{0,2})?(?P<quote>'''|\"\"\")",
        source,
    )
    if match is None:
        return None
    quote = match.group("quote")
    closing = source.find(quote, match.end())
    if closing == -1:
        return None
    return source.count("\n", 0, closing + len(quote)) + 1


def newline_for(source: str) -> str:
    match = re.search(r"\r\n|\r|\n", source)
    return match.group(0) if match else "\n"


def insert_import(source: str, docstring_end_row: int | None, newline: str) -> str:
    import_line = IMPORT + newline
    if docstring_end_row is None:
        return import_line + source

    lines = source.splitlines(keepends=True)
    insertion_index = min(docstring_end_row, len(lines))
    if insertion_index and not lines[insertion_index - 1].endswith(("\n", "\r")):
        lines[insertion_index - 1] += newline
    lines.insert(insertion_index, import_line)
    return "".join(lines)


def read_python(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
    except SyntaxError:
        encoding = "utf-8"
    try:
        return raw.decode(encoding), encoding
    except (LookupError, UnicodeDecodeError):
        return raw.decode("utf-8", errors="replace"), "utf-8"


def convert_python(path: Path, destination: Path, is_sketch: bool) -> bool:
    """Convert one Python source file. Return whether regex fallback was used."""
    source, encoding = read_python(path)
    newline = newline_for(source)
    used_fallback = False
    try:
        converted, docstring_end_row = token_conversion(source)
    except (IndentationError, SyntaxError, tokenize.TokenError):
        converted = regex_conversion(source)
        docstring_end_row = fallback_docstring_end(source)
        used_fallback = True

    converted = insert_import(converted, docstring_end_row, newline)
    converted = NOTE.replace("\n", newline) + converted
    if is_sketch:
        if converted and not converted.endswith(("\n", "\r")):
            converted += newline
        converted += "run()" + newline

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(converted.encode(encoding))
    return used_fallback


def write_pyproject(destination_root: Path) -> None:
    """Write a project file at the tree root so ``uv run`` can find mewnala.

    uv discovers a project by walking up from the script it is asked to run
    until it finds a ``pyproject.toml``. A single file at the destination root
    therefore lets ``uv run mewnala-examples/.../Sketch.py`` resolve the
    ``mewnala`` dependency for every example beneath it.
    """
    destination_root.mkdir(parents=True, exist_ok=True)
    (destination_root / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")


def convert_tree(source_root: Path, destination_root: Path) -> dict[str, object]:
    counts: dict[str, object] = {
        "sketches": 0,
        "helpers": 0,
        "assets": 0,
        "properties": 0,
        "fallbacks": [],
    }
    write_pyproject(destination_root)
    for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
        relative = source.relative_to(source_root)
        if source.name == "sketch.properties":
            counts["properties"] += 1  # type: ignore[operator]
            continue

        if source.suffix == ".pyde":
            destination = (destination_root / relative).with_suffix(".py")
            fallback = convert_python(source, destination, is_sketch=True)
            counts["sketches"] += 1  # type: ignore[operator]
        elif source.suffix == ".py":
            destination = destination_root / relative
            fallback = convert_python(source, destination, is_sketch=False)
            counts["helpers"] += 1  # type: ignore[operator]
        else:
            destination = destination_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            counts["assets"] += 1  # type: ignore[operator]
            continue

        if fallback:
            counts["fallbacks"].append(relative)  # type: ignore[union-attr]
            print(f"warning: regex fallback used for {relative}", file=sys.stderr)
    return counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mechanically convert Processing Python Mode examples to mewnala."
    )
    parser.add_argument("--src", type=Path, default=Path(DEFAULT_SRC))
    parser.add_argument("--dst", type=Path, default=Path(DEFAULT_DST))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.src.resolve()
    destination_root = args.dst.resolve()
    if not source_root.is_dir():
        print(f"error: source directory does not exist: {source_root}", file=sys.stderr)
        return 2
    if destination_root == source_root or source_root in destination_root.parents:
        print("error: destination must not be inside the source tree", file=sys.stderr)
        return 2

    counts = convert_tree(source_root, destination_root)
    print(
        "Converted "
        f"{counts['sketches']} sketches and {counts['helpers']} helpers; "
        f"copied {counts['assets']} assets; "
        f"skipped {counts['properties']} sketch.properties files."
    )
    fallbacks = counts["fallbacks"]
    if fallbacks:
        print("Files converted with the regex fallback:")
        for path in fallbacks:  # type: ignore[union-attr]
            print(f"  {path}")
    else:
        print("Files converted with the regex fallback: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
