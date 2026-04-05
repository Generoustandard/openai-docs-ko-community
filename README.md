# OpenAI Docs Korean Community

This repository is a Phase 1 MVP for evaluating Korean translation quality on official OpenAI English-Korean document pairs hosted on `openai.com`.

The MVP exists to validate the evaluation framework on a clean reference setup before extending the same framework to `developers.openai.com`, where Korean references are limited and reference-less evaluation plus community review will matter more.

Codex is used here to generate `candidate_ko`, support the evaluation workflow, and prepare the project for future agent-assisted improvement loops.

## Phase Scope

### Phase 1 MVP

Phase 1 is intentionally narrow:

- collect one official English page as `source_en`
- collect its official Korean counterpart as `reference_ko`
- align stable paragraph-level evaluation units
- generate a new Korean translation as `candidate_ko`
- compare `candidate_ko` against `reference_ko`
- save machine-readable results and a human-readable report

Current evaluation roles:

| Role | Meaning |
| --- | --- |
| `source_en` | Official English source text from OpenAI |
| `reference_ko` | Official Korean translation published by OpenAI |
| `candidate_ko` | A newly generated Korean translation produced by the pipeline |
| `reviewed_golden` | A human-reviewed example that may later be promoted for regression testing or deeper evaluation |

Important constraints:

- `reference_ko` is a reference, not automatically a golden sample.
- `candidate_ko` is never stored as golden.
- Only manual review by the maintainer or community reviewers can promote an item to `reviewed_golden`.

### Phase 2 Expansion

Phase 2 is a later extension of the same framework, not the current MVP:

- ingestion for `developers.openai.com`
- reference-less evaluation where Korean references do not exist
- stronger community review and promotion workflows
- broader candidate generation paths
- expansion of curated `reviewed_golden` assets

## Why Start With Official EN-KO Page Pairs

Official `openai.com` English-Korean page pairs provide a clearer reference path for validating the evaluation design. That makes it easier to test alignment, scoring, reporting, and human review rules before moving to developers documentation, where the reference signal is weaker.

## Current Demo Pair

- English: [why-we-no-longer-evaluate-swe-bench-verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- Korean: [why-we-no-longer-evaluate-swe-bench-verified (ko-KR)](https://openai.com/ko-KR/index/why-we-no-longer-evaluate-swe-bench-verified/)

## Where Codex Is Used

- Candidate generation: produce `candidate_ko` from aligned `source_en` blocks.
- Evaluation workflow support: run backtranslation, LLM judging, scoring, and reporting.
- Iterative improvement path: provide a base for future agent loops that re-run evaluation, surface review queues, and support human-reviewed promotion to `reviewed_golden`.

## Recommended Command Sequence

Prerequisites:

- Python 3.11+
- Chrome installed
- `OPENAI_API_KEY` set
- `pip install -r requirements.txt`

Recommended MVP demo configuration:

- `generation_model`: `gpt-5.4-mini`
- `backtranslation_model`: `gpt-5.4-mini`
- `judge_model`: `gpt-5.4-mini`

Recommended run sequence:

```powershell
python -X utf8 collect_pair.py --slug why-we-no-longer-evaluate-swe-bench-verified --source-url https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ --reference-url https://openai.com/ko-KR/index/why-we-no-longer-evaluate-swe-bench-verified/
python -X utf8 align_units.py --slug why-we-no-longer-evaluate-swe-bench-verified
python -X utf8 generate_candidate.py --input data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json --model gpt-5.4-mini
python -X utf8 run_eval.py --input data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json --backtranslation-model gpt-5.4-mini --judge-model gpt-5.4-mini --embedding-model text-embedding-3-small
python -X utf8 build_report.py --input reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json --output reports/why-we-no-longer-evaluate-swe-bench-verified.report.md
```

Notes:

- `collect_pair.py` uses Chrome and is safest in non-headless mode for the current `openai.com` pages.
- The script defaults now point to `gpt-5.4-mini`, but the commands above keep the recommended configuration explicit for reviewers.
- On Windows, use `py -3 -X utf8` if `python -X utf8` is not available on `PATH`.

## Checked-In Sample Artifacts

The repository keeps sample artifacts for the current demo pair under `docs/pairs/`, `data/processed/`, and `reports/`.

The checked-in sample candidate, evaluation, and report artifacts have been refreshed for the current Phase 1 MVP demo configuration:

- `generation_model`: `gpt-5.4-mini`
- `backtranslation_model`: `gpt-5.4-mini`
- `judge_model`: `gpt-5.4-mini`

Their recorded timestamps and metadata should be treated as the provenance source for the current checked-in demo run.

Key sample files:

- [docs/pairs/why-we-no-longer-evaluate-swe-bench-verified/pair_manifest.json](docs/pairs/why-we-no-longer-evaluate-swe-bench-verified/pair_manifest.json)
- [data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json](data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json)
- [data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json](data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json)
- [reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json](reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json)
- [reports/why-we-no-longer-evaluate-swe-bench-verified.report.md](reports/why-we-no-longer-evaluate-swe-bench-verified.report.md)

## Repository Map

- [AGENTS.md](AGENTS.md): repository operating notes
- [PLAN.md](PLAN.md): current project stage and next steps
- [EVAL_SPEC.md](EVAL_SPEC.md): Phase 1 evaluation specification
- [evals/README.md](evals/README.md): preserved legacy experimental evaluation path

## Existing Experimental Assets

Existing files under `docs/golden/` and `evals/` are preserved as experimental or future-expansion assets. They are not the primary path for the current Phase 1 official document-pair MVP, and they should not be deleted during this cleanup.
