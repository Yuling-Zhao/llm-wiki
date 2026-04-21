# Tiny Research Example

This example shows the intended workflow:

1. Put source files in `raw/`.
2. Ask an LLM agent to ingest one source.
3. Review generated source pages in `wiki/source/`.
4. Ask follow-up questions and file useful answers into `wiki/synthesis/`.

Run this first:

```bash
llm-wiki init tiny-research
llm-wiki doctor tiny-research
```
