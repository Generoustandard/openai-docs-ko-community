# Evaluation Spec

## 목적

이 문서는 공식 OpenAI 영어-한국어 문서 쌍을 기준으로 한국어 번역 품질을 평가하는 Phase 1 MVP 명세입니다.

## 범위

Phase 1은 다음 두 요소가 모두 존재하는 공식 `openai.com` 페이지 쌍으로 한정됩니다.

- `source_en`: 공식 영어 원문
- `reference_ko`: OpenAI가 게시한 공식 한국어 번역

현재 평가 파이프라인은 다음 산출물을 다룹니다.

- `candidate_ko`: `source_en`에서 새로 생성한 한국어 번역
- `improved_candidate_ko`: 이후 필요할 경우 다시 평가할 수 있는 후속 개선안
- `backtranslated_en`: `candidate_ko`를 다시 영어로 옮긴 backtranslation

`reviewed_golden`은 자동화된 Phase 1 점수화 루프 밖에 있는 개념입니다. 사람이 검토하고 의도적으로 승격한 예시만 regression testing 또는 더 깊은 평가에 사용합니다.

중요한 원칙:

- `reference_ko`는 reference이지 자동으로 golden이 아닙니다.
- `candidate_ko`는 golden으로 저장하지 않습니다.
- `improved_candidate_ko`도 candidate 출력이며 golden이 아닙니다.
- 사람이 검토한 샘플만 `reviewed_golden`이 될 수 있습니다.

## 호환되는 평가 레이어

이 저장소는 서로 호환되는 두 가지 평가 레이어를 가집니다.

1. Phase 1 MVP의 공식 문서 쌍 평가
   `candidate_ko`를 공식 페이지 단위 `reference_ko`와 비교합니다.
2. 회귀 체크와 비교를 위한 경량 golden-example 평가
   `docs/golden/` 아래의 curated 또는 human-reviewed 예시와 생성 결과를 단어, 문장, 문단 수준에서 비교합니다.

이 구조는 다음 방향을 유지합니다.

- 소규모 golden 세트 사용
- 한국어 측 cosine similarity
- backtranslation similarity
- 이후 모델, 프롬프트, 파이프라인 비교

## 단위 선택

현재 MVP는 문단 수준 정렬을 사용합니다. 실제 평가 단위는 기사 본문에서 뽑은 안정적인 prose block입니다.

- paragraph blocks (`p`)
- list items (`li`)
- section headers (`h2`~`h3`)

코드 블록, diff, 코드 예시 캡션은 1차 평가 데이터셋에서 제외합니다. 이런 항목은 번역 품질 신호보다 source preservation 성격이 강하기 때문입니다.

별도로 golden-example 레이어는 단위 범위를 더 넓게 유지합니다.

- word level
- sentence level
- paragraph level

## 페이로드 형태

### 정렬 입력

현재 `data/processed/` 아래의 정렬 입력은 top-level list입니다.

```json
[
  {
    "id": "why-we-no-longer-evaluate-swe-bench-verified.block-001",
    "unit_type": "paragraph",
    "source_en": "English source block",
    "reference_ko": "Official Korean reference block",
    "source_meta": {
      "tag": "P",
      "source_index": 1,
      "reference_index": 1,
      "pair_slug": "why-we-no-longer-evaluate-swe-bench-verified"
    }
  }
]
```

공통 로더는 top-level `records` 배열이 있는 object도 허용하지만, 현재 Phase 1 정렬 입력의 기본 형태는 flat list입니다.

### Candidate 생성 출력

`generate_candidate.py`는 metadata와 `records`를 함께 가진 object를 씁니다.

```json
{
  "generated_at": "2026-03-31T16:59:18.814737+00:00",
  "generation_model": "gpt-5.4-mini",
  "run_label": "phase1-baseline",
  "pipeline_label": "baseline",
  "prompt_label": "official_openai_style_translation_v1",
  "records": [
    {
      "id": "why-we-no-longer-evaluate-swe-bench-verified.block-001",
      "unit_type": "paragraph",
      "source_en": "English source block",
      "reference_ko": "Official Korean reference block",
      "candidate_ko": "Generated Korean block",
      "source_meta": {
        "tag": "P",
        "pair_slug": "why-we-no-longer-evaluate-swe-bench-verified"
      }
    }
  ]
}
```

### Evaluation 출력

`run_eval.py`는 metadata, configuration, summary, 평가된 `records`를 함께 가진 object를 씁니다.

```json
{
  "generation_model": "gpt-5.4-mini",
  "evaluated_at": "2026-03-31T17:02:52.303607+00:00",
  "config": {
    "candidate_field": "candidate_ko",
    "backtranslation_model": "gpt-5.4-mini",
    "judge_model": "gpt-5.4-mini",
    "embedding_model": "text-embedding-3-small",
    "score_scale": "0-100",
    "overall_formula": "0.30 * semantic_similarity_score + 0.25 * backtranslation_similarity_score + 0.15 * terminology_consistency_score + 0.30 * llm_judge_score"
  },
  "summary": {
    "count": 46,
    "average_overall_score": 92.4,
    "human_review_count": 7
  },
  "records": [
    {
      "id": "why-we-no-longer-evaluate-swe-bench-verified.block-001",
      "source_en": "English source block",
      "reference_ko": "Official Korean reference block",
      "candidate_ko": "Generated Korean block",
      "backtranslated_en": "Backtranslated English block",
      "semantic_similarity_score": 92.4,
      "backtranslation_similarity_score": 89.7,
      "terminology_consistency_score": 100.0,
      "llm_judge_score": 90.0,
      "overall_score": 91.0,
      "issues": [
        "Minor style drift around benchmark phrasing."
      ],
      "judge_needs_human_review": false,
      "review_reasons": [
        "terminology_consistency_score < 100"
      ],
      "needs_human_review": true,
      "suggested_revision": "Revised Korean text",
      "metadata": {
        "unit_type": "paragraph",
        "tag": "P",
        "pair_slug": "why-we-no-longer-evaluate-swe-bench-verified",
        "candidate_source_field": "candidate_ko",
        "terminology_details": [
          {
            "label": "SWE-bench Verified",
            "matched": true
          }
        ]
      }
    }
  ]
}
```

## 점수 스케일

모든 점수는 `0-100` 스케일을 사용합니다.

## 지표 정의

### `semantic_similarity_score`

생성된 한국어와 한국어 측 비교 target 사이의 embedding cosine similarity를 아래 방식으로 변환합니다.

```text
semantic_similarity_score = clamp(cosine_similarity(korean_target, candidate_ko), 0, 1) * 100
```

공식 Phase 1 문서 쌍 MVP에서는 `korean_target = reference_ko`입니다.

경량 golden-example 레이어에서는 `korean_target = reviewed_golden_ko`입니다.

### `backtranslation_similarity_score`

1. `candidate_ko`를 다시 영어로 옮겨 `backtranslated_en` 생성
2. `source_en`과 `backtranslated_en`의 embedding cosine similarity 계산
3. 아래 방식으로 점수화

```text
backtranslation_similarity_score = clamp(cosine_similarity(source_en, backtranslated_en), 0, 1) * 100
```

이 지표는 두 평가 레이어 모두에 공통으로 쓰입니다. 특히 한국어 표현이 달라져도 원래 영어 의미를 유지하는지 확인하면서 모델, 프롬프트, 개선 파이프라인을 비교할 때 유용합니다.

### `terminology_consistency_score`

문서에서 중요한 용어에 대한 소규모 glossary 기반 점수입니다. 현재 구현은 `source_en`에 해당 source-side pattern이 등장한 규칙만 검사하고, 아래 방식으로 점수화합니다.

```text
terminology_consistency_score = (matched_applicable_rules / applicable_rules) * 100
```

적용 가능한 terminology rule이 하나도 없으면 `100.0`입니다.

현재 rule label:

- `SWE-bench Verified`
- `SWE-bench Pro`
- `frontier`
- `benchmark`
- `contamination`
- `gold patch`
- `Preparedness Framework`

### `llm_judge_score`

LLM judge는 다음 요소를 기준으로 `0-100` 점수를 반환합니다.

- accuracy
- naturalness
- terminology consistency
- document style fit

또한 judge는 다음도 함께 반환합니다.

- `issues`
- `judge_needs_human_review`
- `suggested_revision`

## 종합 점수

현재 MVP는 아래 가중 공식을 사용합니다.

```text
overall_score =
  0.30 * semantic_similarity_score +
  0.25 * backtranslation_similarity_score +
  0.15 * terminology_consistency_score +
  0.30 * llm_judge_score
```

최종 값은 소수 첫째 자리에서 반올림하고 `0-100` 범위로 clamp합니다.

## 사람 검토 휴리스틱

구현은 아래 조건 중 하나라도 만족하면 검토 대상으로 표시합니다.

- `overall_score < 80`
- `llm_judge_score < 75`
- `terminology_consistency_score < 100`
- `judge_needs_human_review = true`

최종 `needs_human_review`는 score 기반 규칙과 judge flag를 합친 뒤 `review_reasons`가 비어 있지 않으면 true입니다.

## Golden Example Layer

curated 또는 future-curated golden 자산은 `docs/golden/` 아래에 있으며 현재 다음 파일을 유지합니다.

- `words.json`
- `sentences.json`
- `paragraphs.json`

각 record는 다음 필드를 가집니다.

- `source_en`
- `bad_ko`
- `improved_ko`
- `notes`
- `tags`

해석 원칙:

- `improved_ko`는 현재 golden 예시의 한국어 target이며, 경량 회귀 체크에서는 reviewed golden 텍스트 역할을 합니다.
- `bad_ko`는 대비를 위한 contrastive example일 뿐입니다. candidate run도 아니고 golden target도 아닙니다.
- 이 파일들은 공식 문서 쌍 평가에서 쓰는 페이지 단위 `reference_ko`와는 별개입니다.

`run_golden_eval.py`는 이 세트들을 위한 경량 machine-readable evaluation 경로를 제공합니다. 지원 범위는 다음과 같습니다.

- `source_en`에서 fresh candidate 생성
- 기존 candidate 파일 불러오기
- `candidate_ko` 또는 `improved_candidate_ko` 필드 선택 비교
- 한국어 측 cosine similarity와 optional backtranslation similarity 보고

## 비교용 메타데이터

더 큰 experiment framework를 추가하지 않으면서 이후 비교를 쉽게 하기 위해, candidate와 evaluation 산출물에는 아래 optional label을 포함할 수 있습니다.

- `run_label`
- `pipeline_label`
- `prompt_label`
- `candidate_field`

이 값들은 여러 실행 결과를 모델, 프롬프트, 개선 파이프라인 단위로 비교하는 데 도움을 주며, 현재 Phase 1 MVP 구조는 그대로 유지합니다.

## 출력 위치

- 문서 쌍 스냅샷: `docs/pairs/`
- 정렬된 평가 입력: `data/processed/`
- 점수 결과와 markdown 보고서: `reports/`

## 기존 자산과의 관계

`docs/golden/`과 `evals/` 아래의 기존 파일은 계속 저장소에 남습니다. `docs/golden/`의 curated 파일은 lightweight reviewed-golden 평가 레이어를 지원하고, `evals/`는 메인 Phase 1 공식 문서 쌍 경로가 아니라 보존 중인 실험 또는 future-expansion 경로로 유지합니다.
