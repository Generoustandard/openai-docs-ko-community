# Golden Example Sets

이 디렉터리에는 영어-한국어 번역 예시를 세 가지 수준으로 정리한 소규모 golden 자산이 들어 있습니다.

- `words.json`
- `sentences.json`
- `paragraphs.json`

이 자산들은 경량 회귀 체크와 비교 실행에 사용합니다. 현재 Phase 1 공식 문서 쌍 MVP에서 사용하는 페이지 단위 `reference_ko`와는 같은 개념이 아닙니다.

## 저장소 안에서의 역할

- `reference_ko`: 현재 Phase 1 `openai.com` 문서 쌍 평가에 쓰는 공식 한국어 페이지 reference
- `reviewed_golden`: sanity check, regression check, 모델 또는 프롬프트 비교에 쓰는 소규모 human-reviewed 예시
- `candidate_ko`: 평가 대상인 raw LLM 생성 한국어
- `improved_candidate_ko`: 이후 다시 평가할 수 있는 후속 개선안

## 레코드 형태

각 golden record는 다음 필드를 가집니다.

- `source_en`
- `bad_ko`
- `improved_ko`
- `notes`
- `tags`

golden-set 평가에서는 `improved_ko`를 현재 reviewed golden target으로 취급합니다. 이 값은 페이지 단위 `reference_ko`와도 다르고, raw `candidate_ko`와도 다릅니다.

## 의도된 사용 방식

- 생성된 한국어와 curated 한국어 사이의 빠른 cosine-similarity 체크
- 영어 원문을 기준으로 한 optional backtranslation 체크
- 모델, 프롬프트, 개선 파이프라인을 바꾸기 전후의 경량 회귀 체크

메인 Phase 1 문서 쌍 흐름을 바꾸지 않고 이 세트를 점수화하려면 [run_golden_eval.py](../../run_golden_eval.py)를 사용하십시오.
