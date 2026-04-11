# Repository Agents Guide

## Goal

This repository packages a reviewable Phase 1 MVP for evaluating Korean translation quality on official OpenAI English-Korean document pairs.

## Current MVP Scope

- Phase 1 focuses on official `openai.com` EN-KO page pairs.
- The primary flow is: collect the pair, align paragraph-level units, generate `candidate_ko`, evaluate against `reference_ko`, and build a report.
- A lightweight golden-example layer also exists under `docs/golden/` for word, sentence, and paragraph checks.
- `developers.openai.com` is a Phase 2 expansion track, not the current MVP path.

## Evaluation Roles

- `source_en`: official English source text
- `reference_ko`: official Korean translation published by OpenAI
- `candidate_ko`: newly generated Korean translation produced by the pipeline
- `improved_candidate_ko`: optional follow-up revision used for re-evaluation if present
- `reviewed_golden`: curated human-reviewed example used for lightweight regression, sanity checks, and later comparison

## Constraints

- `reference_ko` is a reference, not automatically golden.
- `candidate_ko` is never stored as golden.
- `improved_candidate_ko` is still a candidate output, not golden.
- Only manual review by the maintainer or community reviewers can promote an item to `reviewed_golden`.

## Asset Preservation

Keep existing files under `docs/golden/` and `evals/`. The curated files in `docs/golden/words.json`, `docs/golden/sentences.json`, and `docs/golden/paragraphs.json` support lightweight reviewed-golden checks, while `evals/` remains a preserved experimental path. Do not delete them while working on the Phase 1 official document-pair MVP.
