from __future__ import annotations

import argparse
import json
from pathlib import Path

from mvp.alignment import align_blocks, load_snapshot_blocks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Align extracted English and Korean article blocks into evaluation units.",
    )
    parser.add_argument("--slug", required=True, help="Stable pair slug used in IDs.")
    parser.add_argument(
        "--pair-dir",
        default="docs/pairs",
        help="Directory that contains pair snapshots created by collect_pair.py.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the aligned JSON output. Defaults to data/processed/<slug>.aligned.json",
    )
    args = parser.parse_args()

    pair_root = Path(args.pair_dir) / args.slug
    source_blocks = load_snapshot_blocks(pair_root / "source_en.blocks.json")
    reference_blocks = load_snapshot_blocks(pair_root / "reference_ko.blocks.json")
    aligned = align_blocks(
        pair_slug=args.slug,
        source_blocks=source_blocks,
        reference_blocks=reference_blocks,
    )

    output_path = Path(args.output or f"data/processed/{args.slug}.aligned.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(aligned, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"Wrote {len(aligned)} aligned units to {output_path}")


if __name__ == "__main__":
    main()
