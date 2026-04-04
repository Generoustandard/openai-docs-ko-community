from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI


def build_client() -> "OpenAI":
    from openai import OpenAI

    return OpenAI()


def chunked(items: list[dict], size: int) -> Iterable[list[dict]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def load_records_payload(path: Path) -> tuple[dict, list[dict]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, list):
        return {}, payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        meta = {key: value for key, value in payload.items() if key != "records"}
        return meta, payload["records"]
    raise ValueError(f"{path} must contain a top-level list or an object with a 'records' array.")


def save_json(path: Path, payload: dict | list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def invoke_json_model(
    client: OpenAI,
    *,
    model: str,
    instructions: str,
    payload: dict,
    schema_name: str,
    schema: dict,
    max_output_tokens: int | None = None,
) -> dict:
    request = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": instructions}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": json.dumps(payload, ensure_ascii=False)}],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "schema": schema,
                "strict": True,
            }
        },
    }
    if max_output_tokens is not None:
        request["max_output_tokens"] = max_output_tokens

    response = client.responses.create(**request)
    return json.loads(response.output_text)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
