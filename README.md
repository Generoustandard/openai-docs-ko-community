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
| `improved_candidate_ko` | An optional follow-up revision produced after evaluation or review |
| `reviewed_golden` | A human-reviewed example that may later be promoted for regression testing or deeper evaluation |

Important constraints:

- `reference_ko` is a reference, not automatically a golden sample.
- `candidate_ko` is never stored as golden.
- `improved_candidate_ko` is still a candidate output, not a golden sample.
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

## Evaluation Framing

This repository now supports two compatible evaluation layers:

- Official document-pair evaluation: compare `candidate_ko` against the official `reference_ko` for the current Phase 1 `openai.com` page pair.
- Golden-example evaluation: compare generated Korean against a small curated `reviewed_golden` set at the word, sentence, and paragraph levels under `docs/golden/`.

The main quantitative signals align with the OpenAI-suggested direction:

- Korean-side cosine similarity: compare generated Korean to a reference-like target.
  For the Phase 1 pair MVP, that target is `reference_ko`.
  For lightweight regression checks, that target is the curated golden Korean example.
- Backtranslation cosine similarity: compare `source_en` against English translated back from the generated Korean.
- Metadata for comparison: preserve model labels and optional `run_label`, `pipeline_label`, and `prompt_label` fields so later runs can be compared across models, prompts, and pipelines.

Important distinction:

- `reference_ko` is the official page-level reference for the current Phase 1 pair evaluation.
- `reviewed_golden` is a small curated or human-reviewed target set used for sanity checks and regression-style comparison.
- Neither raw `candidate_ko` nor optional `improved_candidate_ko` is treated as golden automatically.

## Current Demo Pair

- English: [why-we-no-longer-evaluate-swe-bench-verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- Korean: [why-we-no-longer-evaluate-swe-bench-verified (ko-KR)](https://openai.com/ko-KR/index/why-we-no-longer-evaluate-swe-bench-verified/)

## Where Codex Is Used

- Candidate generation: produce `candidate_ko` from aligned `source_en` blocks.
- Evaluation workflow support: run backtranslation, LLM judging, scoring, and reporting.
- Iterative improvement path: support a `candidate_ko -> evaluation -> improved_candidate_ko -> human review` direction while keeping small golden-set checks available for regression and comparison.

## Improvement-Loop Direction

The current Phase 1 MVP validates evaluation on raw `candidate_ko` first. The next step is a lightweight improvement path:

- evaluate `candidate_ko`
- optionally produce `improved_candidate_ko`
- re-evaluate if needed
- promote only manually reviewed items toward `reviewed_golden`

This future step is compatible with the same cosine-similarity, backtranslation, and reviewed-golden checks described above.

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

## Golden Example Checks

The curated or future-curated reviewed-golden layer lives under [docs/golden/README.md](docs/golden/README.md) and is organized as:

- [docs/golden/words.json](docs/golden/words.json)
- [docs/golden/sentences.json](docs/golden/sentences.json)
- [docs/golden/paragraphs.json](docs/golden/paragraphs.json)

These examples are intended for lightweight comparison and regression checks, not as substitutes for the Phase 1 official page reference.

Example golden-set run:

```powershell
python -X utf8 run_golden_eval.py --golden-set sentences --generation-model gpt-5.4-mini --backtranslation-model gpt-5.4-mini --embedding-model text-embedding-3-small --run-label sentences-baseline --pipeline-label baseline --prompt-label official_openai_style_translation_v1
```

If you already have revised outputs, you can evaluate a different field from an input file:

```powershell
python -X utf8 run_golden_eval.py --golden-set paragraphs --input path/to/candidates.json --candidate-field improved_candidate_ko --backtranslation-model gpt-5.4-mini --embedding-model text-embedding-3-small --run-label paragraphs-improved
```

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

Existing files under `docs/golden/` and `evals/` are preserved. The curated files under `docs/golden/` now support the lightweight reviewed-golden evaluation layer, while `evals/` remains a legacy experimental path rather than the main Phase 1 MVP flow.
