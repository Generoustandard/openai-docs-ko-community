# OpenAI Docs Korean Community

이 저장소는 `openai.com`에 게시된 공식 OpenAI 영어-한국어 문서 쌍을 기준으로 한국어 번역 품질을 평가하기 위한 Phase 1 MVP입니다.

이 MVP의 목적은 먼저 reference가 분명한 공식 EN-KO 페이지 쌍에서 평가 프레임워크를 검증한 뒤, 같은 틀을 `developers.openai.com`으로 확장하는 것입니다. 개발자 문서 영역은 한국어 reference가 제한적이기 때문에, 이후에는 reference-less evaluation과 커뮤니티 리뷰가 더 중요해집니다.

이 저장소에서 Codex는 `candidate_ko` 생성, 평가 워크플로 지원, 그리고 이후 에이전트 기반 개선 루프를 준비하는 데 사용됩니다.

## Phase 범위

### Phase 1 MVP

Phase 1은 의도적으로 범위를 좁게 잡고 있습니다.

- 공식 영어 페이지를 `source_en`으로 수집
- 해당 페이지의 공식 한국어 페이지를 `reference_ko`로 수집
- 안정적인 문단 단위 평가 블록으로 정렬
- 새로운 한국어 번역 `candidate_ko` 생성
- `candidate_ko`를 `reference_ko`와 비교
- 기계 판독용 결과와 사람이 읽는 보고서 저장

현재 평가 역할은 다음과 같습니다.

| 역할 | 의미 |
| --- | --- |
| `source_en` | OpenAI 공식 영어 원문 |
| `reference_ko` | OpenAI가 게시한 공식 한국어 번역 |
| `candidate_ko` | 파이프라인이 새로 생성한 한국어 번역 |
| `improved_candidate_ko` | 평가 또는 검토 이후에 만든 후속 개선안 |
| `reviewed_golden` | 회귀 테스트나 심화 평가용으로 사람이 검토해 둘 수 있는 예시 |

중요한 원칙:

- `reference_ko`는 reference이지 자동으로 golden이 아닙니다.
- `candidate_ko`는 golden으로 저장하지 않습니다.
- `improved_candidate_ko`도 여전히 candidate 출력이며 golden이 아닙니다.
- 유지보수자 또는 커뮤니티 검토자가 수동 검토한 경우에만 `reviewed_golden`으로 승격할 수 있습니다.

### Phase 2 확장

Phase 2는 현재 MVP가 아니라, 같은 프레임워크의 다음 확장 단계입니다.

- `developers.openai.com` 수집 경로 추가
- 한국어 reference가 없는 문서에 대한 reference-less evaluation
- 더 강한 커뮤니티 리뷰 및 승격 워크플로
- 더 다양한 candidate 생성 경로
- curated `reviewed_golden` 자산 확장

## 왜 공식 EN-KO 페이지 쌍부터 시작하는가

공식 `openai.com` 영어-한국어 페이지 쌍은 평가 설계를 검증하기에 더 명확한 reference 경로를 제공합니다. 덕분에 개발자 문서처럼 reference 신호가 약한 영역으로 넘어가기 전에, 정렬, 점수화, 보고서 생성, 사람 검토 규칙을 더 분명하게 점검할 수 있습니다.

## 평가 프레이밍

이 저장소는 현재 서로 호환되는 두 가지 평가 레이어를 가집니다.

- 공식 문서 쌍 평가: 현재 Phase 1 `openai.com` 페이지 쌍에 대해 `candidate_ko`를 공식 `reference_ko`와 비교
- golden 예시 평가: `docs/golden/` 아래의 단어, 문장, 문단 example bank 중 `reviewed_golden_candidate`로 표시된 소규모 target만 골라 생성 결과와 비교

핵심 정량 신호는 OpenAI가 제안한 방향과 맞춰져 있습니다.

- 한국어 측 cosine similarity: 생성된 한국어와 reference에 가까운 한국어 target을 비교
  Phase 1 공식 문서 쌍 MVP에서는 그 target이 `reference_ko`입니다.
  경량 회귀 체크에서는 curated golden 한국어가 target입니다.
- backtranslation cosine similarity: `source_en`과 생성 한국어를 다시 영어로 옮긴 결과를 비교
- 비교용 메타데이터: `run_label`, `pipeline_label`, `prompt_label` 같은 값을 남겨 두어 이후 모델, 프롬프트, 파이프라인 비교에 활용

구분해야 할 점:

- `reference_ko`는 현재 Phase 1 공식 페이지 평가를 위한 페이지 단위 reference입니다.
- `reviewed_golden`은 sanity check와 regression-style comparison을 위한 소규모 curated evaluation target입니다.
- `docs/golden/*.json`의 나머지 항목은 example bank이며, 현재 평가 target이 아닙니다.
- raw `candidate_ko`나 `improved_candidate_ko`는 자동으로 golden 취급하지 않습니다.

## 현재 데모 문서 쌍

- 영어: [why-we-no-longer-evaluate-swe-bench-verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- 한국어: [why-we-no-longer-evaluate-swe-bench-verified (ko-KR)](https://openai.com/ko-KR/index/why-we-no-longer-evaluate-swe-bench-verified/)

## Codex가 사용되는 위치

- Candidate 생성: 정렬된 `source_en` 블록에서 `candidate_ko` 생성
- 평가 워크플로 지원: backtranslation, LLM judging, 점수화, 보고서 생성
- 반복 개선 경로: 작은 golden-set 체크를 유지하면서 `candidate_ko -> evaluation -> improved_candidate_ko -> human review` 방향을 지원

## Improvement-Loop 방향

현재 Phase 1 MVP는 먼저 raw `candidate_ko` 평가를 검증하는 데 집중합니다. 다음 단계는 아래와 같은 경량 개선 경로입니다.

- `candidate_ko` 평가
- 필요하면 `improved_candidate_ko` 생성
- 필요하면 다시 평가
- 사람이 검토한 항목만 `reviewed_golden` 후보로 승격

이 다음 단계 역시 같은 cosine similarity, backtranslation, reviewed-golden 체크와 호환됩니다.

## 권장 실행 순서

사전 조건:

- Python 3.11+
- Chrome 설치
- `OPENAI_API_KEY` 설정
- `pip install -r requirements.txt`

현재 권장 MVP 데모 설정:

- `generation_model`: `gpt-5.4-mini`
- `backtranslation_model`: `gpt-5.4-mini`
- `judge_model`: `gpt-5.4-mini`

권장 실행 순서:

```powershell
python -X utf8 collect_pair.py --slug why-we-no-longer-evaluate-swe-bench-verified --source-url https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ --reference-url https://openai.com/ko-KR/index/why-we-no-longer-evaluate-swe-bench-verified/
python -X utf8 align_units.py --slug why-we-no-longer-evaluate-swe-bench-verified
python -X utf8 generate_candidate.py --input data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json --model gpt-5.4-mini
python -X utf8 run_eval.py --input data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json --backtranslation-model gpt-5.4-mini --judge-model gpt-5.4-mini --embedding-model text-embedding-3-small
python -X utf8 build_report.py --input reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json --output reports/why-we-no-longer-evaluate-swe-bench-verified.report.md
```

참고:

- `collect_pair.py`는 현재 `openai.com` 페이지에 대해 Chrome 기반 비헤드리스 실행이 가장 안전합니다.
- 스크립트 기본값도 `gpt-5.4-mini`를 가리키지만, 검토자가 보기에 명확하도록 위 명령에서는 권장 설정을 명시적으로 적었습니다.
- Windows에서는 `python -X utf8` 대신 `py -3 -X utf8`를 써도 됩니다.

## Golden Example Checks

curated 또는 future-curated reviewed-golden 레이어는 [docs/golden/README.md](docs/golden/README.md)에 설명되어 있으며, 다음 자산으로 구성됩니다.

- [docs/golden/words.json](docs/golden/words.json)
- [docs/golden/sentences.json](docs/golden/sentences.json)
- [docs/golden/paragraphs.json](docs/golden/paragraphs.json)

이 예시들은 Phase 1 공식 페이지 reference를 대체하는 것이 아니라, 경량 비교와 회귀 체크를 위한 평가 자산입니다.

현재는 각 파일 전체를 evaluation target으로 쓰지 않고, `target_role: reviewed_golden_candidate`로 표시된 7개 항목만 review target 후보로 사용합니다. 나머지 항목은 `example_only` 상태의 example bank로 남겨 둡니다.

예시 golden-set 실행:

```powershell
python -X utf8 run_golden_eval.py --golden-set sentences --generation-model gpt-5.4-mini --backtranslation-model gpt-5.4-mini --embedding-model text-embedding-3-small --run-label sentences-baseline --pipeline-label baseline --prompt-label official_openai_style_translation_v1
```

이미 후속 개선 출력이 있다면, 입력 파일의 다른 필드를 평가할 수도 있습니다.

```powershell
python -X utf8 run_golden_eval.py --golden-set paragraphs --input path/to/candidates.json --candidate-field improved_candidate_ko --backtranslation-model gpt-5.4-mini --embedding-model text-embedding-3-small --run-label paragraphs-improved
```

## Human Review Artifact

최소 human review artifact는 [reviews/phase1_pair_review.md](reviews/phase1_pair_review.md)에 정리합니다.

- 이 파일은 현재 Phase 1 pair eval에서 사람이 다시 봐야 할 블록을 모아 둔 review worksheet입니다.
- `source_en`, `reference_ko`, `candidate_ko`, `decision`, `reviewed_golden_ko`, `notes`를 함께 기록합니다.
- 여기 적힌 `reviewed_golden_ko`는 maintainer 확인 전까지 draft 제안값이며, 자동으로 승격되지 않습니다.

## 체크인된 샘플 산출물

현재 데모 문서 쌍에 대한 샘플 산출물은 `docs/pairs/`, `data/processed/`, `reports/` 아래에 유지됩니다.

체크인된 샘플 candidate, evaluation, report 산출물은 현재 Phase 1 MVP 데모 설정 기준으로 갱신되어 있습니다.

- `generation_model`: `gpt-5.4-mini`
- `backtranslation_model`: `gpt-5.4-mini`
- `judge_model`: `gpt-5.4-mini`

현재 체크인된 데모 실행의 provenance는 각 산출물에 기록된 timestamp와 metadata를 기준으로 봐야 합니다.

주요 샘플 파일:

- [docs/pairs/why-we-no-longer-evaluate-swe-bench-verified/pair_manifest.json](docs/pairs/why-we-no-longer-evaluate-swe-bench-verified/pair_manifest.json)
- [data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json](data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.json)
- [data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json](data/processed/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.json)
- [reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json](reports/why-we-no-longer-evaluate-swe-bench-verified.aligned.candidates.eval.json)
- [reports/why-we-no-longer-evaluate-swe-bench-verified.report.md](reports/why-we-no-longer-evaluate-swe-bench-verified.report.md)

## 저장소 안내

- [AGENTS.md](AGENTS.md): 저장소 운영 메모
- [PLAN.md](PLAN.md): 현재 단계와 다음 작업
- [EVAL_SPEC.md](EVAL_SPEC.md): Phase 1 평가 명세
- [reviews/phase1_pair_review.md](reviews/phase1_pair_review.md): 최소 human review worksheet
- [evals/README.md](evals/README.md): 보존 중인 레거시 실험 평가 경로

## 기존 실험 자산

`docs/golden/`과 `evals/` 아래의 기존 파일은 그대로 보존합니다. `docs/golden/`의 curated 파일은 이제 lightweight reviewed-golden 평가 레이어를 지원하고, `evals/`는 메인 Phase 1 MVP가 아니라 레거시 실험 경로로 남겨 둡니다.
