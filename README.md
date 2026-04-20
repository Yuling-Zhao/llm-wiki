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

## PDF Sources

LLM Wiki keeps the core CLI dependency-free. If you put PDF files in `raw/`,
install a PDF text extraction tool or provide extracted text beside the PDF.

Recommended Poppler install:

```bash
# macOS
brew install poppler

# Debian/Ubuntu
sudo apt install poppler-utils
```

Extract text before ingestion:

```bash
pdftotext -layout raw/paper.pdf raw/paper.txt
```

A good source layout is:

```text
raw/paper.pdf
raw/paper.txt
```

Then ask your LLM agent to ingest `raw/paper.txt`, treating `raw/paper.pdf` as
the original source. `llm-wiki doctor` warns when PDFs are present in `raw/` and
`pdftotext` is not available.
