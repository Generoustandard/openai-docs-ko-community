from __future__ import annotations

import re


_SPACE_RE = re.compile(r"\s+")
_SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:!?])")

_UNIT_TYPE_BY_TAG = {
    "P": "paragraph",
    "LI": "list_item",
    "H2": "section_header",
    "H3": "section_header",
    "H4": "section_header",
}


def normalize_prose(text: str) -> str:
    """Normalize extracted article prose into a stable single-line block."""
    normalized = text.replace("\u2060", " ")
    normalized = normalized.replace("(opens in a new window)", " ")
    normalized = normalized.replace("(새 창에서 열기)", " ")
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("\n", " ")
    normalized = _SPACE_RE.sub(" ", normalized).strip()
    normalized = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", normalized)
    return normalized


def unit_type_from_tag(tag: str) -> str:
    return _UNIT_TYPE_BY_TAG.get(tag.upper(), "paragraph")
