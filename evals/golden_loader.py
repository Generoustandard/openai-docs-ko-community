from __future__ import annotations

import json
from pathlib import Path


DATA_FILES = ("words.json", "sentences.json", "paragraphs.json")
REQUIRED_FIELDS = {"id", "source_en", "bad_ko", "improved_ko", "notes", "tags"}


def _resolve_golden_dir(base_dir: str | Path) -> Path:
    base_path = Path(base_dir)
    nested_dir = base_path / "docs" / "golden"
    if nested_dir.is_dir():
        return nested_dir
    return base_path


def _load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a top-level JSON array.")
    return data


def _validate_record(record: dict, path: Path, index: int) -> None:
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        raise ValueError(f"{path} record #{index} is missing required fields: {missing}")
    if not isinstance(record["bad_ko"], str):
        raise ValueError(f"{path} record #{index} must use a string for 'bad_ko'.")
    if not isinstance(record["improved_ko"], str):
        raise ValueError(f"{path} record #{index} must use a string for 'improved_ko'.")
    if not isinstance(record["notes"], list) or not all(isinstance(note, str) for note in record["notes"]):
        raise ValueError(f"{path} record #{index} must use a list of strings for 'notes'.")
    if not isinstance(record["tags"], list) or not all(isinstance(tag, str) for tag in record["tags"]):
        raise ValueError(f"{path} record #{index} must use a list of strings for 'tags'.")


def load_goldens(base_dir: str | Path) -> dict[str, list[dict]]:
    golden_dir = _resolve_golden_dir(base_dir)
    loaded: dict[str, list[dict]] = {}

    for file_name in DATA_FILES:
        path = golden_dir / file_name
        records = _load_json(path)
        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                raise ValueError(f"{path} record #{index} must be a JSON object.")
            _validate_record(record, path, index)
        loaded[path.stem] = records

    return loaded


if __name__ == "__main__":
    goldens = load_goldens(Path(__file__).resolve().parents[1])
    for name, records in goldens.items():
        print(f"{name}: {len(records)} records")
