from __future__ import annotations

import argparse
import json
from pathlib import Path

from metrics import (
    candidate_vs_golden_similarity,
    source_vs_backtranslation_similarity,
)


REQUIRED_FIELDS = {
    "id",
    "source_en",
    "candidate_ko",
    "golden_ko",
    "backtranslated_en",
    "candidate_ko_embedding",
    "golden_ko_embedding",
    "source_en_embedding",
    "backtranslated_en_embedding",
}


def _load_input(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError("Input file must contain a top-level JSON array.")
    return payload


def _validate_record(record: dict, index: int) -> None:
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        raise ValueError(f"Record #{index} is missing required fields: {missing}")


def _score_record(record: dict) -> dict:
    candidate_score = candidate_vs_golden_similarity(
        record["candidate_ko_embedding"],
        record["golden_ko_embedding"],
    )
    backtranslation_score = source_vs_backtranslation_similarity(
        record["source_en_embedding"],
        record["backtranslated_en_embedding"],
    )

    return {
        "id": record["id"],
        "candidate_vs_golden_cosine": round(candidate_score, 6),
        "source_vs_backtranslation_cosine": round(backtranslation_score, 6),
    }


def _build_summary(scored_records: list[dict]) -> dict:
    count = len(scored_records)
    if count == 0:
        return {
            "count": 0,
            "average_candidate_vs_golden_cosine": 0.0,
            "average_source_vs_backtranslation_cosine": 0.0,
        }

    avg_candidate = sum(item["candidate_vs_golden_cosine"] for item in scored_records) / count
    avg_backtranslation = sum(item["source_vs_backtranslation_cosine"] for item in scored_records) / count
    return {
        "count": count,
        "average_candidate_vs_golden_cosine": round(avg_candidate, 6),
        "average_source_vs_backtranslation_cosine": round(avg_backtranslation, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute two lightweight cosine-based translation quality signals.",
    )
    parser.add_argument("input_path", help="Path to the precomputed eval input JSON file.")
    parser.add_argument("output_path", help="Path to write the JSON results.")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    records = _load_input(input_path)
    scored_records = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record #{index} must be a JSON object.")
        _validate_record(record, index)
        scored_records.append(_score_record(record))

    results = {
        "records": scored_records,
        "summary": _build_summary(scored_records),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"Wrote {len(scored_records)} results to {output_path}")


if __name__ == "__main__":
    main()
