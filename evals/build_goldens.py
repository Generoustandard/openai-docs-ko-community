from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import time
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html import unescape
from pathlib import Path


DEFAULT_MODEL = "gpt-5-mini"
DEFAULT_URLS_PATH = Path("docs/inputs/urls.txt")
DEFAULT_MARKDOWN_DIR = Path("docs/inputs/md")
DEFAULT_GOLDEN_DIR = Path("docs/golden")
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
DOC_TIMEOUT_SECONDS = 30
OPENAI_TIMEOUT_SECONDS = 180
OPENAI_MAX_RETRIES = 3
NOISE_LINES = {
    "copy page",
    "copy pagemore page actions",
    "search docs",
    "start searching",
    "api dashboard",
    "compare",
    "try in playground",
}
WORD_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "s",
    "so",
    "that",
    "the",
    "their",
    "them",
    "they",
    "this",
    "to",
    "use",
    "using",
    "with",
    "you",
    "your",
}
BATCH_SIZES = {
    "words": 20,
    "sentences": 8,
    "paragraphs": 3,
}
MIN_WORD_LENGTH = 3


def _load_env(base_dir: Path) -> None:
    env_path = base_dir / ".env"
    if not env_path.is_file():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        value = value.strip().strip("'").strip('"')
        os.environ[key] = value


def _slugify(text: str, *, fallback: str = "item") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or fallback


def _read_urls(path: Path) -> list[str]:
    urls: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    if not urls:
        raise ValueError(f"{path} does not contain any URLs.")
    return urls


def _fetch_url_text(url: str, *, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex-Community-Docs-KR/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    ssl_context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout, context=ssl_context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def _strip_blocks(html: str) -> str:
    stripped = re.sub(r"(?is)<(script|style|svg|noscript|template).*?>.*?</\1>", "", html)
    return re.sub(r"(?is)<!--.*?-->", "", stripped)


def _extract_main_html(html: str) -> str:
    for pattern in (
        r"(?is)<main\b[^>]*>(.*?)</main>",
        r"(?is)<article\b[^>]*>(.*?)</article>",
        r"(?is)<body\b[^>]*>(.*?)</body>",
    ):
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return html


def _strip_tags(fragment: str) -> str:
    without_tags = re.sub(r"(?is)<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", unescape(without_tags)).strip()


def _strip_tags_preserving_newlines(fragment: str) -> str:
    without_tags = re.sub(r"(?is)<[^>]+>", "", fragment)
    without_carriage_returns = without_tags.replace("\r", "")
    collapsed_spaces = re.sub(r"[ \t\f\v]+", " ", without_carriage_returns)
    normalized = re.sub(r"\n{3,}", "\n\n", collapsed_spaces)
    return unescape(normalized).strip()


def _extract_title(html: str, url: str) -> str:
    match = re.search(r"(?is)<title\b[^>]*>(.*?)</title>", html)
    if match:
        title = _strip_tags(match.group(1))
        if title:
            return title
    parsed = urllib.parse.urlparse(url)
    return parsed.path.rstrip("/").split("/")[-1] or parsed.netloc


def _html_to_markdownish(html: str) -> str:
    body = _strip_blocks(_extract_main_html(html))
    body = re.sub(
        r"(?is)<pre\b[^>]*>\s*<code\b[^>]*>(.*?)</code>\s*</pre>",
        lambda match: "\n\n```text\n" + unescape(_strip_tags(match.group(1))) + "\n```\n\n",
        body,
    )
    body = re.sub(
        r"(?is)<h([1-6])\b[^>]*>(.*?)</h\1>",
        lambda match: "\n"
        + ("#" * int(match.group(1)))
        + " "
        + _strip_tags(match.group(2))
        + "\n",
        body,
    )
    body = re.sub(r"(?is)<li\b[^>]*>(.*?)</li>", lambda m: "\n- " + _strip_tags(m.group(1)) + "\n", body)
    body = re.sub(r"(?is)<br\s*/?>", "\n", body)
    body = re.sub(r"(?is)</(p|section|div|article|header|footer|aside|tr|table|ul|ol|blockquote)>", "\n\n", body)
    body = re.sub(r"(?is)<hr\b[^>]*>", "\n\n---\n\n", body)
    body = _strip_tags_preserving_newlines(body)

    lines = [line.strip() for line in body.splitlines()]
    filtered_lines: list[str] = []
    seen_title = False
    for line in lines:
        if not line:
            if filtered_lines and filtered_lines[-1] != "":
                filtered_lines.append("")
            continue

        folded = line.casefold()
        if folded in NOISE_LINES:
            continue
        if folded.startswith("was this page helpful"):
            break
        if not seen_title and line.startswith("# "):
            seen_title = True
        if not seen_title and len(line.split()) <= 2:
            continue
        filtered_lines.append(line)

    text = "\n".join(filtered_lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def _sentence_split(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'`])", normalized)
    return [part.strip() for part in parts if part.strip()]


def _extract_paragraphs(markdown_text: str) -> list[str]:
    paragraphs: list[str] = []

    for block in markdown_text.split("\n\n"):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        if lines[0].startswith("```"):
            continue

        cleaned_lines: list[str] = []
        for line in lines:
            if line.startswith("```"):
                continue
            if line.startswith("#"):
                continue
            if line.startswith("Source: "):
                continue
            if line.casefold() in NOISE_LINES:
                continue
            cleaned_lines.append(line.lstrip("- ").strip())

        paragraph = re.sub(r"\s+", " ", " ".join(cleaned_lines)).strip()
        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs


def _extract_sentences(paragraphs: list[str]) -> list[str]:
    sentences: list[str] = []
    seen: set[str] = set()
    for paragraph in paragraphs:
        for sentence in _sentence_split(paragraph):
            if sentence not in seen:
                seen.add(sentence)
                sentences.append(sentence)
    return sentences


def _extract_words(paragraphs: list[str]) -> list[str]:
    tokens: list[str] = []
    for paragraph in paragraphs:
        tokens.extend(re.findall(r"[A-Za-z][A-Za-z0-9+#/-]*(?:\.[A-Za-z0-9+#/-]+)*", paragraph))

    counts = Counter(token.lower() for token in tokens)
    canonical: dict[str, str] = {}
    for token in tokens:
        folded = token.lower()
        if folded not in canonical:
            canonical[folded] = token

    ranked_words = sorted(
        canonical,
        key=lambda word: (-counts[word], word),
    )

    words: list[str] = []
    for word in ranked_words:
        if len(word) < MIN_WORD_LENGTH or word in WORD_STOPWORDS:
            continue
        words.append(canonical[word])
    return words


def _build_word_records(doc_slug: str, words: list[str]) -> list[dict]:
    return [
        {
            "id": f"words.{doc_slug}.{index:03d}",
            "source_en": word,
        }
        for index, word in enumerate(words, start=1)
    ]


def _build_text_records(unit: str, doc_slug: str, items: list[str]) -> list[dict]:
    return [
        {
            "id": f"{unit}.{doc_slug}.{index:03d}",
            "source_en": item,
        }
        for index, item in enumerate(items, start=1)
    ]


def _chunked(items: list[dict], size: int) -> list[list[dict]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def _parse_json_payload(text: str) -> object:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _call_openai_chat(api_key: str, *, model: str, system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_CHAT_COMPLETIONS_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    ssl_context = ssl.create_default_context()
    last_error: Exception | None = None
    for attempt in range(1, OPENAI_MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=OPENAI_TIMEOUT_SECONDS, context=ssl_context) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code in {408, 409, 429, 500, 502, 503, 504} and attempt < OPENAI_MAX_RETRIES:
                last_error = exc
                time.sleep(attempt * 2)
                continue
            raise RuntimeError(f"OpenAI API request failed with HTTP {exc.code}: {body}") from exc
        except (TimeoutError, urllib.error.URLError) as exc:
            last_error = exc
            if attempt < OPENAI_MAX_RETRIES:
                time.sleep(attempt * 2)
                continue
            raise RuntimeError(f"OpenAI API request failed after retries: {exc}") from exc
    else:
        raise RuntimeError(f"OpenAI API request failed after retries: {last_error}")

    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"Unexpected OpenAI response shape: {payload}") from exc


def _translate_batch(
    api_key: str,
    *,
    model: str,
    title: str,
    url: str,
    unit: str,
    batch: list[dict],
) -> list[dict]:
    system_prompt = textwrap.dedent(
        """
        You are building a Korean golden translation set for technical docs.
        Return strict JSON with the shape:
        {
          "items": [
            {
              "id": "...",
              "bad_ko": "...",
              "improved_ko": "...",
              "notes": ["...", "..."],
              "tags": ["...", "..."]
            }
          ]
        }

        Rules:
        - Preserve technical accuracy.
        - bad_ko must be understandable but intentionally literal or awkward Korean.
        - improved_ko must be natural Korean suitable for documentation.
        - notes must be 2 short Korean strings explaining the improvement.
        - tags must be 2 to 5 lowercase kebab-case strings.
        - Keep official product names in English when appropriate.
        - Do not omit any item.
        - Do not add markdown fences or commentary.
        """
    ).strip()

    user_prompt = textwrap.dedent(
        f"""
        Source document title: {title}
        Source document URL: {url}
        Unit type: {unit}

        Translate every source_en item into Korean and generate bad_ko, improved_ko, notes, and tags.
        Input items:
        {json.dumps(batch, ensure_ascii=False, indent=2)}
        """
    ).strip()

    response_text = _call_openai_chat(
        api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    payload = _parse_json_payload(response_text)
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError(f"Model response must be a JSON object with an 'items' array: {payload}")

    translated_by_id: dict[str, dict] = {}
    for index, item in enumerate(payload["items"], start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Translated item #{index} must be a JSON object.")
        required_fields = {"id", "bad_ko", "improved_ko", "notes", "tags"}
        missing = required_fields - set(item)
        if missing:
            raise ValueError(f"Translated item #{index} is missing fields: {sorted(missing)}")
        if not isinstance(item["notes"], list) or not all(isinstance(note, str) for note in item["notes"]):
            raise ValueError(f"Translated item #{index} must use a list of strings for notes.")
        if not isinstance(item["tags"], list) or not all(isinstance(tag, str) for tag in item["tags"]):
            raise ValueError(f"Translated item #{index} must use a list of strings for tags.")
        translated_by_id[item["id"]] = item

    translated: list[dict] = []
    for source_item in batch:
        translated_item = translated_by_id.get(source_item["id"])
        if translated_item is None:
            raise ValueError(f"Missing translated output for {source_item['id']}")
        translated.append(
            {
                "id": source_item["id"],
                "source_en": source_item["source_en"],
                "bad_ko": translated_item["bad_ko"].strip(),
                "improved_ko": translated_item["improved_ko"].strip(),
                "notes": [note.strip() for note in translated_item["notes"] if note.strip()],
                "tags": [_slugify(tag, fallback="tag") for tag in translated_item["tags"] if str(tag).strip()],
            }
        )
    return translated


def _translate_records(
    records: list[dict],
    *,
    api_key: str,
    model: str,
    title: str,
    url: str,
    unit: str,
) -> list[dict]:
    if not records:
        return []

    translated: list[dict] = []
    batches = _chunked(records, BATCH_SIZES[unit])
    total_batches = len(batches)
    for batch_index, batch in enumerate(batches, start=1):
        print(f"[{unit}] batch {batch_index}/{total_batches} ({len(batch)} items)")
        translated.extend(
            _translate_batch(
                api_key,
                model=model,
                title=title,
                url=url,
                unit=unit,
                batch=batch,
            )
        )
    return translated


def _write_json(path: Path, payload: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _write_markdown(path: Path, *, title: str, url: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"# {title}\n\nSource: {url}\n\n{body.strip()}\n"
    path.write_text(content, encoding="utf-8")


def _build_doc_bundle(url: str, markdown_text: str) -> tuple[str, dict[str, list[dict]]]:
    parsed = urllib.parse.urlparse(url)
    doc_slug = _slugify(parsed.path.split("/")[-1] or parsed.netloc)
    paragraphs = _extract_paragraphs(markdown_text)
    sentences = _extract_sentences(paragraphs)
    words = _extract_words(paragraphs)
    return doc_slug, {
        "words": _build_word_records(doc_slug, words),
        "sentences": _build_text_records("sentences", doc_slug, sentences),
        "paragraphs": _build_text_records("paragraphs", doc_slug, paragraphs),
    }


def build_goldens(
    base_dir: Path,
    *,
    urls_path: Path,
    markdown_dir: Path,
    golden_dir: Path,
    model: str,
    max_words: int | None,
    max_sentences: int | None,
    max_paragraphs: int | None,
) -> dict[str, int]:
    _load_env(base_dir)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required. Add it to your environment or .env file.")

    urls = _read_urls(urls_path)
    merged_records = {
        "words": [],
        "sentences": [],
        "paragraphs": [],
    }

    for url in urls:
        html = _fetch_url_text(url, timeout=DOC_TIMEOUT_SECONDS)
        title = _extract_title(html, url)
        markdown_text = _html_to_markdownish(html)
        doc_slug, bundle = _build_doc_bundle(url, markdown_text)

        if max_words is not None:
            bundle["words"] = bundle["words"][:max_words]
        if max_sentences is not None:
            bundle["sentences"] = bundle["sentences"][:max_sentences]
        if max_paragraphs is not None:
            bundle["paragraphs"] = bundle["paragraphs"][:max_paragraphs]

        markdown_path = markdown_dir / f"{doc_slug}.md"
        _write_markdown(markdown_path, title=title, url=url, body=markdown_text)

        for unit, source_records in bundle.items():
            translated_records = _translate_records(
                source_records,
                api_key=api_key,
                model=model,
                title=title,
                url=url,
                unit=unit,
            )
            merged_records[unit].extend(translated_records)

    _write_json(golden_dir / "words.json", merged_records["words"])
    _write_json(golden_dir / "sentences.json", merged_records["sentences"])
    _write_json(golden_dir / "paragraphs.json", merged_records["paragraphs"])

    return {name: len(records) for name, records in merged_records.items()}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch source docs from URLs, save markdown snapshots, and build golden JSON files with OpenAI translations.",
    )
    parser.add_argument(
        "--base-dir",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repository root. Defaults to the current project root.",
    )
    parser.add_argument(
        "--urls-path",
        type=Path,
        default=None,
        help="Optional path to the URL list file.",
    )
    parser.add_argument(
        "--markdown-dir",
        type=Path,
        default=None,
        help="Optional output directory for fetched markdown snapshots.",
    )
    parser.add_argument(
        "--golden-dir",
        type=Path,
        default=None,
        help="Optional output directory for generated JSON files.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model used for translation generation. Defaults to {DEFAULT_MODEL}.",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=None,
        help="Optional cap on the number of word records per document.",
    )
    parser.add_argument(
        "--max-sentences",
        type=int,
        default=None,
        help="Optional cap on the number of sentence records per document.",
    )
    parser.add_argument(
        "--max-paragraphs",
        type=int,
        default=None,
        help="Optional cap on the number of paragraph records per document.",
    )
    args = parser.parse_args()

    base_dir = args.base_dir.resolve()
    urls_path = (args.urls_path or (base_dir / DEFAULT_URLS_PATH)).resolve()
    markdown_dir = (args.markdown_dir or (base_dir / DEFAULT_MARKDOWN_DIR)).resolve()
    golden_dir = (args.golden_dir or (base_dir / DEFAULT_GOLDEN_DIR)).resolve()

    counts = build_goldens(
        base_dir,
        urls_path=urls_path,
        markdown_dir=markdown_dir,
        golden_dir=golden_dir,
        model=args.model,
        max_words=args.max_words,
        max_sentences=args.max_sentences,
        max_paragraphs=args.max_paragraphs,
    )

    for unit, count in counts.items():
        print(f"{unit}: {count} records")


if __name__ == "__main__":
    main()
