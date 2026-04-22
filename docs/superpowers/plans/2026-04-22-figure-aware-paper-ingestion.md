# Figure-Aware Paper Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make LLM Wiki initialize and validate figure-aware scientific-paper workspaces.

**Architecture:** Keep runtime dependency-free. Extend the static template directories and `AGENTS.md` instructions, then update `llm_wiki/cli.py` so `doctor` can run as both a pre-init dependency preflight and a post-init workspace validator.

**Tech Stack:** Python 3.10+, argparse, pathlib, shutil, pytest, markdown templates.

---

## File Structure

- `tests/test_cli.py`: add tests for figure directories, figure schema text, pre-init doctor, and Poppler dependency warnings.
- `llm_wiki/cli.py`: update required paths and doctor preflight behavior.
- `templates/default/AGENTS.md`: add figure ingestion policy.
- `llm_wiki/templates/default/AGENTS.md`: keep packaged template in sync.
- `templates/default/raw/assets/.gitkeep`: preserve asset directory.
- `templates/default/wiki/figures/.gitkeep`: preserve figure page directory.
- `llm_wiki/templates/default/raw/assets/.gitkeep`: packaged asset directory.
- `llm_wiki/templates/default/wiki/figures/.gitkeep`: packaged figure directory.
- `README.md`: document doctor-before-init and figure-aware ingestion.

## Tasks

- [ ] Add failing tests for `raw/assets`, `wiki/figures`, figure schema text, and pre-init `doctor`.
- [ ] Update template directories and packaged template directories.
- [ ] Update `AGENTS.md` figure policy in both template copies.
- [ ] Update `llm_wiki/cli.py` doctor behavior and dependency checks.
- [ ] Update README usage order and figure ingestion notes.
- [ ] Run `pytest`.
- [ ] Run installed/manual smoke checks for `doctor`, `init`, and `doctor` after init.

## Self-Review

- Spec coverage: Covers workspace structure, agent schema, doctor preflight behavior, README, tests, and acceptance criteria.
- Placeholder scan: No placeholder implementation instructions remain.
- Type consistency: Existing CLI pattern remains integer return codes with `Path` arguments.
