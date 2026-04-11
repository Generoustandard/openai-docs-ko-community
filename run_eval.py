from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from mvp.openai_utils import build_client, chunked, invoke_json_model, load_records_payload, save_json, utc_timestamp
from mvp.scoring import compute_overall_score, cosine_similarity, cosine_to_score, review_reasons, score_terminology


BACKTRANSLATION_SCHEMA = {
    "type": "object",
    "properties": {
        "backtranslations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "backtranslated_en": {"type": "string"},
                },
                "required": ["id", "backtranslated_en"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["backtranslations"],
    "additionalProperties": False,
}


JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "judgments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "llm_judge_score": {"type": "number"},
                    "issues": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "needs_human_review": {"type": "boolean"},
                    "suggested_revision": {"type": "string"},
                },
                "required": ["id", "llm_judge_score", "issues", "needs_human_review", "suggested_revision"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["judgments"],
    "additionalProperties": False,
}


POSITIVE_ISSUE_PATTERNS = (
    "translation is accurate",
    "no significant issues",
    "terminology and style are consistent",
    "terminology consistent otherwise",
    "translation is strong",
)


def _candidate_text(record: dict, candidate_field: str) -> str:
    candidate = record.get(candidate_field)
    if not candidate or not isinstance(candidate, str):
        raise ValueError(f"Missing string field '{candidate_field}' for {record.get('id', 'unknown-record')}")
    return candidate


def _create_embeddings(client, model: str, texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def _backfill_missing_backtranslations(
    client,
    *,
    model: str,
    instructions: str,
    batch: list[dict],
    backtranslated_by_id: dict[str, str],
    max_attempts: int = 3,
) -> None:
    requested_ids = {record["id"] for record in batch}
    missing_ids = requested_ids - backtranslated_by_id.keys()
    attempts = 0

    while missing_ids and attempts < max_attempts:
        payload = {
            "items": [
                {
                    "id": record["id"],
                    "candidate_ko": record["candidate_ko"],
                }
                for record in batch
                if record["id"] in missing_ids
            ]
        }
        result = invoke_json_model(
            client,
            model=model,
            instructions=instructions,
            payload=payload,
            schema_name="backtranslation_retry_batch",
            schema=BACKTRANSLATION_SCHEMA,
            max_output_tokens=5000,
        )
        for item in result["backtranslations"]:
            item_id = item["id"]
            if item_id in missing_ids:
                backtranslated_by_id[item_id] = item["backtranslated_en"].strip()
        missing_ids = requested_ids - backtranslated_by_id.keys()
        attempts += 1

    if missing_ids:
        raise ValueError(f"Missing backtranslations after retries: {sorted(missing_ids)}")


def _backfill_missing_judgments(
    client,
    *,
    model: str,
    instructions: str,
    batch: list[dict],
    backtranslated_by_id: dict[str, str],
    judgments_by_id: dict[str, dict],
    max_attempts: int = 3,
) -> None:
    requested_ids = {record["id"] for record in batch}
    missing_ids = requested_ids - judgments_by_id.keys()
    attempts = 0

    while missing_ids and attempts < max_attempts:
        payload = {
            "items": [
                {
                    "id": record["id"],
                    "source_en": record["source_en"],
                    "reference_ko": record["reference_ko"],
                    "candidate_ko": record["candidate_ko"],
                    "backtranslated_en": backtranslated_by_id[record["id"]],
                }
                for record in batch
                if record["id"] in missing_ids
            ]
        }
        result = invoke_json_model(
            client,
            model=model,
            instructions=instructions,
            payload=payload,
            schema_name="llm_judge_retry_batch",
            schema=JUDGE_SCHEMA,
            max_output_tokens=7000,
        )
        for item in result["judgments"]:
            item_id = item["id"]
            if item_id in missing_ids:
                judgments_by_id[item_id] = item
        missing_ids = requested_ids - judgments_by_id.keys()
        attempts += 1

    if missing_ids:
        raise ValueError(f"Missing LLM judgments after retries: {sorted(missing_ids)}")


def _filter_issues(issues: list[str]) -> list[str]:
    filtered = []
    for issue in issues:
        normalized = issue.strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if any(lowered.startswith(pattern) for pattern in POSITIVE_ISSUE_PATTERNS):
            continue
        filtered.append(normalized)
    return list(dict.fromkeys(filtered))


def _build_summary(records: list[dict]) -> dict:
    count = len(records)
    if count == 0:
        return {
            "count": 0,
            "average_semantic_similarity_score": 0.0,
            "average_backtranslation_similarity_score": 0.0,
            "average_terminology_consistency_score": 0.0,
            "average_llm_judge_score": 0.0,
            "average_overall_score": 0.0,
            "human_review_count": 0,
        }

    def average(field: str) -> float:
        return round(sum(record[field] for record in records) / count, 1)

    issue_counter = Counter(issue for record in records for issue in record["issues"])
    return {
        "count": count,
        "average_semantic_similarity_score": average("semantic_similarity_score"),
        "average_backtranslation_similarity_score": average("backtranslation_similarity_score"),
        "average_terminology_consistency_score": average("terminology_consistency_score"),
        "average_llm_judge_score": average("llm_judge_score"),
        "average_overall_score": average("overall_score"),
        "human_review_count": sum(1 for record in records if record["needs_human_review"]),
        "top_issue_counts": issue_counter.most_common(10),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the official document-pair evaluation pipeline on generated candidate translations.",
    )
    parser.add_argument("--input", required=True, help="Candidate JSON created by generate_candidate.py.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output path. Defaults to reports/<input-stem>.eval.json",
    )
    parser.add_argument("--backtranslation-model", default="gpt-5.4-mini")
    parser.add_argument("--judge-model", default="gpt-5.4-mini")
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument(
        "--candidate-field",
        default="candidate_ko",
        help="Record field to evaluate. Use `improved_candidate_ko` for a follow-up improvement pass.",
    )
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--judge-batch-size", type=int, default=5)
    parser.add_argument("--run-label", default=None, help="Optional label for comparing evaluation runs.")
    parser.add_argument("--pipeline-label", default=None, help="Optional label for the evaluated pipeline.")
    parser.add_argument("--prompt-label", default=None, help="Optional label for the prompt family.")
    args = parser.parse_args()

    input_path = Path(args.input)
    meta, records = load_records_payload(input_path)
    client = build_client()

    backtranslation_instructions = (
        "Translate each Korean block back into concise, faithful English for semantic comparison. "
        "Preserve benchmark names, product names, numbers, and inline code. "
        "Return only the requested JSON schema."
    )
    backtranslated_by_id: dict[str, str] = {}
    for batch in chunked(records, args.batch_size):
        payload = {
            "items": [
                {
                    "id": record["id"],
                    "candidate_ko": _candidate_text(record, args.candidate_field),
                }
                for record in batch
            ]
        }
        result = invoke_json_model(
            client,
            model=args.backtranslation_model,
            instructions=backtranslation_instructions,
            payload=payload,
            schema_name="backtranslation_batch",
            schema=BACKTRANSLATION_SCHEMA,
            max_output_tokens=5000,
        )
        for item in result["backtranslations"]:
            backtranslated_by_id[item["id"]] = item["backtranslated_en"].strip()
        _backfill_missing_backtranslations(
            client,
            model=args.backtranslation_model,
            instructions=backtranslation_instructions,
            batch=batch,
            backtranslated_by_id=backtranslated_by_id,
        )

    judge_instructions = (
        "You are evaluating Korean technical translations for an official OpenAI-style publication. "
        "For each item, compare source_en, reference_ko, candidate_ko, and backtranslated_en. "
        "Assign one llm_judge_score on a 0-100 scale using this rubric: accuracy 40, naturalness 20, terminology consistency 20, style fit 20. "
        "Return at most 3 concise issues. "
        "Set needs_human_review to true only if the item contains a high-severity wording, terminology, or accuracy problem that should be manually reviewed. "
        "Set needs_human_review to false for minor style nits or acceptable alternatives. "
        "Return suggested_revision in Korean. If the candidate is already strong, suggested_revision may equal candidate_ko. "
        "Return only the requested JSON schema."
    )
    judgments_by_id: dict[str, dict] = {}
    for batch in chunked(records, args.judge_batch_size):
        payload = {
            "items": [
                {
                    "id": record["id"],
                    "source_en": record["source_en"],
                    "reference_ko": record["reference_ko"],
                    "candidate_ko": _candidate_text(record, args.candidate_field),
                    "backtranslated_en": backtranslated_by_id[record["id"]],
                }
                for record in batch
            ]
        }
        result = invoke_json_model(
            client,
            model=args.judge_model,
            instructions=judge_instructions,
            payload=payload,
            schema_name="llm_judge_batch",
            schema=JUDGE_SCHEMA,
            max_output_tokens=7000,
        )
        for item in result["judgments"]:
            judgments_by_id[item["id"]] = item
        _backfill_missing_judgments(
            client,
            model=args.judge_model,
            instructions=judge_instructions,
            batch=batch,
            backtranslated_by_id=backtranslated_by_id,
            judgments_by_id=judgments_by_id,
        )

    source_embeddings = _create_embeddings(client, args.embedding_model, [record["source_en"] for record in records])
    reference_embeddings = _create_embeddings(client, args.embedding_model, [record["reference_ko"] for record in records])
    candidate_embeddings = _create_embeddings(
        client,
        args.embedding_model,
        [_candidate_text(record, args.candidate_field) for record in records],
    )
    backtranslated_embeddings = _create_embeddings(
        client,
        args.embedding_model,
        [backtranslated_by_id[record["id"]] for record in records],
    )

    evaluated_records = []
    for index, record in enumerate(records):
        candidate_text = _candidate_text(record, args.candidate_field)
        semantic_cosine = cosine_similarity(reference_embeddings[index], candidate_embeddings[index])
        backtranslation_cosine = cosine_similarity(source_embeddings[index], backtranslated_embeddings[index])
        terminology_score, terminology_issues, terminology_details = score_terminology(
            source_en=record["source_en"],
            candidate_ko=candidate_text,
        )

        judgment = judgments_by_id.get(record["id"])
        if not judgment:
            raise ValueError(f"Missing LLM judgment for {record['id']}")

        merged = {
            "id": record["id"],
            "source_en": record["source_en"],
            "reference_ko": record["reference_ko"],
            "candidate_ko": candidate_text,
            "backtranslated_en": backtranslated_by_id[record["id"]],
            "semantic_similarity_score": cosine_to_score(semantic_cosine),
            "backtranslation_similarity_score": cosine_to_score(backtranslation_cosine),
            "terminology_consistency_score": terminology_score,
            "llm_judge_score": round(max(0.0, min(100.0, float(judgment["llm_judge_score"]))), 1),
            "issues": [],
            "judge_needs_human_review": bool(judgment["needs_human_review"]),
            "suggested_revision": judgment["suggested_revision"].strip(),
            "metadata": {
                "unit_type": record.get("unit_type"),
                "tag": record.get("source_meta", {}).get("tag"),
                "pair_slug": record.get("source_meta", {}).get("pair_slug"),
                "candidate_source_field": args.candidate_field,
                "terminology_details": terminology_details,
            },
        }
        merged["issues"] = _filter_issues(
            terminology_issues + [issue.strip() for issue in judgment["issues"] if issue.strip()]
        )
        merged["overall_score"] = compute_overall_score(merged)
        merged["review_reasons"] = review_reasons(merged)
        if merged["judge_needs_human_review"]:
            merged["review_reasons"].append("llm_judge_flagged")
        merged["review_reasons"] = list(dict.fromkeys(merged["review_reasons"]))
        merged["needs_human_review"] = bool(merged["review_reasons"])
        evaluated_records.append(merged)

    output_path = Path(args.output or f"reports/{input_path.stem}.eval.json")
    output_meta = dict(meta)
    if args.run_label:
        output_meta["run_label"] = args.run_label
    if args.pipeline_label:
        output_meta["pipeline_label"] = args.pipeline_label
    if args.prompt_label:
        output_meta["prompt_label"] = args.prompt_label
    save_json(
        output_path,
        {
            **output_meta,
            "evaluated_at": utc_timestamp(),
            "config": {
                "candidate_field": args.candidate_field,
                "backtranslation_model": args.backtranslation_model,
                "judge_model": args.judge_model,
                "embedding_model": args.embedding_model,
                "score_scale": "0-100",
                "overall_formula": (
                    "0.30 * semantic_similarity_score + "
                    "0.25 * backtranslation_similarity_score + "
                    "0.15 * terminology_consistency_score + "
                    "0.30 * llm_judge_score"
                ),
            },
            "summary": _build_summary(evaluated_records),
            "records": evaluated_records,
        },
    )

    print(f"Wrote {len(evaluated_records)} evaluation records to {output_path}")


if __name__ == "__main__":
    main()
