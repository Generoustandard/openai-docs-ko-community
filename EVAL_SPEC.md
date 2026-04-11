# Evaluation Spec

## Phase

This specification defines the Phase 1 MVP for evaluating an official OpenAI English-Korean document pair.

## Unit Choice

The MVP uses paragraph-level alignment.

In practice, an evaluation unit is a stable prose block extracted from the article body:

- paragraph blocks (`p`)
- list items (`li`)
- section headers (`h2` to `h4`)

Code blocks and diffs are excluded from the first-pass evaluation dataset because they are primarily source-preservation artifacts, not Korean translation quality signals.

## Core Roles

- `source_en`: official English source block
- `reference_ko`: official Korean reference block published on `openai.com`
- `candidate_ko`: new Korean translation generated from `source_en`
- `backtranslated_en`: English text translated back from `candidate_ko`

## Input Schema

The aligned evaluation input stored under `data/processed/` uses this shape:

```json
[
  {
    "id": "why-we-no-longer-evaluate-swe-bench-verified.block-001",
    "unit_type": "paragraph",
    "source_en": "English source block",
    "reference_ko": "Official Korean reference block",
    "source_meta": {
      "tag": "P",
      "pair_slug": "why-we-no-longer-evaluate-swe-bench-verified"
    }
  }
]
```

## Evaluation Output Schema

Each evaluated item must include:

```json
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
  "suggested_revision": "벤치마크라는 표현을 유지하고 ...",
  "metadata": {
    "unit_type": "paragraph",
    "tag": "P"
  }
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

Rule-based score over a small glossary of document-critical terms.

The MVP starts with explicit checks for terms such as:

- `SWE-bench Verified`
- `SWE-bench Pro`
- `frontier`
- `benchmark`
- `contamination`
- `gold patch`
- `Preparedness Framework`

The score is based on how consistently the candidate preserves or translates the required terms compared with the glossary rule and the reference phrasing.

### `llm_judge_score`

LLM-judged score on a `0-100` scale based on:

- accuracy
- naturalness
- terminology consistency
- document style fit

The judge also returns:

- `issues`
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

## Review Heuristics

The report should flag items for human review when any of these conditions hold:

- `overall_score < 80`
- `llm_judge_score < 75`
- `terminology_consistency_score < 100`
- `issues` is non-empty and includes a high-severity wording or accuracy concern

## Outputs

- pair snapshots: `docs/pairs/`
- aligned evaluation input: `data/processed/`
- scored results and markdown reports: `reports/`

## Relationship To Existing Assets

Existing files under `docs/golden/` and `evals/` remain valid as experimental or future-expansion assets. They are not the primary path for this Phase 1 official document-pair MVP.
