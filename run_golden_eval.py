from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from evals.golden_loader import load_goldens
from mvp.openai_utils import build_client, chunked, invoke_json_model, load_records_payload, save_json, utc_timestamp
from mvp.scoring import cosine_similarity, cosine_to_score


DEFAULT_PROMPT_LABEL = "official_openai_style_translation_v1"


TRANSLATION_SCHEMA = {
    "type": "object",
    "properties": {
        "translations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "candidate_ko": {"type": "string"},
                },
                "required": ["id", "candidate_ko"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["translations"],
    "additionalProperties": False,
}


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


UNIT_LEVELS = {
    "words": "word",
    "sentences": "sentence",
    "paragraphs": "paragraph",
}
REVIEW_TARGET_ROLE = "reviewed_golden_candidate"


def _create_embeddings(client, model: str, texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def _select_review_targets(records: list[dict], *, golden_set: str) -> tuple[list[dict], int]:
    selected = [record for record in records if record.get("target_role") == REVIEW_TARGET_ROLE]
    if not selected:
        raise ValueError(
            f"{golden_set} does not contain any records marked as '{REVIEW_TARGET_ROLE}'. "
            "Mark a small reviewed subset before running golden evaluation."
        )
    return selected, len(records) - len(selected)


def _retry_missing_backtranslations(
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
            schema_name="golden_backtranslation_retry_batch",
            schema=BACKTRANSLATION_SCHEMA,
            max_output_tokens=4000,
        )
        for item in result["backtranslations"]:
            item_id = item["id"]
            if item_id in missing_ids:
                backtranslated_by_id[item_id] = item["backtranslated_en"].strip()
        missing_ids = requested_ids - backtranslated_by_id.keys()
        attempts += 1

    if missing_ids:
        raise ValueError(f"Missing golden backtranslations after retries: {sorted(missing_ids)}")


def _generate_candidates(
    client,
    *,
    model: str,
    records: list[dict],
    batch_size: int,
) -> dict[str, str]:
    instructions = (
        "Translate each English block into Korean for an official OpenAI-style document. "
        "Preserve product names, benchmark names, inline code, and factual meaning. "
        "Keep the Korean natural, concise, and publication-ready. "
        "Return only the requested JSON schema."
    )
    candidates_by_id: dict[str, str] = {}

    for batch in chunked(records, batch_size):
        payload = {
            "items": [
                {
                    "id": record["id"],
                    "source_en": record["source_en"],
                }
                for record in batch
            ]
        }
        result = invoke_json_model(
            client,
            model=model,
            instructions=instructions,
            payload=payload,
            schema_name="golden_candidate_batch",
            schema=TRANSLATION_SCHEMA,
            max_output_tokens=5000,
        )
        for item in result["translations"]:
            candidates_by_id[item["id"]] = item["candidate_ko"].strip()

    missing_ids = {record["id"] for record in records} - candidates_by_id.keys()
    if missing_ids:
        raise ValueError(f"Missing generated candidates for golden set: {sorted(missing_ids)}")
    return candidates_by_id


def _build_summary(records: list[dict], *, include_backtranslation: bool) -> dict:
    count = len(records)
    if count == 0:
        return {
            "count": 0,
            "average_candidate_vs_reviewed_golden_score": 0.0,
            "average_source_vs_backtranslation_score": None if not include_backtranslation else 0.0,
            "top_tags": [],
        }

    candidate_average = round(sum(record["candidate_vs_reviewed_golden_score"] for record in records) / count, 1)
    if include_backtranslation:
        backtranslation_average = round(sum(record["source_vs_backtranslation_score"] for record in records) / count, 1)
    else:
        backtranslation_average = None

    tag_counter = Counter(tag for record in records for tag in record.get("tags", []))
    return {
        "count": count,
        "average_candidate_vs_reviewed_golden_score": candidate_average,
        "average_source_vs_backtranslation_score": backtranslation_average,
        "top_tags": tag_counter.most_common(10),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="각 golden 파일에서 reviewed_golden_candidate로 표시된 항목만 대상으로 경량 평가를 실행합니다.",
    )
    parser.add_argument("--golden-set", required=True, choices=sorted(UNIT_LEVELS))
    parser.add_argument(
        "--input",
        default=None,
        help="matching id를 가진 optional candidate JSON 경로. 생략하면 선택된 review target의 `source_en`에서 새 candidate를 생성합니다.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="출력 경로. 기본값은 `reports/golden.<golden-set>.eval.json`입니다.",
    )
    parser.add_argument(
        "--candidate-field",
        default="candidate_ko",
        help="`--input`에서 읽을 field. 후속 개선안을 평가할 때는 `improved_candidate_ko`를 사용합니다.",
    )
    parser.add_argument("--generation-model", default="gpt-5.4-mini")
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--backtranslation-model", default="gpt-5.4-mini")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--skip-backtranslation", action="store_true", help="backtranslation 유사도 계산을 건너뜁니다.")
    parser.add_argument("--run-label", default=None, help="여러 golden 평가 실행을 비교하기 위한 optional label.")
    parser.add_argument("--pipeline-label", default=None, help="평가 대상 파이프라인을 구분하기 위한 optional label.")
    parser.add_argument("--prompt-label", default=DEFAULT_PROMPT_LABEL, help="프롬프트 계열을 구분하기 위한 optional label.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    golden_pool = load_goldens(repo_root)[args.golden_set]
    golden_records, example_only_count = _select_review_targets(golden_pool, golden_set=args.golden_set)
    client = build_client()

    input_meta: dict = {}
    candidates_by_id: dict[str, str]
    source_mode: str

    if args.input:
        input_meta, candidate_records = load_records_payload(Path(args.input))
        indexed_records = {record["id"]: record for record in candidate_records}
        candidates_by_id = {}
        for golden_record in golden_records:
            candidate_record = indexed_records.get(golden_record["id"])
            if not candidate_record:
                raise ValueError(f"Missing golden candidate input for {golden_record['id']}")
            candidate_text = candidate_record.get(args.candidate_field)
            if not isinstance(candidate_text, str) or not candidate_text.strip():
                raise ValueError(f"Missing string field '{args.candidate_field}' for {golden_record['id']}")
            candidates_by_id[golden_record["id"]] = candidate_text.strip()
        source_mode = "input_candidates"
    else:
        candidates_by_id = _generate_candidates(
            client,
            model=args.generation_model,
            records=golden_records,
            batch_size=args.batch_size,
        )
        source_mode = "generated_from_source_en"

    normalized_records = []
    for golden_record in golden_records:
        normalized_records.append(
            {
                "id": golden_record["id"],
                "source_en": golden_record["source_en"],
                "reviewed_golden_ko": golden_record["improved_ko"],
                "candidate_ko": candidates_by_id[golden_record["id"]],
                "notes": golden_record["notes"],
                "tags": golden_record["tags"],
                "target_role": golden_record["target_role"],
                "review_status": golden_record["review_status"],
            }
        )

    candidate_embeddings = _create_embeddings(client, args.embedding_model, [record["candidate_ko"] for record in normalized_records])
    golden_embeddings = _create_embeddings(
        client,
        args.embedding_model,
        [record["reviewed_golden_ko"] for record in normalized_records],
    )

    backtranslated_by_id: dict[str, str] = {}
    if not args.skip_backtranslation:
        backtranslation_instructions = (
            "Translate each Korean block back into concise, faithful English for semantic comparison. "
            "Preserve product names, benchmark names, numbers, and inline code. "
            "Return only the requested JSON schema."
        )
        for batch in chunked(normalized_records, args.batch_size):
            payload = {
                "items": [
                    {
                        "id": record["id"],
                        "candidate_ko": record["candidate_ko"],
                    }
                    for record in batch
                ]
            }
            result = invoke_json_model(
                client,
                model=args.backtranslation_model,
                instructions=backtranslation_instructions,
                payload=payload,
                schema_name="golden_backtranslation_batch",
                schema=BACKTRANSLATION_SCHEMA,
                max_output_tokens=4000,
            )
            for item in result["backtranslations"]:
                backtranslated_by_id[item["id"]] = item["backtranslated_en"].strip()
            _retry_missing_backtranslations(
                client,
                model=args.backtranslation_model,
                instructions=backtranslation_instructions,
                batch=batch,
                backtranslated_by_id=backtranslated_by_id,
            )

        source_embeddings = _create_embeddings(client, args.embedding_model, [record["source_en"] for record in normalized_records])
        backtranslated_embeddings = _create_embeddings(
            client,
            args.embedding_model,
            [backtranslated_by_id[record["id"]] for record in normalized_records],
        )
    else:
        source_embeddings = []
        backtranslated_embeddings = []

    evaluated_records = []
    for index, record in enumerate(normalized_records):
        evaluated_record = {
            "id": record["id"],
            "source_en": record["source_en"],
            "reviewed_golden_ko": record["reviewed_golden_ko"],
            "candidate_ko": record["candidate_ko"],
            "candidate_vs_reviewed_golden_score": cosine_to_score(
                cosine_similarity(candidate_embeddings[index], golden_embeddings[index])
            ),
            "notes": record["notes"],
            "tags": record["tags"],
            "target_role": record["target_role"],
            "review_status": record["review_status"],
        }
        if args.skip_backtranslation:
            evaluated_record["backtranslated_en"] = None
            evaluated_record["source_vs_backtranslation_score"] = None
        else:
            evaluated_record["backtranslated_en"] = backtranslated_by_id[record["id"]]
            evaluated_record["source_vs_backtranslation_score"] = cosine_to_score(
                cosine_similarity(source_embeddings[index], backtranslated_embeddings[index])
            )
        evaluated_records.append(evaluated_record)

    output_path = Path(args.output or f"reports/golden.{args.golden_set}.eval.json")
    output_meta = dict(input_meta)
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
            "golden_set": args.golden_set,
            "unit_level": UNIT_LEVELS[args.golden_set],
            "golden_target_field": "improved_ko",
            "evaluated_at": utc_timestamp(),
            "config": {
                "selection_rule": f"target_role={REVIEW_TARGET_ROLE}",
                "source_pool_count": len(golden_pool),
                "review_target_count": len(golden_records),
                "example_only_count": example_only_count,
                "source_mode": source_mode,
                "candidate_field": args.candidate_field,
                "generation_model": None if args.input else args.generation_model,
                "embedding_model": args.embedding_model,
                "backtranslation_model": None if args.skip_backtranslation else args.backtranslation_model,
            },
            "summary": _build_summary(evaluated_records, include_backtranslation=not args.skip_backtranslation),
            "records": evaluated_records,
        },
    )
    print(f"{len(evaluated_records)}개의 reviewed golden candidate 평가 결과를 {output_path}에 저장했습니다.")


if __name__ == "__main__":
    main()
