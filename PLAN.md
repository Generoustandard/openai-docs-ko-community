# PLAN

## Current Stage

The Phase 1 official OpenAI English-Korean document-pair MVP is implemented. This branch is focused on making that MVP easier for external reviewers to understand and evaluate.

## Completed

- defined the Phase 1 scope around official `openai.com` EN-KO page pairs
- preserved `docs/golden/` and `evals/` instead of deleting or redesigning them
- implemented the current collection, alignment, candidate generation, evaluation, and report-building scripts
- generated sample outputs for `why-we-no-longer-evaluate-swe-bench-verified`
- clarified that `reference_ko` is not automatically golden and that only human-reviewed items can become `reviewed_golden`
- reframed `docs/golden/words.json`, `docs/golden/sentences.json`, and `docs/golden/paragraphs.json` as lightweight reviewed-golden evaluation assets
- added a lightweight golden-set evaluation path for word, sentence, and paragraph checks
- added optional comparison metadata for later model, prompt, and pipeline comparisons
- rewrote repository-facing documentation for clearer external review
- updated the recommended current MVP model configuration to `gpt-5.4-mini`

## Next Steps

- add more official `openai.com` English-Korean page pairs
- use the current evaluation-first path as the base for `candidate_ko -> evaluation -> improved_candidate_ko -> human review`
- expand the human review queue and promote only reviewed items to `reviewed_golden`
- use the reviewed-golden layer for lightweight sanity checks before and after prompt, model, or pipeline changes
- improve terminology and style guidance for repeated document-critical terms
- extend the same framework to `developers.openai.com` in Phase 2, where reference-less evaluation and community review will matter more
