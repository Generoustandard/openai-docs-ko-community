# Phase 1 Pair Review Worksheet

This file is a minimal human review artifact for the `why-we-no-longer-evaluate-swe-bench-verified` pair.

- Purpose: collect the Phase 1 pair items that need maintainer review before any promotion step.
- Status: every `decision` below is `pending_human_review`, so nothing in this file is an approved `reviewed_golden` yet.
- `reviewed_golden_ko`: draft proposal based on the current eval `suggested_revision`; a maintainer must confirm or edit it before promotion.

## why-we-no-longer-evaluate-swe-bench-verified.block-001

- decision: `pending_human_review`
- overall_score: `92.8`

### source_en

Since we first published SWE-bench Verified in August 2024, the industry has widely used it to measure the progress of models on autonomous software engineering tasks. After its release, SWE-bench Verified provided a strong signal of capability progress and became a standard metric reported in frontier model releases. Tracking and forecasting progress of these capabilities is also an important part of OpenAI’s Preparedness Framework. When we created the Verified benchmark initially, we attempted to solve issues in the original evaluation that made certain tasks impossible to accomplish in the SWE-bench dataset.

### reference_ko

2024년 8월 SWE-bench Verified를 처음 발표한 이후, 업계에서는 자율 소프트웨어 엔지니어링 작업에 대한 모델의 발전을 측정하는 데 이를 널리 사용해 왔습니다. 출시 이후, SWE-bench Verified는 역량 향상의 강력한 지표를 제공했으며 프런티어 모델 출시 시 보고되는 표준 지표가 되었습니다. 이러한 역량의 발전을 추적하고 예측하는 것은 OpenAI의 준비성 평가 프레임워크의 중요한 부분이기도 합니다. 처음 Verified 벤치마크를 구축할 당시, SWE-bench 데이터세트 에서 특정 작업 완료를 불가능하게 만들었던 원본 평가의 문제점을 해결하고자 했습니다.

### candidate_ko

2024년 8월 SWE-bench Verified를 처음 공개한 이후, 업계에서는 이를 자율 소프트웨어 엔지니어링 작업에서 모델의 진전을 측정하는 지표로 널리 사용해 왔습니다. 출시 이후 SWE-bench Verified는 역량 발전을 보여주는 강력한 신호를 제공했으며, 최첨단 모델 공개에서 보고되는 표준 지표가 되었습니다. 이러한 역량의 진전을 추적하고 예측하는 일은 OpenAI의 Preparedness Framework에서도 중요한 부분입니다. 당초 Verified 벤치마크를 만들 때, SWE-bench 데이터셋의 일부 작업을 해결 불가능하게 만들던 기존 평가상의 문제를 해결하려고 했습니다.

### reviewed_golden_ko (draft)

2024년 8월 SWE-bench Verified를 처음 공개한 이후, 업계에서는 이를 자율 소프트웨어 엔지니어링 작업에서 모델의 진전을 측정하는 지표로 널리 사용해 왔습니다. 출시 이후 SWE-bench Verified는 역량 발전을 보여주는 강력한 신호를 제공했으며, 최첨단 모델 공개에서 보고되는 표준 지표가 되었습니다. 이러한 역량의 진전을 추적하고 예측하는 일은 OpenAI의 Preparedness Framework에서도 중요한 부분입니다. 당초 Verified 벤치마크를 만들 때, SWE-bench 데이터셋의 일부 작업을 해결 불가능하게 만들던 기존 평가상의 문제를 해결하려고 했습니다.

### notes

- Terminology mismatch: expected a consistent rendering for 'frontier'.
- Maintainer confirmation required before any promotion to `reviewed_golden`.

## why-we-no-longer-evaluate-swe-bench-verified.block-003

- decision: `pending_human_review`
- overall_score: `82.4`

### source_en

In a new analysis, we found two major issues with the Verified set that indicate the benchmark is no longer suitable for measuring progress on autonomous software engineering capabilities for frontier launches at today’s performance levels:

### reference_ko

새로운 분석 결과, Verified 데이터세트에서 두 가지 주요 문제를 발견했습니다. 이는 현재의 성능 수준에서 프런티어 모델 출시에 수반되는 자율 소프트웨어 엔지니어링 역량 발전을 측정하는 데 해당 벤치마크가 더 이상 적합하지 않음을 시사합니다.

### candidate_ko

새로운 분석에서 우리는 Verified 세트에 두 가지 주요 문제가 있음을 확인했으며, 이는 이 벤치마크가 더 이상 오늘날의 성능 수준에서 최첨단 출시를 위한 자율 소프트웨어 엔지니어링 역량의 진전을 측정하는 데 적합하지 않음을 시사합니다:

### reviewed_golden_ko (draft)

새로운 분석에서 우리는 Verified 세트에 두 가지 주요 문제가 있음을 확인했으며, 이는 이 벤치마크가 더 이상 오늘날의 성능 수준에서 프런티어 출시를 위한 자율 소프트웨어 엔지니어링 역량의 진전을 측정하는 데 적합하지 않음을 시사합니다.

### notes

- Terminology mismatch: expected a consistent rendering for 'frontier'.
- 문장 끝의 콜론(:)이 원문 대비 부자연스럽게 남아 있습니다.
- "최첨단 출시"는 원문의 frontier launches보다 다소 어색합니다.
- Maintainer confirmation required before any promotion to `reviewed_golden`.

## why-we-no-longer-evaluate-swe-bench-verified.block-005

- decision: `pending_human_review`
- overall_score: `81.2`

### source_en

Training on solutions: Because large frontier models can learn information from their training, it is important that they are never trained on problems and solutions they are evaluated on. This is akin to sharing problems and solutions for an upcoming test with students before the test - they may not memorize the answer but students who have seen the answers before will certainly do better than those without. SWE-bench problems are sourced from open-source repositories many model providers use for training purposes. In our analysis we found that all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference, known as the gold patch, or verbatim problem statement specifics for certain tasks, indicating that all of them have seen at least some of the problems and solutions during training.

### reference_ko

해답 학습: 대규모 프런티어 모델은 학습 과정을 통해 정보를 습득할 수 있으므로, 평가 대상이 되는 문제와 해답으로 모델을 절대 학습시키지 않는 것이 중요합니다. 이는 앞으로 치를 시험의 문제와 해답을 시험 전에 학생에게 공유하는 것과 같습니다. 정답을 통째로 외우지는 않더라도, 해답을 미리 본 학생은 그렇지 않은 학생보다 당연히 더 좋은 성적을 거둘 것입니다. SWE-bench 문제는 많은 모델 제공업체가 학습 목적으로 사용하는 오픈 소스 리포지터리에서 추출됩니다. 이번 분석 결과, 테스트한 모든 프런티어 모델이 정답 기준으로 사용된, 사람이 작성한 원본 버그 수정(골드 패치)을 재현해 내거나 특정 작업의 문제 명세 세부 사항을 글자 그대로 재현할 수 있었으며, 이는 모든 모델이 학습 과정에서 최소한 일부 문제와 해답을 접했음을 나타냅니다.

### candidate_ko

해결책에 대한 학습: 대형 최첨단 모델은 학습 과정에서 정보를 습득할 수 있으므로, 평가 대상인 문제와 해결책을 학습하지 않도록 하는 것이 매우 중요합니다. 이는 학생들에게 시험 전에 예정된 시험의 문제와 답을 미리 공유하는 것과 비슷합니다. 정답을 외우지 못할 수도 있지만, 답을 미리 본 학생이 그렇지 않은 학생보다 분명히 더 좋은 성과를 낼 것입니다. SWE-bench 문제는 많은 모델 제공업체가 학습 목적으로 사용하는 오픈소스 저장소에서 출처를 가져옵니다. 우리의 분석에서 테스트한 모든 최첨단 모델은 정답 참조로 사용되는 원래의 인간 작성 버그 수정, 즉 gold patch, 또는 특정 작업에 대한 문제 설명의 세부 사항을 그대로 재현할 수 있었으며, 이는 이들 모두가 학습 과정에서 적어도 일부 문제와 해결책을 보았음을 보여줍니다.

### reviewed_golden_ko (draft)

해답 학습: 대규모 프런티어 모델은 학습 과정에서 정보를 습득할 수 있으므로, 평가 대상이 되는 문제와 해답으로 모델을 절대 학습시키지 않는 것이 중요합니다. 이는 앞으로 치를 시험의 문제와 해답을 시험 전에 학생에게 공유하는 것과 같습니다. 정답을 통째로 외우지는 않더라도, 해답을 미리 본 학생은 그렇지 않은 학생보다 당연히 더 좋은 성적을 거둘 것입니다. SWE-bench 문제는 많은 모델 제공업체가 학습 목적으로 사용하는 오픈소스 리포지터리에서 추출됩니다. 이번 분석에서 테스트한 모든 프런티어 모델은 정답 기준인 사람이 작성한 원본 버그 수정인 gold patch 또는 특정 작업의 문제 설명 세부 사항을 글자 그대로 재현할 수 있었으며, 이는 이들 모두가 학습 과정에서 최소한 일부 문제와 해답을 접했음을 보여줍니다.

### notes

- Terminology mismatch: expected a consistent rendering for 'frontier'.
- "대형 최첨단 모델"은 원문의 large frontier models보다 다소 어색합니다.
- "정답 참조로 사용되는 원래의 인간 작성 버그 수정"은 용어가 장황하고 다소 부자연스럽습니다.
- "문제 설명의 세부 사항"은 original problem statement specifics의 뉘앙스를 충분히 살리지 못합니다.
- Maintainer confirmation required before any promotion to `reviewed_golden`.

## why-we-no-longer-evaluate-swe-bench-verified.block-040

- decision: `pending_human_review`
- overall_score: `85.7`

### source_en

Gemini 3 Flash, when given no further information regarding the task besides the ID, is able to output verbatim details from the task description and the gold patch. This includes the new regex formula for username validation and the exact line numbers for the change.

### reference_ko

Gemini 3 Flash는 작업 ID 외에 작업에 대한 추가 정보가 주어지지 않았음에도, 작업 설명과 골드 패치의 세부 내용을 글자 그대로 출력할 수 있습니다. 여기에는 사용자 이름 유효성 검사를 위한 새로운 정규식과 변경 사항의 정확한 줄 번호가 포함됩니다.

### candidate_ko

Gemini 3 Flash는 과제 ID 외에 추가 정보가 전혀 주어지지 않아도, 과제 설명과 골드 패치의 세부 사항을 그대로 출력할 수 있습니다. 여기에는 사용자 이름 검증을 위한 새 regex 수식과 변경된 정확한 줄 번호가 포함됩니다.

### reviewed_golden_ko (draft)

Gemini 3 Flash는 과제 ID 외에 추가 정보가 전혀 주어지지 않아도, 과제 설명과 골드 패치의 세부 사항을 그대로 출력할 수 있습니다. 여기에는 사용자 이름 검증을 위한 새로운 정규식과 변경 사항의 정확한 줄 번호가 포함됩니다.

### notes

- "regex"는 번역어로 남기기보다 한국어 문맥에 맞게 "정규식"으로 통일하는 편이 자연스럽습니다.
- "골드 패치"는 의미는 전달되지만 기술 문서에서는 "정답 패치" 또는 원문 용어 일관성을 더 점검할 여지가 있습니다.
- "변경된 정확한 줄 번호"는 어색하므로 "변경 사항의 정확한 줄 번호"처럼 다듬는 것이 좋습니다.
- Maintainer confirmation required before any promotion to `reviewed_golden`.

## why-we-no-longer-evaluate-swe-bench-verified.block-041

- decision: `pending_human_review`
- overall_score: `82.2`

### source_en

Task ID: django__django-11099

### reference_ko

작업 ID: django__django-11099

### candidate_ko

Task ID: django__django-11099

### reviewed_golden_ko (draft)

작업 ID: django__django-11099

### notes

- Falls back to English instead of Korean, which is inappropriate for the target publication.
- Terminology/style mismatch: should use Korean translation for Task ID.
- Maintainer confirmation required before any promotion to `reviewed_golden`.
