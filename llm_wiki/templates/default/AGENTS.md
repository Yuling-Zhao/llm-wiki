# LLM Wiki Operating Schema

You maintain this workspace as a persistent, compounding markdown wiki.

## Layers

- `raw/` contains immutable source materials supplied by the user. Read from it, do not edit it.
- `wiki/` contains LLM-maintained markdown pages. You may create and update these files.
- `wiki/source/` contains pages created directly from source ingestion.
- `wiki/synthesis/` contains synthesis pages refined through Q&A with users.
- `index.md` is the content catalog. Read it first when answering questions.
- `log.md` is the append-only activity record.
- `overview.md` is the entry point for the current synthesis.

## Ingest Workflow

When the user asks you to ingest a source:

1. Read the source from `raw/`.
2. If the assigned ingest source is a PDF:
   - Check for Poppler with `command -v pdftotext`.
   - If `pdftotext` is missing, ask the user to install Poppler before continuing.
   - Run `pdftotext -layout raw/<source-title>.pdf /tmp/trim-pdf-text/<source-title>.txt`.
   - Write converted text outside `raw/`, for example `/tmp/trim-pdf-text/<source-title>.txt`.
   - Ingest from the converted text and keep the original PDF as the source reference.
3. Summarize the source's key claims, evidence, entities, and concepts.
4. Create or update relevant pages in `wiki/source`.
5. Add cross-links between related wiki pages.
6. Update `index.md`.
7. Append an entry to `log.md` using `## [YYYY-MM-DD] ingest | Source Title`.

## Query Workflow

When the user asks a question:

1. Read `index.md`.
2. Open the most relevant wiki pages.
3. Answer from the wiki first, citing page links and source references when available.
4. If the answer creates reusable analysis, ask whether to file it back into `wiki/synthesis`.

## Lint Workflow

When asked to lint the wiki, check for contradictions, stale claims, orphan pages, missing backlinks, important concepts without pages, and source claims that are not reflected in the synthesis.

## Conventions

- Use markdown links for files and Obsidian-style `[[Page Name]]` links for wiki concepts.
- Keep source references close to claims.
- Do not silently delete useful prior synthesis. Mark superseded claims and explain why.
- Keep `log.md` append-only.
