# 저장소 에이전트 가이드

## 목표

이 저장소는 공식 OpenAI 영어-한국어 문서 쌍을 기준으로 한국어 번역 품질을 평가하는 Phase 1 MVP를 정리한 저장소입니다.

## 현재 MVP 범위

- Phase 1은 공식 `openai.com` EN-KO 페이지 쌍에 집중합니다.
- 기본 흐름은 문서 쌍 수집, 문단 단위 정렬, `candidate_ko` 생성, `reference_ko` 기준 평가, 보고서 생성입니다.
- `docs/golden/` 아래에는 단어, 문장, 문단 수준의 경량 golden-example 체크 레이어가 함께 존재합니다.
- `developers.openai.com`은 Phase 2 확장 트랙이며, 현재 MVP의 주 경로가 아닙니다.

## 평가 역할

- `source_en`: 공식 영어 원문
- `reference_ko`: OpenAI가 게시한 공식 한국어 번역
- `candidate_ko`: 파이프라인이 새로 생성한 한국어 번역
- `improved_candidate_ko`: 필요할 경우 재평가할 수 있는 후속 개선안
- `reviewed_golden`: 경량 회귀 체크, sanity check, 이후 비교 실험에 쓰는 human-reviewed 예시

## 제약

- `reference_ko`는 reference이지 자동으로 golden이 아닙니다.
- `candidate_ko`는 golden으로 저장하지 않습니다.
- `improved_candidate_ko`도 candidate 출력이며 golden이 아닙니다.
- 유지보수자 또는 커뮤니티 리뷰어의 수동 검토가 있어야만 `reviewed_golden`으로 승격할 수 있습니다.

## 자산 보존

`docs/golden/`과 `evals/` 아래의 기존 파일은 유지합니다. `docs/golden/words.json`, `docs/golden/sentences.json`, `docs/golden/paragraphs.json`는 lightweight reviewed-golden 체크 자산으로 사용하고, `evals/`는 보존 중인 실험 경로로 남깁니다. Phase 1 공식 문서 쌍 MVP 작업 중 이 자산들을 삭제하지 마십시오.
