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
