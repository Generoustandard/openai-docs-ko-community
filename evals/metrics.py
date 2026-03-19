from __future__ import annotations

import math
from typing import Sequence


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same length.")
    if not vec_a:
        raise ValueError("Vectors must not be empty.")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(value * value for value in vec_a))
    norm_b = math.sqrt(sum(value * value for value in vec_b))

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must not be all zeros.")

    return dot_product / (norm_a * norm_b)


def candidate_vs_golden_similarity(
    candidate_ko_embedding: Sequence[float],
    golden_ko_embedding: Sequence[float],
) -> float:
    return cosine_similarity(candidate_ko_embedding, golden_ko_embedding)


def source_vs_backtranslation_similarity(
    source_en_embedding: Sequence[float],
    backtranslated_en_embedding: Sequence[float],
) -> float:
    return cosine_similarity(source_en_embedding, backtranslated_en_embedding)
