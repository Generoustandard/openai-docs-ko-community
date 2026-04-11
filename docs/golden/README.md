# Golden Example Sets

이 디렉터리에는 영어-한국어 번역 예시를 단어, 문장, 문단 수준으로 정리한 small golden asset pool이 들어 있습니다.

- `words.json`
- `sentences.json`
- `paragraphs.json`

이 파일들은 모두 같은 역할을 하지 않습니다. 현재 저장소는 이 안에서 소수의 항목만 `reviewed_golden_candidate`로 골라 경량 evaluation target으로 사용하고, 나머지는 example bank로 유지합니다.

## 저장소 안에서의 역할

- `reference_ko`: Phase 1 공식 문서 쌍 평가에서 쓰는 페이지 단위 baseline
- `reviewed_golden`: 사람이 검토해 curated evaluation target으로 인정한 소규모 target
- `candidate_ko`: 평가 대상인 raw LLM 출력
- `improved_candidate_ko`: 필요할 때 다시 평가할 수 있는 후속 개선안

## 레코드 필드

각 golden record는 아래 필드를 가집니다.

- `source_en`
- `bad_ko`
- `improved_ko`
- `notes`
- `tags`
- `target_role`
- `review_status`

해석 원칙:

- `improved_ko`는 golden target 후보로 보관하는 한국어 표현입니다.
- `bad_ko`는 대비용 example이며 evaluation target이 아닙니다.
- `target_role = reviewed_golden_candidate`인 항목만 현재 golden eval이 읽는 target입니다.
- `target_role = example_only`인 항목은 예시 bank로 남겨 두지만 현재 evaluation target은 아닙니다.
- `review_status = pending_human_review`는 아직 사람이 최종 승인하지 않았다는 뜻입니다.

현재 구성은 총 7개 항목만 `reviewed_golden_candidate`로 표시하고, 나머지는 `example_only`로 둡니다. 이 구조는 Phase 1 평가 철학에 맞춰 “작은 curated target + 더 큰 example bank”를 유지하기 위한 것입니다.

## 사용 방식

- 경량 cosine similarity 체크
- optional backtranslation similarity 체크
- 모델, 프롬프트, 파이프라인 변경 전후의 sanity check

메인 Phase 1 문서 쌍 흐름을 바꾸지 않고 golden target만 점수화하려면 [run_golden_eval.py](../../run_golden_eval.py)를 사용하십시오. 이 스크립트는 각 파일 전체를 평가하지 않고, `reviewed_golden_candidate`로 표시된 항목만 대상으로 삼습니다.
