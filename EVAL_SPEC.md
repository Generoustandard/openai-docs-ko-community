# Evaluation Spec

## Purpose

This specification defines the Phase 1 MVP for evaluating Korean translation quality on an official OpenAI English-Korean document pair.

## Scope

Phase 1 is limited to official `openai.com` page pairs with both:

- `source_en`: official English source text
- `reference_ko`: official Korean translation published by OpenAI

The evaluation pipeline generates:

- `candidate_ko`: a new Korean translation from `source_en`
- `improved_candidate_ko`: an optional follow-up revision that may be re-evaluated later
- `backtranslated_en`: an English backtranslation of `candidate_ko`

`reviewed_golden` is outside the automated Phase 1 scoring loop. It is reserved for samples that have been manually reviewed and intentionally promoted later for regression testing or deeper evaluation.

Important constraints:

- `reference_ko` is a reference, not automatically golden.
- `candidate_ko` is never stored as golden.
- `improved_candidate_ko` is still a candidate output, not golden.
- Only human-reviewed samples can become `reviewed_golden`.

## Compatible Evaluation Layers

The repository now supports two compatible evaluation layers:

1. Official document-pair evaluation for the Phase 1 MVP.
   This compares `candidate_ko` against the official page-level `reference_ko`.
2. Lightweight golden-example evaluation for regression and comparison.
   This compares generated Korean against curated or human-reviewed examples in `docs/golden/` across words, sentences, and paragraphs.

This keeps the Phase 1 framing intact while matching the OpenAI-suggested direction of using:

- a small golden set
- Korean-side cosine similarity
- backtranslation similarity
- later comparison across models, prompts, and pipelines

## Unit Choice

The MVP uses paragraph-level alignment. In practice, each evaluation unit is a stable prose block extracted from the article body:

- paragraph blocks (`p`)
- list items (`li`)
- section headers (`h2` to `h3`)

Code blocks, diffs, and code-example captions are excluded from the first-pass evaluation dataset because they are primarily source-preservation artifacts, not Korean translation quality signals.

The separate golden-example layer is intentionally broader in unit size and keeps curated examples at:

- word level
- sentence level
- paragraph level

## Payload Shapes

### Aligned Input

The current aligned input under `data/processed/` is a top-level list:

```json
[
  {
    "id": "why-we-no-longer-evaluate-swe-bench-verified.block-001",
    "unit_type": "paragraph",
    "source_en": "English source block",
    "reference_ko": "Official Korean reference block",
    "source_meta": {
      "tag": "P",
      "source_index": 1,
      "reference_index": 1,
      "pair_slug": "why-we-no-longer-evaluate-swe-bench-verified"
    }
  }
]
```

The shared loader also accepts an object with a top-level `records` array, but the current Phase 1 aligned input is a flat list.

### Candidate Generation Output

`generate_candidate.py` writes an object with metadata plus `records`:

```json
{
  "generated_at": "2026-03-31T16:59:18.814737+00:00",
  "generation_model": "gpt-5.4-mini",
  "run_label": "phase1-baseline",
  "pipeline_label": "baseline",
  "prompt_label": "official_openai_style_translation_v1",
  "records": [
    {
      "id": "why-we-no-longer-evaluate-swe-bench-verified.block-001",
      "unit_type": "paragraph",
      "source_en": "English source block",
      "reference_ko": "Official Korean reference block",
      "candidate_ko": "Generated Korean block",
      "source_meta": {
        "tag": "P",
        "pair_slug": "why-we-no-longer-evaluate-swe-bench-verified"
      }
    }
  ]
}
```

### Evaluation Output

`run_eval.py` writes an object with metadata, configuration, summary, and evaluated `records`:

```json
{
  "generation_model": "gpt-5.4-mini",
  "evaluated_at": "2026-03-31T17:02:52.303607+00:00",
  "config": {
    "candidate_field": "candidate_ko",
    "backtranslation_model": "gpt-5.4-mini",
    "judge_model": "gpt-5.4-mini",
    "embedding_model": "text-embedding-3-small",
    "score_scale": "0-100",
    "overall_formula": "0.30 * semantic_similarity_score + 0.25 * backtranslation_similarity_score + 0.15 * terminology_consistency_score + 0.30 * llm_judge_score"
  },
  "summary": {
    "count": 46,
    "average_overall_score": 92.4,
    "human_review_count": 7
  },
  "records": [
    {
      "id": "why-we-no-longer-evaluate-swe-bench-verified.block-001",
      "source_en": "English source block",
      "reference_ko": "Official Korean reference block",
      "candidate_ko": "Generated Korean block",
      "backtranslated_en": "Backtranslated English block",
      "semantic_similarity_score": 92.4,
      "backtranslation_similarity_score": 89.7,
      "terminology_consistency_score": 100.0,
      "llm_judge_score": 90.0,
      "overall_score": 91.0,
      "issues": [
        "Minor style drift around benchmark phrasing."
      ],
      "judge_needs_human_review": false,
      "review_reasons": [
        "terminology_consistency_score < 100"
      ],
      "needs_human_review": true,
      "suggested_revision": "Revised Korean text",
      "metadata": {
        "unit_type": "paragraph",
        "tag": "P",
        "pair_slug": "why-we-no-longer-evaluate-swe-bench-verified",
        "candidate_source_field": "candidate_ko",
        "terminology_details": [
          {
            "label": "SWE-bench Verified",
            "matched": true
          }
        ]
      }
    }
  ]
}
```

## Score Scale

All scores use a `0-100` scale.

## Metric Definitions

### `semantic_similarity_score`

Embedding cosine similarity between generated Korean and the Korean-side comparison target, converted with:

```text
semantic_similarity_score = clamp(cosine_similarity(korean_target, candidate_ko), 0, 1) * 100
```

For the official Phase 1 document-pair MVP, `korean_target = reference_ko`.

For the lightweight golden-example layer, `korean_target = reviewed_golden_ko` from the curated golden set.

### `backtranslation_similarity_score`

1. translate `candidate_ko` back into English to produce `backtranslated_en`
2. compute embedding cosine similarity between `source_en` and `backtranslated_en`
3. convert with:

```text
backtranslation_similarity_score = clamp(cosine_similarity(source_en, backtranslated_en), 0, 1) * 100
```

This metric is shared across both evaluation layers and is especially useful for comparing models, prompts, or improvement pipelines that may choose different Korean wording while preserving the original English meaning.

### `terminology_consistency_score`

Rule-based score over a small glossary of document-critical terms. The current implementation checks only rules whose source-side pattern appears in `source_en`, then scores:

```text
terminology_consistency_score = (matched_applicable_rules / applicable_rules) * 100
```

If no terminology rule applies to a unit, the score is `100.0`.

Current rule labels:

- `SWE-bench Verified`
- `SWE-bench Pro`
- `frontier`
- `benchmark`
- `contamination`
- `gold patch`
- `Preparedness Framework`

### `llm_judge_score`

LLM-judged score on a `0-100` scale based on:

- accuracy
- naturalness
- terminology consistency
- document style fit

The judge also returns:

- `issues`
- `judge_needs_human_review`
- `suggested_revision`

## Overall Score

The MVP uses this weighted formula:

```text
overall_score =
  0.30 * semantic_similarity_score +
  0.25 * backtranslation_similarity_score +
  0.15 * terminology_consistency_score +
  0.30 * llm_judge_score
```

The final value is rounded to one decimal place and clamped to `0-100`.

## Human Review Heuristics

The implementation flags items for review when any of these conditions hold:

- `overall_score < 80`
- `llm_judge_score < 75`
- `terminology_consistency_score < 100`
- `judge_needs_human_review = true`

The final `needs_human_review` flag is true when `review_reasons` is non-empty after merging the score-based rules with the LLM judge flag.

## Golden Example Layer

The curated or future-curated golden assets live under `docs/golden/` and currently preserve:

- `words.json`
- `sentences.json`
- `paragraphs.json`

Each record includes:

- `source_en`
- `bad_ko`
- `improved_ko`
- `notes`
- `tags`

Interpretation:

- `improved_ko` is the current curated Korean target for the golden example and functions as the reviewed golden text in lightweight regression checks.
- `bad_ko` is a contrastive example only. It is not a candidate run and not a golden target.
- These files are distinct from the page-level `reference_ko` used in the official document-pair MVP.

`run_golden_eval.py` provides a lightweight machine-readable evaluation path for these sets. It supports:

- generating fresh candidates from `source_en`
- loading an existing candidate file
- comparing either `candidate_ko` or an optional `improved_candidate_ko` field
- reporting Korean-side cosine similarity and optional backtranslation similarity

## Comparison Metadata

To make later comparisons easier without introducing a larger experiment framework, candidate and evaluation artifacts may include optional labels such as:

- `run_label`
- `pipeline_label`
- `prompt_label`
- `candidate_field`

These fields help compare multiple runs across models, prompts, and improvement pipelines while preserving the current Phase 1 MVP structure.

## Outputs

- pair snapshots: `docs/pairs/`
- aligned evaluation input: `data/processed/`
- scored results and markdown reports: `reports/`

## Relationship To Existing Assets

Existing files under `docs/golden/` and `evals/` remain in the repository. The curated files in `docs/golden/` now support the lightweight reviewed-golden evaluation layer, while `evals/` remains a preserved experimental or future-expansion path rather than the primary Phase 1 official document-pair flow.
