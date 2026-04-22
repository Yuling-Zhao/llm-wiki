# LLM Wiki Operating Schema

You maintain this workspace as a persistent, compounding markdown wiki.

## Layers

- `raw/` contains immutable source materials supplied by the user. Read from it, do not edit it.
- `raw/assets/` contains extracted or downloaded figure images and other source-adjacent assets.
- `wiki/` contains LLM-maintained markdown pages. You may create and update these files.
- `wiki/figures/` contains semantic figure pages. Figures are evidence objects, not attachments.
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

## Figure Ingestion Policy

Figures in papers are first-class evidence objects, not just attachments. When ingesting any paper that contains figures, process both the paper text and its figures. Do not rely on PDF text extraction alone.

For each figure, preserve:

1. What the figure contains.
2. What claim the figure supports.
3. Which panels provide which evidence.
4. How the figure connects to concepts, entities, methods, and conclusions already present in the wiki.

When a paper is ingested, use these inputs if available:

- The original PDF in `raw/`.
- Extracted paper text.
- Figure images extracted from the PDF or downloaded separately.
- Figure captions.
- Supplementary figure captions, if present.

If figure extraction is incomplete or low quality, say so explicitly in the source page and in the affected figure pages.

### Required Figure Outputs

For each ingested paper, create:

- One source page in `wiki/source/`.
- One figure page per main figure in `wiki/figures/`.
- Optionally one figure page per supplementary figure in `wiki/figures/`.
- Links from the source page to all figure pages.
- Links from relevant concept/entity pages to figure pages when the figure contributes evidence.

Use these paths:

- `wiki/source/<paper-slug>.md`
- `wiki/figures/<paper-slug>--fig-1.md`
- `wiki/figures/<paper-slug>--fig-2.md`
- `wiki/figures/<paper-slug>--fig-s1.md`

If needed, store extracted figure images outside the wiki text pages:

- `raw/assets/<paper-slug>/fig1.png`
- `raw/assets/<paper-slug>/fig2.png`

Do not treat stored images as sufficient output. Every figure must also have a semantic markdown page.

### Figure Ingestion Workflow

For each figure:

1. Identify the figure number and caption.
2. Inspect the image and panel structure if the image is available.
3. Determine the experiment or data modality shown in each panel when possible.
4. Write a figure page that separates direct visual content, caption-grounded description, scientific interpretation, and the claim the figure supports.
5. Link the figure page to relevant concept, method, dataset, gene, protein, disease, or model pages.
6. Update the source page with a `## Figures` section linking all figure pages.
7. Update any affected synthesis pages if the figure materially changes the current understanding.

Always prefer grounded interpretation. If a conclusion is only weakly supported by the caption or image, mark it as tentative.

### Figure Page Template

```markdown
# Figure: <Paper Short Title> - Fig <N>

## Source
- Paper: [[<paper source page>]]
- Figure number: Fig <N>
- Image path: `<path if available>`
- Caption status: full / partial / missing
- Image quality: good / usable / poor

## One-line summary
A concise statement of the main message of the figure.

## Panel map
- A: <what is shown>
- B: <what is shown>
- C: <what is shown>

If panel boundaries are unclear, say so.

## Caption-grounded description
Restate the figure content conservatively using the caption and visible labels only. Do not over-interpret here.

## Observations
- Observation 1
- Observation 2
- Observation 3

These should be descriptive, not speculative.

## Interpretation
Explain what the figure suggests scientifically.

Distinguish clearly between:

- Direct evidence from the figure.
- Reasonable interpretation.
- Broader paper-level claim.

## Claim supported
State the specific claim this figure supports in the paper.

## Key entities and concepts
- [[Entity 1]]
- [[Concept 1]]
- [[Method 1]]

## Data / method tags
- `<omics>`
- `<assay>`
- `<organism>`
- `<cell-type>`
- `<perturbation>`

## Reusable facts
- Fact 1
- Fact 2

## Open questions / caveats
- Any ambiguity in panel interpretation.
- Any mismatch between caption and visible figure.
- Any unresolved uncertainty.
```

### Source Page Figure Sections

Each source page for a paper with figures must include:

```markdown
## Figures
- [[<paper-slug>--fig-1]] - <one-line message>
- [[<paper-slug>--fig-2]] - <one-line message>
- [[<paper-slug>--fig-s1]] - <one-line message>

## Figure-level takeaways
Summarize the most important evidence contributed by the figures across the paper.
```

### Evidence Layers

Keep these layers separate when writing figure pages:

1. Shown: what is directly visible or explicitly labeled.
2. Observed: what pattern can be described without much interpretation.
3. Interpreted: what the pattern likely means scientifically.
4. Claim supported: what paper-level argument this figure contributes to.

Do not collapse these layers into one paragraph.

### Confidence Rules

Use confidence-matched language:

- High confidence: use when caption and image clearly align. Prefer words like "shows" and "demonstrates".
- Medium confidence: use when the figure supports the conclusion but details are partly ambiguous. Prefer words like "supports" and "suggests".
- Low confidence: use when the image is hard to parse, low resolution, or caption is incomplete. Prefer words like "may indicate" and "appears consistent with".

### Hard Rules

- Never invent panel labels or results.
- Never infer exact quantitative values unless explicitly shown.
- Never treat the figure alone as stronger evidence than the caption plus paper context.
- If the image is unavailable, still create a figure page from the caption, but clearly mark it as caption-only.
- If a figure is central to the paper's thesis, link it from relevant synthesis pages.
- If a figure contradicts an existing wiki claim, note that contradiction explicitly and update affected pages.

### Scientific Figure Types

For common paper figure types, extract structured meaning where possible:

- Heatmaps: capture axis meaning, clusters, trends, and enriched groups.
- Genomic tracks: capture loci, signal differences, mark/assay type, and condition contrast.
- Hi-C contact maps: capture compartment patterns, domains, interaction changes, and resolution if stated.
- UMAP/PCA: capture grouping, separation, transitions, and dominant contrast.
- Bar/box/violin plots: capture compared groups and direction of change, not exact numbers unless labeled.
- Microscopy: capture localization, morphology, qualitative differences, and markers.
- Schematics: capture conceptual workflow or mechanism and mark as model/proposal, not empirical evidence.

### Cross-Linking, Logging, and Failure Modes

When a figure provides reusable evidence, update or link concept pages, entity pages, method pages, comparison pages, and synthesis pages.

For each ingested paper, append a parseable log entry that records figure work:

```markdown
## [YYYY-MM-DD] ingest | <Paper Title>
- created source page
- created figure pages: fig-1, fig-2, fig-3, fig-s1
- updated concept pages: [[Concept A]], [[Concept B]]
- notes: fig-2 image quality poor; interpretation partly caption-only
```

If figure handling is incomplete, do not silently skip it. Create the source page, create partial figure pages for available captions, mark missing figures explicitly, add a note in the source page, and record the limitation in `log.md`.

If time or context is limited, prioritize:

1. Title and abstract.
2. Central figures.
3. Discussion and conclusion.
4. Remaining figures.
5. Supplementary figures.

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
