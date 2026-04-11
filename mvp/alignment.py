from __future__ import annotations

from pathlib import Path
import json

from mvp.text_utils import unit_type_from_tag


def load_snapshot_blocks(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    blocks = payload.get("blocks")
    if not isinstance(blocks, list):
        raise ValueError(f"{path} does not contain a valid 'blocks' array.")
    return blocks


def align_blocks(*, pair_slug: str, source_blocks: list[dict], reference_blocks: list[dict]) -> list[dict]:
    if len(source_blocks) != len(reference_blocks):
        raise ValueError(
            "Block counts do not match: "
            f"{len(source_blocks)} source blocks vs {len(reference_blocks)} reference blocks."
        )

    aligned = []
    for offset, (source_block, reference_block) in enumerate(zip(source_blocks, reference_blocks), start=1):
        source_tag = source_block["tag"]
        reference_tag = reference_block["tag"]
        if source_tag != reference_tag:
            raise ValueError(
                "Tag mismatch during alignment at block "
                f"{offset}: source={source_tag}, reference={reference_tag}"
            )

        aligned.append(
            {
                "id": f"{pair_slug}.block-{offset:03d}",
                "unit_type": unit_type_from_tag(source_tag),
                "source_en": source_block["clean_text"],
                "reference_ko": reference_block["clean_text"],
                "source_meta": {
                    "tag": source_tag,
                    "source_index": source_block["index"],
                    "reference_index": reference_block["index"],
                    "pair_slug": pair_slug,
                },
            }
        )

    return aligned
