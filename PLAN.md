# PLAN

## Current Stage

Completed: the Phase 1 official OpenAI English-Korean evaluation MVP is implemented and sample outputs have been generated.

## Completed

- inspected the existing repository structure
- confirmed that existing `docs/golden/` and `evals/` assets should be preserved as experimental or future-expansion paths
- fixed the phase distinction between the official document-pair MVP and later developers-doc expansion
- added `AGENTS.md`, `PLAN.md`, `EVAL_SPEC.md`, and rewrote `README.md` around the new MVP scope
- implemented `collect_pair.py` and `align_units.py`
- implemented `generate_candidate.py`, `run_eval.py`, and `build_report.py`
- generated sample outputs for `why-we-no-longer-evaluate-swe-bench-verified`

## Next

- expand the glossary and terminology heuristics beyond the initial rule set
- add more official OpenAI document pairs
- evaluate whether sentence-level alignment or developers-doc reference-less evaluation should become Phase 2 work

## Remaining Work

- tune terminology and style prompts for better consistency on proper nouns such as `Python`, `Prefill`, and `gold patch`
- decide which human-reviewed samples should be promoted to `reviewed_golden`
- keep the existing `docs/golden/` and `evals/` tracks as experimental assets while the official pair pipeline expands
