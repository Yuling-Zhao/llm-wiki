# LLM Wiki Tool Design

## Purpose

Turn the `llm-wiki.md` idea into a portable GitHub-ready project that can be installed or cloned on other PCs. The project should work both as a template for new LLM-maintained markdown wikis and as a small Python CLI that creates and checks wiki workspaces.

The CLI supports the filesystem tasks. The LLM-agent schema remains the core product: it tells Codex, Claude Code, OpenCode, and similar agents how to maintain the wiki.

## Product Shape

The repository will provide both:

- A template structure for raw sources, generated wiki pages, logs, and agent instructions.
- An installable Python package exposing a `llm-wiki` command.

The implementation should stay lightweight and dependency-minimal. Runtime behavior should use the Python standard library. Tests will use `pytest`.

## Repository Structure

```text
.
├── README.md
├── pyproject.toml
├── AGENTS.md
├── llm-wiki.md
├── llm_wiki/
│   ├── __init__.py
│   └── cli.py
├── templates/
│   └── default/
│       ├── AGENTS.md
│       ├── raw/
│       │   └── .gitkeep
│       └── wiki/
│           ├── index.md
│           ├── log.md
│           └── overview.md
├── tests/
│   └── test_cli.py
├── examples/
│   └── tiny-research/
└── docs/
    ├── llm-wiki-concept.md
    └── superpowers/
        └── specs/
            └── 2026-04-20-llm-wiki-tool-design.md
```

## Template Workspace

Each initialized workspace contains:

- `raw/`: immutable source files curated by the user.
- `wiki/`: LLM-maintained markdown pages.
- `wiki/index.md`: content-oriented catalog of wiki pages.
- `wiki/log.md`: append-only chronological activity log.
- `wiki/overview.md`: entry point summarizing the current knowledge base.
- `AGENTS.md`: operating schema for LLM agents.

The template files should be readable and immediately useful after `llm-wiki init`.

## Agent Schema

`AGENTS.md` should define:

- Roles of `raw/`, `wiki/`, `index.md`, and `log.md`.
- Rules for ingesting one source at a time.
- Rules for answering queries from the wiki first.
- Rules for filing useful answers back into the wiki.
- Rules for linting the wiki for contradictions, stale claims, orphan pages, missing links, and missing concept pages.
- Markdown conventions, including wiki links, source citations, and consistent log headings.

The agent instructions should be generic enough to work across domains and specific enough to keep an LLM from treating the wiki like an unstructured notes folder.

## CLI Commands

Initial CLI commands:

- `llm-wiki init <path>`: create a new workspace from `templates/default`.
- `llm-wiki doctor <path>`: verify required folders and files exist.
- `llm-wiki log <path> [--limit N]`: print recent parseable entries from `wiki/log.md`.
- `llm-wiki index <path>`: print page links and summaries from `wiki/index.md`.

Expected behavior:

- `init` should refuse to overwrite non-empty directories unless a future explicit force flag is added.
- `doctor` should return a non-zero exit code when required files are missing.
- `log` should parse headings matching `## [YYYY-MM-DD] type | title`.
- `index` should parse simple markdown list entries containing links and summaries.

## Documentation

`README.md` should explain:

- What LLM Wiki is.
- How to install from a GitHub repo.
- How to initialize a workspace.
- How to use the workspace with an LLM coding agent and Obsidian.
- The difference between raw sources, wiki pages, and agent schema.

`docs/llm-wiki-concept.md` should preserve the original concept from `llm-wiki.md` in a stable docs location.

## Testing

Use `pytest`.

Tests should cover:

- `init` creates the expected workspace files.
- `init` refuses non-empty target directories.
- `doctor` succeeds on a fresh workspace.
- `doctor` fails when a required file is missing.
- `log` extracts recent log headings.
- `index` extracts wiki page links and summaries.

The test suite should run with:

```bash
pytest
```

## Scope Boundaries

This version will not implement embedding search, MCP, LLM API calls, document parsing, automatic source ingestion, or Obsidian plugin behavior. Those can be added later. The first useful version is a disciplined repo template plus a reliable local setup/check CLI.

## Acceptance Criteria

- The repo can be pushed to GitHub as a normal Python project.
- A user can install it from GitHub with a Python tool installer.
- `llm-wiki init my-wiki` creates a usable wiki workspace.
- `llm-wiki doctor my-wiki` confirms that workspace integrity.
- `pytest` passes locally.
- The generated `AGENTS.md` gives an LLM agent enough guidance to maintain the wiki without re-reading the original idea file.
