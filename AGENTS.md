# Repository Agents Guide

## Goal

This repository implements a translation quality evaluation MVP for official OpenAI English and Korean document pairs.

The primary demo path for this phase is:

1. collect an official `source_en` page and its official `reference_ko` counterpart
2. extract and clean the body text
3. align stable evaluation units
4. generate a new `candidate_ko` from `source_en`
5. compare `candidate_ko` against `reference_ko`
6. save machine-readable results and a human-readable report

## Phase 1 MVP Scope

Phase 1 is limited to official OpenAI English-Korean page pairs hosted on `openai.com`.

Current evaluation roles:

- `source_en`: official English source text
- `reference_ko`: official Korean translation published by OpenAI
- `candidate_ko`: a newly generated Korean translation produced by the pipeline
- `reviewed_golden`: a small, human-reviewed artifact that may be promoted later for deeper evaluation or regression testing

Important constraints:

- `reference_ko` is not automatically treated as `golden`
- `candidate_ko` is never stored as `golden`
- only human-reviewed samples should be promoted to `reviewed_golden`

## Phase 2 Expansion

The following are future-expansion tracks, not the main MVP path for this phase:

- `developers.openai.com` ingestion
- reference-less evaluation for developer docs
- broader candidate generation pipelines
- expansion of curated reviewed examples in `docs/golden/`

## Existing Assets

Existing files under `docs/golden/` and `evals/` remain in the repository as experimental or future-expansion assets. Do not delete them when working on the official document-pair MVP.
