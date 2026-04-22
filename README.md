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

## Check Dependencies

Run `doctor` before creating a workspace. It checks whether optional paper-ingestion
dependencies are available and tells you what to install.

```bash
llm-wiki doctor my-wiki
```

If Poppler tools are missing and you plan to ingest PDF papers, install them first:

```bash
# macOS
brew install poppler

# Debian/Ubuntu
sudo apt install poppler-utils
```

## Create a Workspace

```bash
llm-wiki doctor my-wiki
llm-wiki init my-wiki
cd my-wiki
```

The workspace contains:

- `raw/` for immutable source files.
- `raw/assets/` for extracted or downloaded figure images.
- `wiki/figures/` for semantic figure pages.
- `wiki/source/` for pages created directly from source ingestion.
- `wiki/synthesis/` for synthesis pages refined through Q&A.
- `index.md` for the content catalog.
- `log.md` for chronological activity.
- `overview.md` for the current synthesis entry point.
- `AGENTS.md` for LLM-agent operating instructions.

## Check an Initialized Workspace

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

## Figure-Aware Paper Ingestion

Scientific figures are first-class evidence objects. When ingesting papers, the
LLM agent should process the paper text, captions, and available figure images.
Figure images can be stored under `raw/assets/<paper-slug>/`, but each figure
also needs a semantic markdown page under `wiki/figures/`.

Expected figure page paths:

```text
wiki/figures/<paper-slug>--fig-1.md
wiki/figures/<paper-slug>--fig-2.md
wiki/figures/<paper-slug>--fig-s1.md
```

Each source page in `wiki/source/` should include:

- `## Figures`
- `## Figure-level takeaways`

The generated workspace `AGENTS.md` includes the full figure policy: panel maps,
caption-grounded descriptions, observations, interpretation, supported claims,
confidence wording, cross-linking rules, and failure handling for missing or
low-quality figures.
