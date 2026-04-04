# Evaluation Spec

## Purpose

This specification defines the Phase 1 MVP for evaluating Korean translation quality on an official OpenAI English-Korean document pair.

## Scope

Phase 1 is limited to official `openai.com` page pairs with both:

- `source_en`: official English source text
- `reference_ko`: official Korean translation published by OpenAI

The evaluation pipeline generates:

- `candidate_ko`: a new Korean translation from `source_en`
- `backtranslated_en`: an English backtranslation of `candidate_ko`

`reviewed_golden` is outside the automated Phase 1 scoring loop. It is reserved for samples that have been manually reviewed and intentionally promoted later for regression testing or deeper evaluation.

Important constraints:

- `reference_ko` is a reference, not automatically golden.
- `candidate_ko` is never stored as golden.
- Only human-reviewed samples can become `reviewed_golden`.

## Unit Choice

The MVP uses paragraph-level alignment. In practice, each evaluation unit is a stable prose block extracted from the article body:

- paragraph blocks (`p`)
- list items (`li`)
- section headers (`h2` to `h3`)

Code blocks, diffs, and code-example captions are excluded from the first-pass evaluation dataset because they are primarily source-preservation artifacts, not Korean translation quality signals.

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

Embedding cosine similarity between `reference_ko` and `candidate_ko`, converted with:

```text
semantic_similarity_score = clamp(cosine_similarity(reference_ko, candidate_ko), 0, 1) * 100
```

### `backtranslation_similarity_score`

1. translate `candidate_ko` back into English to produce `backtranslated_en`
2. compute embedding cosine similarity between `source_en` and `backtranslated_en`
3. convert with:

```text
backtranslation_similarity_score = clamp(cosine_similarity(source_en, backtranslated_en), 0, 1) * 100
```

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

## Outputs

- pair snapshots: `docs/pairs/`
- aligned evaluation input: `data/processed/`
- scored results and markdown reports: `reports/`

## Relationship To Existing Assets

Existing files under `docs/golden/` and `evals/` remain valid as experimental or future-expansion assets. They are preserved for future work, but they are not the primary path for this Phase 1 official document-pair MVP.
