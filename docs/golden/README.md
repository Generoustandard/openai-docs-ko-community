# Golden Example Sets

These files preserve a small set of curated English-Korean translation examples at three levels:

- `words.json`
- `sentences.json`
- `paragraphs.json`

They are used for lightweight regression checks and comparison runs. They are not the same thing as the official `reference_ko` page used in the Phase 1 document-pair MVP.

## Role In The Repository

- `reference_ko`: official Korean page reference for the current Phase 1 `openai.com` document-pair evaluation
- `reviewed_golden`: small curated or human-reviewed examples used for sanity checks, regression checks, and model or prompt comparison
- `candidate_ko`: raw LLM-generated translation under evaluation
- `improved_candidate_ko`: optional follow-up revision that can be re-evaluated later

## Record Shape

Each golden record keeps:

- `source_en`
- `bad_ko`
- `improved_ko`
- `notes`
- `tags`

For golden-set evaluation, treat `improved_ko` as the current reviewed golden target. It is distinct from both the official page-level `reference_ko` and any raw LLM-generated `candidate_ko`.

## Intended Use

- quick cosine-similarity checks between generated Korean and curated Korean
- optional backtranslation checks against the English source
- lightweight regression checks before or after changing models, prompts, or improvement pipelines

Use [run_golden_eval.py](../../run_golden_eval.py) to score these sets without changing the main Phase 1 document-pair flow.
