# PLAN

## 현재 단계

공식 OpenAI 영어-한국어 문서 쌍을 대상으로 하는 Phase 1 MVP는 이미 구현되어 있습니다. 현재 브랜치는 이 MVP를 더 읽기 쉽고, 더 검토하기 쉬운 형태로 정리하는 데 초점을 두고 있습니다.

## 완료된 항목

- 공식 `openai.com` EN-KO 페이지 쌍을 중심으로 Phase 1 범위를 정의
- `docs/golden/`과 `evals/`를 삭제하거나 구조를 바꾸지 않고 유지
- 현재 수집, 정렬, candidate 생성, 평가, 보고서 생성 스크립트 구현
- `why-we-no-longer-evaluate-swe-bench-verified`에 대한 샘플 산출물 생성
- `reference_ko`는 자동 golden이 아니며, human-reviewed 항목만 `reviewed_golden`이 될 수 있음을 명확히 정리
- `docs/golden/words.json`, `docs/golden/sentences.json`, `docs/golden/paragraphs.json`를 lightweight reviewed-golden 평가 자산으로 재정리
- 단어, 문장, 문단 수준 golden 체크를 위한 경량 평가 경로 추가
- 이후 모델, 프롬프트, 파이프라인 비교를 위한 optional metadata 추가
- 외부 검토 기준으로 문서 정리 및 현재 권장 MVP 모델 설정을 `gpt-5.4-mini`로 통일

## 다음 단계

- 더 많은 공식 `openai.com` 영어-한국어 페이지 쌍 추가
- 현재 evaluation-first 경로를 기반으로 `candidate_ko -> evaluation -> improved_candidate_ko -> human review` 흐름 정리
- human review queue를 확대하고, 검토 완료 항목만 `reviewed_golden`으로 승격
- prompt, model, pipeline 변경 전후에 reviewed-golden 레이어로 경량 sanity check 수행
- 반복적으로 등장하는 문서 핵심 용어에 대한 terminology / style guidance 보강
- 한국어 reference가 약한 `developers.openai.com` 문서 영역으로 같은 프레임워크를 Phase 2에서 확장
