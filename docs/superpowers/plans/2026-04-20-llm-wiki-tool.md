# LLM Wiki Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a GitHub-ready, installable `llm-wiki` Python tool that creates and checks LLM-maintained wiki workspaces.

**Architecture:** The repository is both a template and a Python package. Runtime code lives in `llm_wiki/cli.py`, static workspace seed files live in `templates/default/`, and tests exercise CLI behavior through subprocess-free direct function calls where practical.

**Tech Stack:** Python 3.10+, standard library runtime, `pytest` for tests, `pyproject.toml` for packaging, Markdown for docs and templates.

---

## File Structure

- `pyproject.toml`: package metadata, console script entry point, pytest configuration.
- `README.md`: installation and usage guide for GitHub, local development, CLI, and LLM-agent workflow.
- `AGENTS.md`: root contributor/agent guidance for maintaining this tool repository.
- `docs/llm-wiki-concept.md`: stable copy of the original concept from `llm-wiki.md`.
- `llm_wiki/__init__.py`: package version export.
- `llm_wiki/cli.py`: argparse CLI, template copy logic, workspace checks, log parser, index parser.
- `templates/default/AGENTS.md`: agent operating schema copied into initialized workspaces.
- `templates/default/raw/.gitkeep`: preserves empty raw source directory.
- `templates/default/wiki/index.md`: initial wiki catalog.
- `templates/default/wiki/log.md`: initial chronological log.
- `templates/default/wiki/overview.md`: initial wiki overview.
- `examples/tiny-research/README.md`: tiny example showing intended workspace shape.
- `tests/test_cli.py`: pytest coverage for CLI commands and parsers.

### Task 1: Package Skeleton and CLI Test Harness

**Files:**
- Create: `pyproject.toml`
- Create: `llm_wiki/__init__.py`
- Create: `llm_wiki/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests for missing CLI package**

Create `tests/test_cli.py` with:

```python
from pathlib import Path

from llm_wiki.cli import main


def run_cli(*args: str) -> int:
    return main(list(args))


def test_cli_help_returns_success(capsys):
    exit_code = run_cli("--help")

    assert exit_code == 0
    assert "llm-wiki" in capsys.readouterr().out
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
pytest tests/test_cli.py::test_cli_help_returns_success -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'llm_wiki'`.

- [ ] **Step 3: Add minimal package metadata and CLI**

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "llm-wiki"
version = "0.1.0"
description = "A local template and CLI for LLM-maintained markdown wikis."
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8"]

[project.scripts]
llm-wiki = "llm_wiki.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Create `llm_wiki/__init__.py`:

```python
__version__ = "0.1.0"
```

Create `llm_wiki/cli.py`:

```python
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-wiki",
        description="Create and inspect local LLM-maintained wiki workspaces.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the test to verify it passes**

Run:

```bash
pytest tests/test_cli.py::test_cli_help_returns_success -v
```

Expected: PASS.

### Task 2: Template Workspace and `init`

**Files:**
- Create: `templates/default/AGENTS.md`
- Create: `templates/default/raw/.gitkeep`
- Create: `templates/default/wiki/index.md`
- Create: `templates/default/wiki/log.md`
- Create: `templates/default/wiki/overview.md`
- Modify: `llm_wiki/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests for `init`**

Append to `tests/test_cli.py`:

```python
def test_init_creates_workspace(tmp_path):
    target = tmp_path / "my-wiki"

    exit_code = run_cli("init", str(target))

    assert exit_code == 0
    assert (target / "AGENTS.md").is_file()
    assert (target / "raw").is_dir()
    assert (target / "wiki" / "index.md").is_file()
    assert (target / "wiki" / "log.md").is_file()
    assert (target / "wiki" / "overview.md").is_file()


def test_init_refuses_non_empty_directory(tmp_path, capsys):
    target = tmp_path / "existing"
    target.mkdir()
    (target / "note.txt").write_text("keep me", encoding="utf-8")

    exit_code = run_cli("init", str(target))

    assert exit_code == 1
    assert "refusing to initialize non-empty directory" in capsys.readouterr().err
    assert (target / "note.txt").read_text(encoding="utf-8") == "keep me"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
pytest tests/test_cli.py::test_init_creates_workspace tests/test_cli.py::test_init_refuses_non_empty_directory -v
```

Expected: FAIL because `init` is not defined.

- [ ] **Step 3: Create template files**

Create `templates/default/AGENTS.md`:

```markdown
# LLM Wiki Operating Schema

You maintain this workspace as a persistent, compounding markdown wiki.

## Layers

- `raw/` contains immutable source materials supplied by the user. Read from it, do not edit it.
- `wiki/` contains LLM-maintained markdown pages. You may create and update these files.
- `wiki/index.md` is the content catalog. Read it first when answering questions.
- `wiki/log.md` is the append-only activity record.
- `wiki/overview.md` is the entry point for the current synthesis.

## Ingest Workflow

When the user asks you to ingest a source:

1. Read the source from `raw/`.
2. Summarize the source's key claims, evidence, entities, and concepts.
3. Create or update relevant pages in `wiki/`.
4. Add cross-links between related wiki pages.
5. Update `wiki/index.md`.
6. Append an entry to `wiki/log.md` using `## [YYYY-MM-DD] ingest | Source Title`.

## Query Workflow

When the user asks a question:

1. Read `wiki/index.md`.
2. Open the most relevant wiki pages.
3. Answer from the wiki first, citing page links and source references when available.
4. If the answer creates reusable analysis, ask whether to file it back into `wiki/`.

## Lint Workflow

When asked to lint the wiki, check for contradictions, stale claims, orphan pages, missing backlinks, important concepts without pages, and source claims that are not reflected in the synthesis.

## Conventions

- Use markdown links for files and Obsidian-style `[[Page Name]]` links for wiki concepts.
- Keep source references close to claims.
- Do not silently delete useful prior synthesis. Mark superseded claims and explain why.
- Keep `wiki/log.md` append-only.
```

Create `templates/default/wiki/index.md`:

```markdown
# Wiki Index

## Overview

- [Overview](overview.md) - Current synthesis and orientation for this wiki.
```

Create `templates/default/wiki/log.md`:

```markdown
# Wiki Log

## [2026-04-20] init | Workspace created

Initialized the LLM Wiki workspace.
```

Create `templates/default/wiki/overview.md`:

```markdown
# Overview

This wiki has been initialized and is ready for source ingestion.
```

Create empty file `templates/default/raw/.gitkeep`.

- [ ] **Step 4: Implement `init`**

Replace `llm_wiki/cli.py` with:

```python
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
DEFAULT_TEMPLATE = REPO_ROOT / "templates" / "default"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-wiki",
        description="Create and inspect local LLM-maintained wiki workspaces.",
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Create a new wiki workspace.")
    init_parser.add_argument("path", help="Target directory for the workspace.")

    return parser


def init_workspace(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"refusing to initialize non-empty directory: {path}")
    path.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DEFAULT_TEMPLATE, path, dirs_exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            init_workspace(Path(args.path))
            return 0
        parser.print_help()
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run the tests to verify they pass**

Run:

```bash
pytest tests/test_cli.py::test_init_creates_workspace tests/test_cli.py::test_init_refuses_non_empty_directory -v
```

Expected: PASS.

### Task 3: `doctor` Workspace Checks

**Files:**
- Modify: `llm_wiki/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests for `doctor`**

Append to `tests/test_cli.py`:

```python
def test_doctor_succeeds_for_fresh_workspace(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0

    exit_code = run_cli("doctor", str(target))

    assert exit_code == 0
    assert "workspace ok" in capsys.readouterr().out


def test_doctor_fails_when_required_file_missing(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0
    (target / "wiki" / "index.md").unlink()

    exit_code = run_cli("doctor", str(target))

    assert exit_code == 1
    assert "missing: wiki/index.md" in capsys.readouterr().err
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
pytest tests/test_cli.py::test_doctor_succeeds_for_fresh_workspace tests/test_cli.py::test_doctor_fails_when_required_file_missing -v
```

Expected: FAIL because `doctor` is not defined.

- [ ] **Step 3: Implement `doctor`**

Update `llm_wiki/cli.py` to add:

```python
REQUIRED_PATHS = (
    "AGENTS.md",
    "raw",
    "wiki",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/overview.md",
)


def missing_required_paths(path: Path) -> list[str]:
    return [relative for relative in REQUIRED_PATHS if not (path / relative).exists()]
```

Add the parser:

```python
doctor_parser = subparsers.add_parser("doctor", help="Check workspace structure.")
doctor_parser.add_argument("path", help="Workspace directory to check.")
```

Add command handling before the help fallback:

```python
if args.command == "doctor":
    missing = missing_required_paths(Path(args.path))
    if missing:
        for relative in missing:
            print(f"missing: {relative}", file=sys.stderr)
        return 1
    print("workspace ok")
    return 0
```

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
pytest tests/test_cli.py::test_doctor_succeeds_for_fresh_workspace tests/test_cli.py::test_doctor_fails_when_required_file_missing -v
```

Expected: PASS.

### Task 4: `log` and `index` Commands

**Files:**
- Modify: `llm_wiki/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests for log and index parsers**

Append to `tests/test_cli.py`:

```python
def test_log_prints_recent_entries(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0
    (target / "wiki" / "log.md").write_text(
        "\n".join(
            [
                "# Wiki Log",
                "",
                "## [2026-04-18] ingest | First Source",
                "",
                "## [2026-04-19] query | Comparison",
                "",
                "## [2026-04-20] lint | Weekly check",
                "",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run_cli("log", str(target), "--limit", "2")

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == [
        "2026-04-19 query | Comparison",
        "2026-04-20 lint | Weekly check",
    ]


def test_index_prints_links_and_summaries(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0
    (target / "wiki" / "index.md").write_text(
        "\n".join(
            [
                "# Wiki Index",
                "",
                "- [Overview](overview.md) - Current synthesis.",
                "- [Entity A](entities/entity-a.md) - Important entity.",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run_cli("index", str(target))

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == [
        "Overview | overview.md | Current synthesis.",
        "Entity A | entities/entity-a.md | Important entity.",
    ]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
pytest tests/test_cli.py::test_log_prints_recent_entries tests/test_cli.py::test_index_prints_links_and_summaries -v
```

Expected: FAIL because `log` and `index` are not defined.

- [ ] **Step 3: Implement parsers and commands**

Update `llm_wiki/cli.py` imports:

```python
import re
```

Add patterns and parser functions:

```python
LOG_HEADING_RE = re.compile(r"^## \[(?P<date>\d{4}-\d{2}-\d{2})\] (?P<kind>[^|]+) \| (?P<title>.+)$")
INDEX_ENTRY_RE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<path>[^)]+)\) - (?P<summary>.+)$")


def parse_log_entries(log_path: Path) -> list[str]:
    entries: list[str] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        match = LOG_HEADING_RE.match(line)
        if match:
            entries.append(
                f"{match.group('date')} {match.group('kind').strip()} | {match.group('title').strip()}"
            )
    return entries


def parse_index_entries(index_path: Path) -> list[str]:
    entries: list[str] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = INDEX_ENTRY_RE.match(line)
        if match:
            entries.append(
                f"{match.group('title').strip()} | {match.group('path').strip()} | {match.group('summary').strip()}"
            )
    return entries
```

Add parsers:

```python
log_parser = subparsers.add_parser("log", help="Print recent wiki log entries.")
log_parser.add_argument("path", help="Workspace directory.")
log_parser.add_argument("--limit", type=int, default=5, help="Number of recent entries to print.")

index_parser = subparsers.add_parser("index", help="Print wiki index entries.")
index_parser.add_argument("path", help="Workspace directory.")
```

Add command handling:

```python
if args.command == "log":
    entries = parse_log_entries(Path(args.path) / "wiki" / "log.md")
    for entry in entries[-args.limit :]:
        print(entry)
    return 0

if args.command == "index":
    entries = parse_index_entries(Path(args.path) / "wiki" / "index.md")
    for entry in entries:
        print(entry)
    return 0
```

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
pytest tests/test_cli.py::test_log_prints_recent_entries tests/test_cli.py::test_index_prints_links_and_summaries -v
```

Expected: PASS.

### Task 5: Docs, Example, and Full Verification

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `docs/llm-wiki-concept.md`
- Create: `examples/tiny-research/README.md`
- Modify: `llm_wiki/cli.py` if full-suite failures expose integration issues.

- [ ] **Step 1: Write repository docs**

Create `README.md`:

```markdown
# LLM Wiki

LLM Wiki is a local template and CLI for building personal knowledge bases that compound over time. Instead of asking an LLM to retrieve raw chunks from documents on every question, you ask the LLM to maintain a persistent markdown wiki between you and the raw sources.

## Install

From a GitHub checkout:

```bash
pip install -e ".[dev]"
```

From a GitHub URL:

```bash
pipx install "git+https://github.com/YOUR-USER/llm-wiki.git"
```

## Create a Workspace

```bash
llm-wiki init my-wiki
cd my-wiki
```

The workspace contains:

- `raw/` for immutable source files.
- `wiki/` for LLM-maintained markdown pages.
- `wiki/index.md` for the content catalog.
- `wiki/log.md` for chronological activity.
- `AGENTS.md` for LLM-agent operating instructions.

## Check a Workspace

```bash
llm-wiki doctor my-wiki
llm-wiki index my-wiki
llm-wiki log my-wiki
```

## Work With an LLM Agent

Open the workspace with Codex, Claude Code, OpenCode, or another coding agent. Ask the agent to follow `AGENTS.md`, ingest files from `raw/`, update pages in `wiki/`, maintain `wiki/index.md`, and append parseable entries to `wiki/log.md`.

Obsidian works well as the reading and browsing interface because the wiki is just markdown.
```

Create root `AGENTS.md`:

```markdown
# Repository Instructions

This repository builds the `llm-wiki` CLI and template.

- Keep runtime code dependency-free unless a new dependency is clearly justified.
- Use `pytest` for tests.
- Keep template files generic and domain-neutral.
- Do not put user-specific knowledge into `templates/default/`.
- Preserve `llm-wiki.md` as the original idea note.
```

Create `docs/llm-wiki-concept.md` by copying the current contents of `llm-wiki.md`.

Create `examples/tiny-research/README.md`:

```markdown
# Tiny Research Example

This example shows the intended workflow:

1. Put source files in `raw/`.
2. Ask an LLM agent to ingest one source.
3. Review the generated pages in `wiki/`.
4. Ask follow-up questions and file useful answers back into the wiki.

Run this first:

```bash
llm-wiki init tiny-research
llm-wiki doctor tiny-research
```
```

- [ ] **Step 2: Run full test suite**

Run:

```bash
pytest
```

Expected: PASS.

- [ ] **Step 3: Verify editable install entry point**

Run:

```bash
python -m pip install -e ".[dev]"
llm-wiki --help
```

Expected: installation succeeds and `llm-wiki --help` prints command help.

- [ ] **Step 4: Verify generated workspace manually**

Run:

```bash
llm-wiki init /tmp/llm-wiki-smoke
llm-wiki doctor /tmp/llm-wiki-smoke
llm-wiki index /tmp/llm-wiki-smoke
llm-wiki log /tmp/llm-wiki-smoke
```

Expected: doctor prints `workspace ok`; index prints the overview entry; log prints the init entry.

## Self-Review

- Spec coverage: The plan covers package structure, template workspace, agent schema, CLI commands, documentation, pytest tests, and acceptance criteria.
- Placeholder scan: No task relies on placeholder implementation text; all code edits include concrete content.
- Type consistency: CLI functions consistently use `Path`, `list[str]`, integer exit codes, and parser command names matching the spec.
