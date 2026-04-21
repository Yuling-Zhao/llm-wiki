# LLM Wiki

LLM Wiki is a local template and CLI for building personal knowledge bases that compound over time. Instead of asking an LLM to retrieve raw chunks from documents on every question, you ask the LLM to maintain a persistent markdown wiki between you and the raw sources.

This project is based on Andrej Karpathy's original `llm-wiki.md` idea note: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>.

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
- `wiki/source/` for pages created directly from source ingestion.
- `wiki/synthesis/` for synthesis pages refined through Q&A.
- `index.md` for the content catalog.
- `log.md` for chronological activity.
- `overview.md` for the current synthesis entry point.
- `AGENTS.md` for LLM-agent operating instructions.

## Check a Workspace

```bash
llm-wiki doctor my-wiki
llm-wiki index my-wiki
llm-wiki log my-wiki
```

## Work With an LLM Agent

Open the workspace with Codex, Claude Code, OpenCode, or another coding agent. Ask the agent to follow `AGENTS.md`, ingest files from `raw/`, update pages in `wiki/source/` and `wiki/synthesis/`, maintain `index.md`, and append parseable entries to `log.md`.

Obsidian works well as the reading and browsing interface because the wiki is just markdown.

## PDF Sources

LLM Wiki keeps the core CLI dependency-free. When the assigned ingest source is
a PDF, keep the original PDF in `raw/` and convert a temporary text copy outside
`raw/` for ingestion.

Recommended Poppler install:

```bash
# macOS
brew install poppler

# Debian/Ubuntu
sudo apt install poppler-utils
```

The LLM agent should first check whether Poppler is available:

```bash
command -v pdftotext
```

If `pdftotext` is available, convert with layout preservation:

```bash
mkdir -p /tmp/trim-pdf-text
pdftotext -layout raw/paper.pdf /tmp/trim-pdf-text/paper.txt
```

Then ask your LLM agent to ingest `/tmp/trim-pdf-text/paper.txt`, keeping
`raw/paper.pdf` as the original source reference. `llm-wiki doctor` warns when
PDFs are present in `raw/` and `pdftotext` is not available.
