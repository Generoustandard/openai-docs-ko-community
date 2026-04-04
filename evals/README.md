# Legacy Eval Sandbox

This directory contains an earlier experimental evaluation path that predates the current Phase 1 official document-pair MVP.

It is preserved for reference and future expansion, but it is not the main review path for this repository. The current MVP lives at the repository root and evaluates official `openai.com` English-Korean page pairs with `source_en`, `reference_ko`, `candidate_ko`, and human-review routing.

## What This Folder Represents

- a lightweight cosine-similarity prototype
- experiments built around curated examples under `docs/golden/`
- a preserved sandbox for future comparison work

## What It Does Not Represent

- the primary Phase 1 MVP
- the current official EN-KO document-pair workflow
- an automatically maintained golden dataset

## Files

- [golden_loader.py](golden_loader.py): loads preserved golden-style experimental inputs from `docs/golden/`
- [metrics.py](metrics.py): simple metric helpers used by the legacy sandbox
- [run_eval.py](run_eval.py): runs the legacy similarity-only evaluation flow
- [results/README.md](results/README.md): notes for legacy result outputs

## Relationship To The Current MVP

Keep this directory in the repository, but do not treat it as the main deliverable for external review of the official document-pair MVP.
