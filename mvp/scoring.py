from __future__ import annotations

import math
import re
from typing import Sequence


SCORE_WEIGHTS = {
    "semantic_similarity_score": 0.30,
    "backtranslation_similarity_score": 0.25,
    "terminology_consistency_score": 0.15,
    "llm_judge_score": 0.30,
}


TERMINOLOGY_RULES = [
    {
        "label": "SWE-bench Verified",
        "source_patterns": [r"\bSWE-bench Verified\b"],
        "candidate_patterns": [r"SWE-bench Verified"],
    },
    {
        "label": "SWE-bench Pro",
        "source_patterns": [r"\bSWE-bench Pro\b"],
        "candidate_patterns": [r"SWE-bench Pro"],
    },
    {
        "label": "frontier",
        "source_patterns": [r"\bfrontier\b"],
        "candidate_patterns": [r"프런티어", r"\bfrontier\b"],
    },
    {
        "label": "benchmark",
        "source_patterns": [r"\bbenchmark\b"],
        "candidate_patterns": [r"벤치마크", r"\bbenchmark\b"],
    },
    {
        "label": "contamination",
        "source_patterns": [r"\bcontaminat(?:ed|ion)\b"],
        "candidate_patterns": [r"오염", r"\bcontaminat(?:ed|ion)\b"],
    },
    {
        "label": "gold patch",
        "source_patterns": [r"\bgold patch\b"],
        "candidate_patterns": [r"골드 패치", r"\bgold patch\b"],
    },
    {
        "label": "Preparedness Framework",
        "source_patterns": [r"\bPreparedness Framework\b"],
        "candidate_patterns": [r"Preparedness Framework", r"준비성 평가 프레임워크"],
    },
]


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


def cosine_to_score(cosine_value: float) -> float:
    clamped = max(0.0, min(1.0, cosine_value))
    return round(clamped * 100, 1)


def score_terminology(*, source_en: str, candidate_ko: str) -> tuple[float, list[str], list[dict]]:
    applicable = []
    passed = 0
    issues: list[str] = []
    details: list[dict] = []

    for rule in TERMINOLOGY_RULES:
        if not any(re.search(pattern, source_en, flags=re.IGNORECASE) for pattern in rule["source_patterns"]):
            continue

        applicable.append(rule["label"])
        matched = any(re.search(pattern, candidate_ko, flags=re.IGNORECASE) for pattern in rule["candidate_patterns"])
        details.append({"label": rule["label"], "matched": matched})
        if matched:
            passed += 1
            continue

        issues.append(f"Terminology mismatch: expected a consistent rendering for '{rule['label']}'.")

    if not applicable:
        return 100.0, issues, details

    return round((passed / len(applicable)) * 100, 1), issues, details


def compute_overall_score(record: dict) -> float:
    score = 0.0
    for field, weight in SCORE_WEIGHTS.items():
        score += float(record[field]) * weight
    return round(max(0.0, min(100.0, score)), 1)


def review_reasons(record: dict) -> list[str]:
    reasons = []
    if record["overall_score"] < 80:
        reasons.append("overall_score < 80")
    if record["llm_judge_score"] < 75:
        reasons.append("llm_judge_score < 75")
    if record["terminology_consistency_score"] < 100:
        reasons.append("terminology_consistency_score < 100")
    return reasons
