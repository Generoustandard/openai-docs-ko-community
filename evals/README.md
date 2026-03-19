# MVP 평가 가이드

이 폴더는 번역 품질을 정교하게 자동 판정하는 시스템이 아니라, 작은 golden 예제를 기준으로 후보 번역을 비교해 보는 **가벼운 MVP 평가 구조**를 설명합니다. 목표는 점수를 절대적인 정답처럼 쓰는 것이 아니라, 어떤 후보가 더 자연스럽고 의미를 잘 보존하는지 빠르게 살펴보는 것입니다.

## 이 평가가 확인하려는 것

- 후보 한국어 번역이 curated golden 번역과 얼마나 가까운가
- 후보 한국어 번역이 영어 원문의 의미를 얼마나 잘 유지하는가
- 점수만으로는 보이지 않는 어색함이나 용어 흔들림을 사람이 함께 확인할 수 있는가

## Metric 1: candidate_ko vs golden_ko cosine similarity

첫 번째 지표는 모델이 생성한 한국어 번역과, 사람이 다듬어 둔 golden 한국어 번역 사이의 cosine similarity입니다.

이 지표가 주로 보는 것은 다음과 같습니다.

- 선호하는 표현과 얼마나 가까운가
- 같은 용어를 얼마나 일관되게 썼는가
- 문장 전체의 표현 방향이 기준 번역과 얼마나 비슷한가

이 지표는 "우리 팀이 현재 선호하는 한국어 번역 스타일에 얼마나 가까운가"를 보는 데 유용합니다. 다만 golden과 다른 표현이라고 해서 무조건 나쁜 번역은 아닙니다. 자연스럽고 정확하지만 wording이 다르면 similarity가 낮아질 수 있습니다.

## Metric 2: source_en vs backtranslated_en cosine similarity

두 번째 지표는 영어 원문과, `영어 -> 한국어 -> 영어`로 다시 옮긴 back-translated English 사이의 cosine similarity입니다.

이 지표가 주로 보는 것은 다음과 같습니다.

- 한국어 번역 과정에서 핵심 의미가 빠지지 않았는가
- 제품 기능이나 제약 조건이 왜곡되지 않았는가
- 한국어 문장이 원문의 정보 구조를 지나치게 바꾸지 않았는가

이 지표는 번역의 **의미 보존**을 확인하는 용도에 가깝습니다. 즉, Korean-to-Korean 비교가 "표현이 기준과 얼마나 닮았는가"를 본다면, back-translation 비교는 "원래 뜻을 얼마나 유지했는가"를 보는 보조 장치입니다.

## 왜 두 지표를 함께 보나

두 지표는 서로 다른 실패 유형을 잡습니다.

- `candidate_ko vs golden_ko`는 wording, 톤, 용어 선택의 흔들림을 잘 드러냅니다.
- `source_en vs backtranslated_en`는 의미 누락이나 과한 의역을 더 잘 드러냅니다.

둘 중 하나만 보면 오판하기 쉽습니다. 예를 들어 similarity가 높아도 한국어가 번역투일 수 있고, 반대로 golden과 표현은 다르지만 더 자연스러운 번역일 수도 있습니다. 그래서 MVP에서는 **두 점수를 나란히 보고, 마지막 판단은 사람이 내리는 방식**을 기본 원칙으로 둡니다.

## 실전 사용 방식

1. 작은 golden 예제 세트에서 몇 개 샘플을 고릅니다.
2. 후보 한국어 번역을 준비합니다.
3. 외부 도구나 모델을 사용해 embedding과 back-translated English를 만듭니다.
4. 이 폴더의 간단한 스크립트로 두 cosine similarity를 계산합니다.
5. 점수가 낮거나 결과가 엇갈리는 항목을 사람이 직접 읽고 메모를 남깁니다.

MVP에서는 한 번에 많은 항목을 돌리는 것보다, 작은 예제를 가지고 어떤 문제가 드러나는지 확인하는 쪽이 더 중요합니다.

## 한계와 주의점

- cosine similarity는 어떤 embedding 모델을 쓰는지에 따라 달라집니다.
- back-translation이 원문 의미를 잘 살렸다고 해도, 한국어 문장이 자연스럽다는 보장은 없습니다.
- 반대로 golden과 similarity가 낮아도, 표현이 더 자연스럽고 정확할 수 있습니다.
- 숫자는 비교를 돕는 신호일 뿐이며, 번역 품질을 자동으로 확정하는 판정기가 아닙니다.

이 MVP는 의도적으로 **최종 단일 점수**를 만들지 않습니다. `candidate_ko vs golden_ko`와 `source_en vs backtranslated_en`를 각각 보고, 필요하면 사람이 메모와 함께 판단합니다.

## 최소 폴더 구조

```text
evals/
  README.md
  golden_loader.py
  metrics.py
  run_eval.py
  results/
    README.md
```

## 포함된 작은 스크립트

- [golden_loader.py](/C:/Users/user/Documents/Repo/openai-docs-ko-community/evals/golden_loader.py)
  `docs/golden/` 아래 JSON 파일을 읽고 기본 필드 검증을 합니다.
- [metrics.py](/C:/Users/user/Documents/Repo/openai-docs-ko-community/evals/metrics.py)
  pure Python으로 cosine similarity를 계산하는 최소 함수들을 제공합니다.
- [run_eval.py](/C:/Users/user/Documents/Repo/openai-docs-ko-community/evals/run_eval.py)
  이미 준비된 텍스트와 embedding을 담은 JSON 입력을 받아 두 개의 similarity 점수를 계산합니다.

## run_eval.py 입력 형식

`run_eval.py`는 번역 API, embedding API, back-translation API를 직접 호출하지 않습니다. 대신 이미 준비된 데이터를 담은 JSON 파일을 읽습니다.

```json
[
  {
    "id": "sentences.responses.recommendation-01",
    "source_en": "Original English",
    "candidate_ko": "Model-generated Korean",
    "golden_ko": "Curated Korean",
    "backtranslated_en": "English translated back from candidate_ko",
    "candidate_ko_embedding": [0.1, 0.2],
    "golden_ko_embedding": [0.1, 0.2],
    "source_en_embedding": [0.1, 0.2],
    "backtranslated_en_embedding": [0.1, 0.2]
  }
]
```

## run_eval.py 출력 형식

출력 JSON은 각 항목별 점수와 간단한 평균 요약을 포함합니다.

```json
{
  "records": [
    {
      "id": "sentences.responses.recommendation-01",
      "candidate_vs_golden_cosine": 0.99,
      "source_vs_backtranslation_cosine": 0.98
    }
  ],
  "summary": {
    "count": 1,
    "average_candidate_vs_golden_cosine": 0.99,
    "average_source_vs_backtranslation_cosine": 0.98
  }
}
```

## 권장 운영 원칙

- 데이터셋은 작고 선별된 상태로 유지합니다.
- 점수 차이가 큰 사례를 중심으로 사람이 메모를 남깁니다.
- 기준 번역이 바뀌면 golden도 함께 업데이트합니다.
- 플랫폼화보다 예제 품질과 설명의 명확성을 우선합니다.
