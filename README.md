# Codex-Community-Docs-KR

비공식 커뮤니티 기반 MVP로, OpenAI 문서의 한국어 번역 품질을 작고 명확한 예제로 보여주는 저장소입니다. 전체 문서 사이트를 번역하거나 플랫폼을 만드는 대신, "좋은 한국어 기술 번역이 무엇인지"를 빠르게 이해할 수 있는 샘플과 가벼운 평가 아이디어에 집중합니다.

## 이 저장소가 보여주려는 것

- 영어 원문을 그대로 옮긴 한국어와, 읽기 쉬운 한국어 기술 문서 번역의 차이
- 용어 일관성, 자연스러운 문장 흐름, 기술적 정확성을 함께 고려하는 방법
- 작은 golden dataset과 간단한 cosine similarity 기반 비교로 번역 품질을 점검하는 MVP 방식

## 핵심 구성

- [docs/golden/words.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/golden/words.json)
- [docs/golden/sentences.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/golden/sentences.json)
- [docs/golden/paragraphs.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/golden/paragraphs.json)
- [docs/examples/responses-api.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/examples/responses-api.md)
- [evals/README.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/evals/README.md)

## Golden 예제의 목적

`docs/golden/` 아래의 예제는 대규모 데이터셋이 아니라, 품질 기준을 설명하는 작은 기준점입니다. 각 항목은 영어 원문, 필요할 때의 직역 또는 어색한 한국어, 개선된 한국어, 그리고 왜 개선 버전이 더 좋은지에 대한 짧은 메모를 포함합니다.

이 예제들은 다음을 돕습니다.

- 반복적으로 헷갈리는 기술 용어를 일관되게 다듬기
- 직역체를 줄이고 한국어 문서답게 다시 쓰기
- 번역 품질 논의를 추상적인 취향이 아니라 구체적인 사례 중심으로 하기

## MVP 평가 아이디어

이 저장소의 평가는 자동 채점 시스템이 아니라, 사람이 빠르게 비교해 볼 수 있는 가벼운 보조 장치입니다.

- Korean-to-Korean cosine similarity:
  후보 한국어 번역과 curated golden 한국어 번역이 얼마나 비슷한지 봅니다.
- English-to-back-translation cosine similarity:
  영어 원문과 `영어 -> 한국어 -> 영어`로 되돌린 문장이 얼마나 의미를 잘 유지하는지 봅니다.

중요한 점은 두 점수를 하나의 최종 점수로 합치지 않는다는 것입니다. 점수는 비교용 신호일 뿐이고, 최종 판단은 사람이 문맥과 문체를 보고 내려야 합니다. 자세한 설명은 [evals/README.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/evals/README.md)에 정리합니다.

## 기여 방법

- 더 자연스럽고 정확한 한국어 번역 예제를 제안하기
- 기존 golden 항목의 메모를 더 명확하게 다듬기
- 작지만 대표성 있는 문장이나 문단을 추가하기
- 특정 용어의 번역 기준을 더 일관되게 정리하기

기여는 작고 읽기 쉬운 단위가 가장 좋습니다. 이 저장소는 빠르게 데모하고 토론하기 위한 MVP이므로, 대량 번역이나 복잡한 자동화보다 작은 개선을 선호합니다.

## 현재 MVP 범위 밖

- OpenAI 문서 전체 sitemap 번역
- 프로덕션급 평가 플랫폼
- 자동 리더보드나 대규모 벤치마크
- 번역, 임베딩, 역번역을 위한 외부 API 호출 자동화

## 다음 단계

- Responses API 외에 1-2개 문서 예제를 더 추가해 구조가 유용한지 확인
- 반복적으로 문제 되는 용어를 중심으로 golden 예제를 점진적으로 확장
- 실제 사용자가 생기면 선택적으로 provider adapter나 CI 검증을 검토
