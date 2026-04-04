from __future__ import annotations

import argparse
from pathlib import Path

from mvp.openai_utils import load_records_payload


RECOMMENDED_MVP_MODEL = "gpt-5.4-mini"


def _format_top_items(records: list[dict], *, field: str, limit: int) -> str:
    lines = []
    for record in sorted(records, key=lambda item: item[field])[:limit]:
        field_fragment = f"{field}={record[field]:.1f}"
        if field == "overall_score":
            field_fragment = f"overall={record['overall_score']:.1f}"
        lines.append(
            f"- `{record['id']}` | {field_fragment}\n"
            f"  source: {record['source_en']}\n"
            f"  candidate: {record['candidate_ko']}\n"
            f"  issues: {', '.join(record['issues']) if record['issues'] else 'none'}"
        )
    return "\n".join(lines) if lines else "- none"


def _format_review_list(records: list[dict]) -> str:
    flagged = [record for record in records if record.get("needs_human_review")]
    if not flagged:
        return "- none"

    lines = []
    for record in flagged:
        reasons = ", ".join(record.get("review_reasons", [])) or "issues present"
        lines.append(
            f"- `{record['id']}` | overall={record['overall_score']:.1f} | reasons: {reasons}"
        )
    return "\n".join(lines)


def _format_provenance(meta: dict, config: dict) -> str:
    generation_model = meta.get("generation_model", "n/a")
    backtranslation_model = config.get("backtranslation_model", "n/a")
    judge_model = config.get("judge_model", "n/a")
    embedding_model = config.get("embedding_model", "n/a")
    generated_at = meta.get("generated_at", "n/a")
    evaluated_at = meta.get("evaluated_at", "n/a")

    lines = [
        f"- generated_at: `{generated_at}`",
        f"- evaluated_at: `{evaluated_at}`",
        f"- generation_model: `{generation_model}`",
        f"- backtranslation_model: `{backtranslation_model}`",
        f"- judge_model: `{judge_model}`",
        f"- embedding_model: `{embedding_model}`",
    ]

    recorded_models = [generation_model, backtranslation_model, judge_model]
    if any(model not in {"n/a", RECOMMENDED_MVP_MODEL} for model in recorded_models):
        lines.append("")
        lines.append(
            f"> Note: This report reflects a historical sample run. The current recommended MVP demo configuration uses `{RECOMMENDED_MVP_MODEL}` for generation, backtranslation, and judging."
        )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a human-readable markdown report from evaluation JSON.",
    )
    parser.add_argument("--input", required=True, help="Evaluation JSON created by run_eval.py.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output markdown path. Defaults to reports/<input-stem>.md",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    meta, records = load_records_payload(input_path)
    summary = meta.get("summary", {})
    config = meta.get("config", {})
    pair_slug = meta.get("pair_slug") or records[0].get("metadata", {}).get("pair_slug", "unknown-pair")

    terminology_mismatches = [record for record in records if record["terminology_consistency_score"] < 100]

    report = f"""# Translation Evaluation Report

## Pair

- pair_slug: `{pair_slug}`
- unit_count: {summary.get("count", len(records))}
- score_scale: `{config.get("score_scale", "0-100")}`
- overall_formula: `{config.get("overall_formula", "n/a")}`

## Artifact Provenance

{_format_provenance(meta, config)}

## Document Summary

- average_overall_score: {summary.get("average_overall_score", 0.0):.1f}
- average_semantic_similarity_score: {summary.get("average_semantic_similarity_score", 0.0):.1f}
- average_backtranslation_similarity_score: {summary.get("average_backtranslation_similarity_score", 0.0):.1f}
- average_terminology_consistency_score: {summary.get("average_terminology_consistency_score", 0.0):.1f}
- average_llm_judge_score: {summary.get("average_llm_judge_score", 0.0):.1f}
- human_review_count: {summary.get("human_review_count", 0)}

## Top 5 Problem Items

{_format_top_items(records, field="overall_score", limit=5)}

## Terminology Mismatch Examples

{_format_top_items(terminology_mismatches, field="terminology_consistency_score", limit=5)}

## Backtranslation Mismatch Examples

{_format_top_items(records, field="backtranslation_similarity_score", limit=5)}

## Human Review Queue

{_format_review_list(records)}
"""

    output_path = Path(args.output or f"reports/{input_path.stem}.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote markdown report to {output_path}")


if __name__ == "__main__":
    main()
