from __future__ import annotations

import argparse
from pathlib import Path

from mvp.openai_utils import build_client, chunked, invoke_json_model, load_records_payload, save_json, utc_timestamp


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
        description="Generate candidate Korean translations from aligned English source blocks.",
    )
    parser.add_argument("--input", required=True, help="Aligned input JSON created by align_units.py.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output path. Defaults to data/processed/<input-stem>.candidates.json",
    )
    parser.add_argument(
        "--model",
        default="gpt-4.1-mini",
        help="OpenAI model used for translation.",
    )
    parser.add_argument("--batch-size", type=int, default=8, help="Number of blocks translated per request.")
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
            "records": enriched_records,
        },
    )
    print(f"Wrote {len(enriched_records)} candidate translations to {output_path}")


if __name__ == "__main__":
    main()
