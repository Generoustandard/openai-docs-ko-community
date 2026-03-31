# Codex-Community-Docs-KR

이 저장소는 공식 OpenAI 영어-한국어 문서쌍을 사용해 번역 품질 평가 MVP를 구현하는 실험 저장소입니다.

현재 1차 MVP의 중심 경로는 다음과 같습니다.

1. 공식 OpenAI 영어 문서를 `source_en`으로 수집한다.
2. 공식 OpenAI 한국어 문서를 `reference_ko`로 수집한다.
3. 본문을 paragraph-level 평가 단위로 정렬한다.
4. `source_en`으로부터 새로운 `candidate_ko`를 생성한다.
5. `reference_ko`와 `candidate_ko`를 비교 평가한다.
6. 결과를 JSON과 Markdown report로 저장한다.

## 1차 MVP 범위

1차 MVP는 `openai.com`의 공식 영어-한국어 문서쌍 기반 평가 데모다.

핵심 역할은 아래처럼 구분한다.

- `source_en`: 공식 영어 원문
- `reference_ko`: 공식 한국어 번역문
- `candidate_ko`: LLM이 새로 생성한 한국어 번역
- `reviewed_golden`: 나중에 사람이 직접 검토해 승격한 소수 샘플

중요한 원칙:

- `reference_ko`는 곧바로 `golden`이 아니다.
- 사람이 검토하지 않은 LLM 생성 번역은 `golden`으로 저장하지 않는다.
- 1차 MVP는 `source_en / reference_ko / candidate_ko` 기반 평가 파이프라인이다.

## 2차 확장 범위

아래 항목은 이번 메인 MVP가 아니라 이후 확장 경로다.

- `developers.openai.com` 문서 수집 및 평가
- reference-less 평가
- 더 넓은 candidate generation pipeline
- curated `reviewed_golden` 확장

기존 `docs/golden/` 및 `evals/` 자산은 삭제하지 않고 future expansion 또는 experimental pipeline 성격으로 유지한다.

## 현재 저장소 구조 요약

- [docs/golden/words.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/golden/words.json)
- [docs/golden/sentences.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/golden/sentences.json)
- [docs/golden/paragraphs.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/golden/paragraphs.json)
- [docs/examples/responses-api.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/examples/responses-api.md)
- [evals/README.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/evals/README.md)
- [guidelines/terminology.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/guidelines/terminology.md)
- [guidelines/translation.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/guidelines/translation.md)

## 문서화 파일

- [AGENTS.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/AGENTS.md)
- [PLAN.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/PLAN.md)
- [EVAL_SPEC.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/EVAL_SPEC.md)

## 실행 흐름

구현되는 메인 스크립트는 아래 흐름을 따른다.

- `collect_pair.py`
- `align_units.py`
- `generate_candidate.py`
- `run_eval.py`
- `build_report.py`

## 준비 사항

- Python 3.12+
- Chrome 설치
- `OPENAI_API_KEY` 설정
- `pip install -r requirements.txt`

중요:

- `collect_pair.py`는 기본적으로 headful Chrome을 사용한다.
- OpenAI 웹페이지는 headless 브라우저에서 차단될 수 있으므로, 특별한 이유가 없으면 `--headless` 없이 실행한다.

## 실행 예시

### 1. 공식 문서쌍 수집

```bash
python -X utf8 collect_pair.py ^
  --slug why-we-no-longer-evaluate-swe-bench-verified ^
  --source-url https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ ^
  --reference-url https://openai.com/ko-KR/index/why-we-no-longer-evaluate-swe-bench-verified/
```

### 2. 평가 단위 정렬

```bash
python -X utf8 align_units.py --slug why-we-no-longer-evaluate-swe-bench-verified
```

### 3. `candidate_ko` 생성

```bash
python -X utf8 generate_candidate.py ^
  --input data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json ^
  --model gpt-4.1-mini
```

### 4. 평가 실행

```bash
python -X utf8 run_eval.py ^
  --input data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json ^
  --backtranslation-model gpt-4.1-mini ^
  --judge-model gpt-4.1-mini ^
  --embedding-model text-embedding-3-small
```

### 5. Markdown report 생성

```bash
python -X utf8 build_report.py ^
  --input reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json ^
  --output reports/why-we-no-longer-evaluate-swe-bench-verified.report.md
```

## 샘플 산출물

이번 작업으로 아래 샘플 산출물을 생성했다.

- [docs/pairs/why-we-no-longer-evaluate-swe-bench-verified/pair_manifest.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/docs/pairs/why-we-no-longer-evaluate-swe-bench-verified/pair_manifest.json)
- [data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json)
- [data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json)
- [reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json](/C:/Users/user/Documents/Repo/openai-docs-ko-community/reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json)
- [reports/why-we-no-longer-evaluate-swe-bench-verified.report.md](/C:/Users/user/Documents/Repo/openai-docs-ko-community/reports/why-we-no-longer-evaluate-swe-bench-verified.report.md)

## 기존 자산의 위치 재정의

- `docs/golden/`: reviewed 또는 curated 예시를 쌓기 위한 실험 자산
- `evals/`: 기존 cosine 기반 실험 평가 파이프라인
- 이번 1차 MVP의 메인 경로: 공식 OpenAI 영어-한국어 문서쌍 평가
