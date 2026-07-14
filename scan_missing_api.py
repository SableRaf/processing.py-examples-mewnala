#!/usr/bin/env python3
"""Statically find names used by examples but not exported by an API module.

The example files are parsed with :mod:`ast`; they are never imported or run.
By default, names are compared with the public exports of ``mewnala``.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import importlib
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass
class Scope:
    """Names bound in one lexical scope."""

    node: ast.AST
    bound: set[str]
    parent: Scope | None


@dataclass
class Finding:
    """Occurrences of one unresolved name."""

    references: int = 0
    call_references: int = 0
    examples: set[str] = field(default_factory=set)
    source_files: set[str] = field(default_factory=set)
    locations: list[dict[str, Any]] = field(default_factory=list)


class BindingCollector(ast.NodeVisitor):
    """Collect bindings belonging directly to a scope."""

    def __init__(self, arguments: ast.arguments | None = None) -> None:
        self.bound: set[str] = set()
        self.globals: set[str] = set()
        self.nonlocals: set[str] = set()
        if arguments is not None:
            args = (
                list(arguments.posonlyargs)
                + list(arguments.args)
                + list(arguments.kwonlyargs)
            )
            self.bound.update(arg.arg for arg in args)
            if arguments.vararg:
                self.bound.add(arguments.vararg.arg)
            if arguments.kwarg:
                self.bound.add(arguments.kwarg.arg)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self.bound.add(node.id)

    def visit_Import(self, node: ast.Import) -> None:
        self.bound.update(alias.asname or alias.name.split(".")[0] for alias in node.names)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.bound.update(
            alias.asname or alias.name for alias in node.names if alias.name != "*"
        )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.bound.add(node.name)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.bound.add(node.name)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        return

    def visit_Global(self, node: ast.Global) -> None:
        self.globals.update(node.names)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        self.nonlocals.update(node.names)


def collect_scope_bindings(
    node: ast.AST, arguments: ast.arguments | None = None
) -> set[str]:
    collector = BindingCollector(arguments)
    statements: Iterable[ast.AST]
    if isinstance(node, ast.Lambda):
        statements = (node.body,)
    else:
        statements = getattr(node, "body", ())
    for statement in statements:
        collector.visit(statement)
    return collector.bound - collector.globals - collector.nonlocals


def top_level_exports(tree: ast.Module) -> set[str]:
    """Return public names a local ``from module import *`` would provide."""
    return {name for name in collect_scope_bindings(tree) if not name.startswith("_")}


class UnresolvedNameVisitor(ast.NodeVisitor):
    def __init__(
        self,
        tree: ast.Module,
        known_names: set[str],
        local_star_exports: dict[str, set[str]],
    ) -> None:
        module_bindings = collect_scope_bindings(tree)
        # Processing sketches commonly initialize module state inside setup():
        # ``global img; img = load_image(...)``. That assignment binds the name
        # at module scope even though it is nested in the AST.
        declared_globals = {
            name
            for node in ast.walk(tree)
            if isinstance(node, ast.Global)
            for name in node.names
        }
        stored_names = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
        }
        module_bindings.update(declared_globals & stored_names)
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module in local_star_exports:
                if any(alias.name == "*" for alias in node.names):
                    module_bindings.update(local_star_exports[node.module])
        self.scope = Scope(tree, module_bindings, None)
        self.known_names = known_names
        self.unresolved: list[ast.Name] = []
        self.called_name_nodes = {
            id(node.func)
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }

    def _is_bound(self, name: str) -> bool:
        scope: Scope | None = self.scope
        while scope is not None:
            if name in scope.bound:
                return True
            scope = scope.parent
        return False

    def visit_Name(self, node: ast.Name) -> None:
        if (
            isinstance(node.ctx, ast.Load)
            and node.id not in self.known_names
            and not self._is_bound(node.id)
        ):
            self.unresolved.append(node)

    def _visit_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda
    ) -> None:
        # Defaults and annotations are evaluated in the enclosing scope.
        arguments = node.args
        for default in (*arguments.defaults, *arguments.kw_defaults):
            if default is not None:
                self.visit(default)
        for arg in (*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs):
            if arg.annotation:
                self.visit(arg.annotation)
        if arguments.vararg and arguments.vararg.annotation:
            self.visit(arguments.vararg.annotation)
        if arguments.kwarg and arguments.kwarg.annotation:
            self.visit(arguments.kwarg.annotation)

        old_scope = self.scope
        # A method does not close over its class namespace: an unqualified class
        # attribute in a method is still an unresolved global name.
        parent = old_scope.parent if isinstance(old_scope.node, ast.ClassDef) else old_scope
        self.scope = Scope(node, collect_scope_bindings(node, arguments), parent)
        if isinstance(node, ast.Lambda):
            self.visit(node.body)
        else:
            for statement in node.body:
                self.visit(statement)
        self.scope = old_scope

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            self.visit(decorator)
        if node.returns:
            self.visit(node.returns)
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self._visit_function(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for item in (*node.decorator_list, *node.bases, *node.keywords):
            self.visit(item.value if isinstance(item, ast.keyword) else item)
        parent = self.scope
        self.scope = Scope(node, collect_scope_bindings(node), parent)
        for statement in node.body:
            self.visit(statement)
        self.scope = parent


def find_main_sketches(examples_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in examples_dir.rglob("*.py")
        if "__pycache__" not in path.parts and path.stem == path.parent.name
    )


def load_api_exports(module_name: str) -> set[str]:
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        raise RuntimeError(f"could not import API module {module_name!r}: {exc}") from exc
    exports = getattr(module, "__all__", None)
    if exports is None:
        exports = (name for name in dir(module) if not name.startswith("_"))
    return set(exports)


REFERENCE_BASE_URL = "https://processing.org/reference"
SPECIAL_REFERENCE_NAMES = {
    "begin_p_g_l": "beginPGL",
    "end_p_g_l": "endPGL",
    "key_is_pressed": "keyPressed",
    "mouse_is_pressed": "mousePressed",
}


def processing_reference_name(name: str) -> str:
    """Undo the converter's snake_case renaming for a reference URL."""
    if name in SPECIAL_REFERENCE_NAMES:
        return SPECIAL_REFERENCE_NAMES[name]
    if "_" not in name or name.isupper():
        return name
    first, *rest = name.split("_")
    return first + "".join(
        part.upper() if len(part) == 1 else part[0].upper() + part[1:]
        for part in rest
        if part
    )


def processing_reference_url(name: str, is_called: bool) -> str:
    """Build the canonical Processing reference URL for an unresolved name."""
    reference_name = processing_reference_name(name)
    # Processing adds an underscore to function pages. Classes and constants
    # may be callable in Python but retain pages such as PVector.html.
    suffix = "_" if is_called and reference_name[:1].islower() else ""
    return f"{REFERENCE_BASE_URL}/{reference_name}{suffix}.html"


def scan(examples_dir: Path, module_name: str, ignored: set[str]) -> dict[str, Any]:
    api_exports = load_api_exports(module_name)
    known_names = set(dir(builtins)) | api_exports | {"__file__", "__name__"} | ignored
    main_sketches = find_main_sketches(examples_dir)
    findings: dict[str, Finding] = defaultdict(Finding)
    syntax_errors: list[dict[str, Any]] = []
    source_count = 0

    for main_sketch in main_sketches:
        example_dir = main_sketch.parent
        example_name = str(main_sketch.relative_to(examples_dir))
        parsed: dict[Path, ast.Module] = {}

        for source_path in sorted(example_dir.glob("*.py")):
            source_count += 1
            relative_source = str(source_path.relative_to(examples_dir))
            try:
                source = source_path.read_text(encoding="utf-8")
                parsed[source_path] = ast.parse(source, filename=relative_source)
            except (OSError, UnicodeError, SyntaxError) as exc:
                syntax_errors.append(
                    {
                        "example": example_name,
                        "path": relative_source,
                        "line": getattr(exc, "lineno", None),
                        "message": getattr(exc, "msg", str(exc)),
                    }
                )

        local_star_exports = {
            path.stem: top_level_exports(tree) for path, tree in parsed.items()
        }
        for source_path, tree in parsed.items():
            relative_source = str(source_path.relative_to(examples_dir))
            visitor = UnresolvedNameVisitor(tree, known_names, local_star_exports)
            visitor.visit(tree)
            for node in visitor.unresolved:
                finding = findings[node.id]
                finding.references += 1
                if id(node) in visitor.called_name_nodes:
                    finding.call_references += 1
                finding.examples.add(example_name)
                finding.source_files.add(relative_source)
                finding.locations.append(
                    {
                        "example": example_name,
                        "path": relative_source,
                        "line": node.lineno,
                        "column": node.col_offset + 1,
                    }
                )

    ranked = []
    for name, finding in findings.items():
        ranked.append(
            {
                "name": name,
                "examples_affected": len(finding.examples),
                "references": finding.references,
                "source_files_affected": len(finding.source_files),
                "reference_url": processing_reference_url(
                    name, finding.call_references > 0
                ),
                "locations": sorted(
                    finding.locations,
                    key=lambda item: (item["example"], item["path"], item["line"]),
                ),
            }
        )
    ranked.sort(
        key=lambda item: (
            -item["examples_affected"],
            -item["references"],
            item["name"].lower(),
        )
    )
    syntax_errors.sort(key=lambda item: (item["example"], item["path"]))

    return {
        "examples_directory": str(examples_dir),
        "api_module": module_name,
        "api_exports": len(api_exports),
        "examples_scanned": len(main_sketches),
        "source_files_scanned": source_count,
        "missing_names": ranked,
        "syntax_errors": syntax_errors,
    }


def render_text(report: dict[str, Any], top: int, show_locations: bool) -> str:
    findings = report["missing_names"]
    shown = findings[:top] if top else findings
    output = [
        f"Scanned {report['examples_scanned']} examples "
        f"({report['source_files_scanned']} Python files)",
        f"Compared against {report['api_exports']} exports from "
        f"{report['api_module']}",
        "",
        f"{'NAME':<28} {'EXAMPLES':>8} {'REFERENCES':>10} {'FILES':>7}",
        f"{'-' * 28} {'-' * 8} {'-' * 10} {'-' * 7}",
    ]
    for finding in shown:
        output.append(
            f"{finding['name']:<28} {finding['examples_affected']:>8} "
            f"{finding['references']:>10} {finding['source_files_affected']:>7}"
        )
        output.append(f"  Reference: {finding['reference_url']}")
        if show_locations:
            for location in finding["locations"]:
                output.append(
                    f"  {location['path']}:{location['line']}:{location['column']}"
                )
    if top and len(findings) > top:
        output.extend(("", f"Showing {top} of {len(findings)} missing names."))

    syntax_errors = report["syntax_errors"]
    output.extend(("", f"Syntax errors: {len(syntax_errors)}"))
    for error in syntax_errors:
        line = f":{error['line']}" if error["line"] is not None else ""
        output.append(f"  {error['path']}{line}: {error['message']}")
    return "\n".join(output)


def render_short_markdown(report: dict[str, Any], top: int) -> str:
    """Render a short Markdown prioritization report."""
    findings = report["missing_names"]
    shown = findings[:top] if top else findings
    output = [
        "# Missing Processing API references",
        "",
        "| Name | Examples affected | Reference |",
        "| --- | ---: | --- |",
    ]
    for finding in shown:
        output.append(
            f"| `{finding['name']}` | {finding['examples_affected']} | "
            f"[Processing reference]({finding['reference_url']}) |"
        )
    return "\n".join(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Find names used by examples but not exported by mewnala, without "
            "running any sketch."
        )
    )
    parser.add_argument(
        "examples_dir",
        nargs="?",
        default="mewnala-examples",
        type=Path,
        help="examples root (default: mewnala-examples)",
    )
    parser.add_argument(
        "--module",
        default="mewnala",
        help="API module whose exports are considered implemented (default: mewnala)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="show only the top N names in text output (default: all)",
    )
    parser.add_argument(
        "--locations",
        action="store_true",
        help="show every file and line in text output",
    )
    parser.add_argument(
        "--short",
        action="store_true",
        help=(
            "emit a short Markdown report with name, examples affected, and "
            "Processing reference link"
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit JSON instead of text (always includes all names and locations)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="write the report to this file instead of stdout",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="NAME",
        help="ignore an unresolved name; may be repeated",
    )
    args = parser.parse_args()

    if not args.examples_dir.is_dir():
        parser.error(f"examples directory not found: {args.examples_dir}")
    if args.top < 0:
        parser.error("--top must be zero or greater")

    try:
        report = scan(args.examples_dir, args.module, set(args.ignore))
    except RuntimeError as exc:
        parser.error(str(exc))

    rendered = (
        json.dumps(report, indent=2) + "\n"
        if args.json
        else (
            render_short_markdown(report, args.top)
            if args.short
            else render_text(report, args.top, args.locations)
        )
        + "\n"
    )
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Report saved to {args.output}")
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
