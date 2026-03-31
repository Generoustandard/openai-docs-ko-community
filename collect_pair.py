from __future__ import annotations

import argparse
import json
from pathlib import Path

from mvp.collection import EN_LOCALE, KO_LOCALE, fetch_page_snapshot


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect an official OpenAI English/Korean page pair and save snapshots.",
    )
    parser.add_argument("--slug", required=True, help="Stable pair slug used for output paths.")
    parser.add_argument("--source-url", required=True, help="Official English page URL.")
    parser.add_argument("--reference-url", required=True, help="Official Korean page URL.")
    parser.add_argument(
        "--output-dir",
        default="docs/pairs",
        help="Directory where pair snapshots will be stored.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Use headless Chrome. Headful mode is the default because some OpenAI pages are blocked in headless mode.",
    )
    args = parser.parse_args()

    pair_dir = Path(args.output_dir) / args.slug
    pair_dir.mkdir(parents=True, exist_ok=True)

    source_snapshot = fetch_page_snapshot(
        url=args.source_url,
        locale=EN_LOCALE,
        headless=args.headless,
    )
    reference_snapshot = fetch_page_snapshot(
        url=args.reference_url,
        locale=KO_LOCALE,
        headless=args.headless,
    )

    (pair_dir / "source_en.html").write_text(source_snapshot["html"], encoding="utf-8")
    (pair_dir / "reference_ko.html").write_text(reference_snapshot["html"], encoding="utf-8")
    (pair_dir / "source_en.txt").write_text(source_snapshot["article_text_clean"], encoding="utf-8")
    (pair_dir / "reference_ko.txt").write_text(reference_snapshot["article_text_clean"], encoding="utf-8")

    _write_json(pair_dir / "source_en.blocks.json", source_snapshot)
    _write_json(pair_dir / "reference_ko.blocks.json", reference_snapshot)
    _write_json(
        pair_dir / "pair_manifest.json",
        {
            "pair_slug": args.slug,
            "source_url": args.source_url,
            "reference_url": args.reference_url,
            "source_final_url": source_snapshot["final_url"],
            "reference_final_url": reference_snapshot["final_url"],
            "source_block_count": source_snapshot["block_count"],
            "reference_block_count": reference_snapshot["block_count"],
        },
    )

    print(f"Saved pair snapshot to {pair_dir}")


if __name__ == "__main__":
    main()
