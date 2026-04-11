from __future__ import annotations

import argparse
from pathlib import Path

from mvp.openai_utils import build_client, chunked, invoke_json_model, load_records_payload, save_json, utc_timestamp


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="정렬된 영어 원문 블록에서 후보 한국어 번역을 생성합니다.",
    )
    parser.add_argument("--input", required=True, help="`align_units.py`가 만든 정렬 입력 JSON 경로.")
    parser.add_argument(
        "--output",
        default=None,
        help="출력 경로. 기본값은 `data/processed/<input-stem>.candidates.json`입니다.",
    )
    parser.add_argument(
        "--model",
        default="gpt-5.4-mini",
        help="번역에 사용할 OpenAI 모델.",
    )
    parser.add_argument("--batch-size", type=int, default=8, help="한 요청에서 번역할 블록 수.")
    parser.add_argument("--run-label", default=None, help="여러 생성 실행을 비교하기 위한 optional label.")
    parser.add_argument("--pipeline-label", default=None, help="생성 파이프라인을 구분하기 위한 optional label.")
    parser.add_argument(
        "--prompt-label",
        default=DEFAULT_PROMPT_LABEL,
        help="번역 프롬프트 또는 프롬프트 계열을 구분하기 위한 optional label.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    meta, records = load_records_payload(input_path)
    client = build_client()

    instructions = (
        "Translate each English block into Korean for an official OpenAI-style document. "
        "Preserve benchmark names, product names, inline code, numbers, percentages, and factual meaning. "
        "Keep the tone natural, concise, and publication-ready. "
        "Return only the requested JSON schema."
    )

    translated_by_id: dict[str, str] = {}
    for batch in chunked(records, args.batch_size):
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
            model=args.model,
            instructions=instructions,
            payload=payload,
            schema_name="candidate_translation_batch",
            schema=TRANSLATION_SCHEMA,
            max_output_tokens=6000,
        )
        for item in result["translations"]:
            translated_by_id[item["id"]] = item["candidate_ko"].strip()

    enriched_records = []
    for record in records:
        candidate = translated_by_id.get(record["id"])
        if not candidate:
            raise ValueError(f"Missing candidate translation for {record['id']}")
        enriched_record = dict(record)
        enriched_record["candidate_ko"] = candidate
        enriched_records.append(enriched_record)

    output_path = Path(args.output or f"data/processed/{input_path.stem}.candidates.json")
    save_json(
        output_path,
        {
            **meta,
            "generated_at": utc_timestamp(),
            "generation_model": args.model,
            "run_label": args.run_label,
            "pipeline_label": args.pipeline_label,
            "prompt_label": args.prompt_label,
            "records": enriched_records,
        },
    )
    print(f"{len(enriched_records)}개의 candidate 번역을 {output_path}에 저장했습니다.")


if __name__ == "__main__":
    main()
