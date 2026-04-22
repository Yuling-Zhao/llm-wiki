# Figure-Aware Paper Ingestion Design

## Purpose

Adapt LLM Wiki for scientific papers where figures are first-class evidence. The tool should initialize figure-ready workspaces, validate the required directories, and instruct LLM agents to create semantic markdown pages for figures instead of relying on PDF text extraction alone.

## Scope

This change updates the template, CLI checks, tests, and README. It does not implement automatic PDF figure extraction, computer vision, or a new parsing dependency. The LLM agent remains responsible for inspecting images and writing grounded figure pages.

## Workspace Structure

Initialized workspaces must include:

- `raw/assets/` for extracted or downloaded figure images.
- `wiki/figures/` for semantic figure pages.
- Existing paths remain in use:
  - `wiki/source/`
  - `wiki/synthesis/`
  - root `index.md`
  - root `log.md`
  - root `overview.md`

Figure page paths follow:

- `wiki/figures/<paper-slug>--fig-1.md`
- `wiki/figures/<paper-slug>--fig-2.md`
- `wiki/figures/<paper-slug>--fig-s1.md`

Figure image assets may be stored as:

- `raw/assets/<paper-slug>/fig1.png`
- `raw/assets/<paper-slug>/fig2.png`

## Agent Schema Changes

`AGENTS.md` must include a figure ingestion policy covering:

- Figures as first-class evidence objects.
- Required source and figure pages for paper ingestion.
- Figure page template.
- Source page `## Figures` and `## Figure-level takeaways` sections.
- Shown, observed, interpreted, and claim-supported evidence layers.
- Confidence wording rules.
- Hard rules against inventing labels or values.
- Scientific figure type handling.
- Cross-linking and logging requirements.
- Failure modes when figures or captions are incomplete.
- Priority rule that central figures are processed early.

The policy should use the current template's root `index.md` and `log.md` convention.

## Doctor Behavior

`llm-wiki doctor <path>` should support two modes:

- If `<path>` is an initialized workspace, validate required paths and report missing files or directories.
- If `<path>` does not exist, run dependency preflight checks and print guidance without failing. This lets users run `llm-wiki doctor my-wiki` before `llm-wiki init my-wiki`.

Dependency checks should include:

- `pdftotext` for PDF text extraction.
- `pdftoppm` for PDF page/image extraction workflows.

When dependencies are missing, `doctor` should explain how to install Poppler on macOS and Debian/Ubuntu. Missing dependencies should be warnings, not fatal errors, because plain markdown workflows still work.

## README Changes

README should recommend:

1. Run `llm-wiki doctor my-wiki` first to check dependencies.
2. Install missing dependencies if needed.
3. Run `llm-wiki init my-wiki`.

README should also explain figure-aware paper ingestion and the role of `raw/assets/` and `wiki/figures/`.

## Tests

Update pytest coverage to verify:

- `init` creates `raw/assets/` and `wiki/figures/`.
- `doctor` requires those paths for initialized workspaces.
- `doctor` can run before `init` when the target path does not exist.
- `doctor` prints dependency guidance when Poppler tools are missing.
- Initialized `AGENTS.md` includes the figure page template and figure workflow rules.

## Acceptance Criteria

- `pytest` passes.
- A fresh workspace is figure-ready.
- `doctor` is useful before and after `init`.
- README tells users to run `doctor`, install dependencies, then run `init`.
- Figure instructions are included in both source template files and packaged template files.
