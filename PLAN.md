# PLAN

## Current Stage

The Phase 1 official OpenAI English-Korean document-pair MVP is implemented. This branch is focused on making that MVP easier for external reviewers to understand and evaluate.

## Completed

- defined the Phase 1 scope around official `openai.com` EN-KO page pairs
- preserved `docs/golden/` and `evals/` as experimental or future-expansion assets
- implemented the current collection, alignment, candidate generation, evaluation, and report-building scripts
- generated sample outputs for `why-we-no-longer-evaluate-swe-bench-verified`
- clarified that `reference_ko` is not automatically golden and that only human-reviewed items can become `reviewed_golden`
- rewrote repository-facing documentation for clearer external review
- updated the recommended current MVP model configuration to `gpt-5.4-mini`

## Next Steps

- add more official `openai.com` English-Korean page pairs
- expand the human review queue and promote only reviewed items to `reviewed_golden`
- improve terminology and style guidance for repeated document-critical terms
- extend the same framework to `developers.openai.com` in Phase 2, where reference-less evaluation and community review will matter more
