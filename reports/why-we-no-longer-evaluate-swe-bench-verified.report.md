# Translation Evaluation Report

## Pair

- pair_slug: `why-we-no-longer-evaluate-swe-bench-verified`
- unit_count: 46
- score_scale: `0-100`
- overall_formula: `0.30 * semantic_similarity_score + 0.25 * backtranslation_similarity_score + 0.15 * terminology_consistency_score + 0.30 * llm_judge_score`

## Artifact Provenance

- generated_at: `2026-04-05T03:38:20.863013+00:00`
- evaluated_at: `2026-04-05T03:41:24.997727+00:00`
- generation_model: `gpt-5.4-mini`
- backtranslation_model: `gpt-5.4-mini`
- judge_model: `gpt-5.4-mini`
- embedding_model: `text-embedding-3-small`

## Document Summary

- average_overall_score: 93.0
- average_semantic_similarity_score: 88.9
- average_backtranslation_similarity_score: 95.6
- average_terminology_consistency_score: 97.3
- average_llm_judge_score: 93.0
- human_review_count: 5

## Top 5 Problem Items

- `why-we-no-longer-evaluate-swe-bench-verified.block-005` | overall=81.2
  source: Training on solutions: Because large frontier models can learn information from their training, it is important that they are never trained on problems and solutions they are evaluated on. This is akin to sharing problems and solutions for an upcoming test with students before the test - they may not memorize the answer but students who have seen the answers before will certainly do better than those without. SWE-bench problems are sourced from open-source repositories many model providers use for training purposes. In our analysis we found that all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference, known as the gold patch, or verbatim problem statement specifics for certain tasks, indicating that all of them have seen at least some of the problems and solutions during training.
  candidate: 해결책에 대한 학습: 대형 최첨단 모델은 학습 과정에서 정보를 습득할 수 있으므로, 평가 대상인 문제와 해결책을 학습하지 않도록 하는 것이 매우 중요합니다. 이는 학생들에게 시험 전에 예정된 시험의 문제와 답을 미리 공유하는 것과 비슷합니다. 정답을 외우지 못할 수도 있지만, 답을 미리 본 학생이 그렇지 않은 학생보다 분명히 더 좋은 성과를 낼 것입니다. SWE-bench 문제는 많은 모델 제공업체가 학습 목적으로 사용하는 오픈소스 저장소에서 출처를 가져옵니다. 우리의 분석에서 테스트한 모든 최첨단 모델은 정답 참조로 사용되는 원래의 인간 작성 버그 수정, 즉 gold patch, 또는 특정 작업에 대한 문제 설명의 세부 사항을 그대로 재현할 수 있었으며, 이는 이들 모두가 학습 과정에서 적어도 일부 문제와 해결책을 보았음을 보여줍니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., "대형 최첨단 모델"은 원문의 large frontier models보다 다소 어색합니다., "정답 참조로 사용되는 원래의 인간 작성 버그 수정"은 용어가 장황하고 다소 부자연스럽습니다., "문제 설명의 세부 사항"은 original problem statement specifics의 뉘앙스를 충분히 살리지 못합니다.
- `why-we-no-longer-evaluate-swe-bench-verified.block-041` | overall=82.2
  source: Task ID: django__django-11099
  candidate: Task ID: django__django-11099
  issues: Falls back to English instead of Korean, which is inappropriate for the target publication., Terminology/style mismatch: should use Korean translation for Task ID.
- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | overall=82.4
  source: In a new analysis, we found two major issues with the Verified set that indicate the benchmark is no longer suitable for measuring progress on autonomous software engineering capabilities for frontier launches at today’s performance levels:
  candidate: 새로운 분석에서 우리는 Verified 세트에 두 가지 주요 문제가 있음을 확인했으며, 이는 이 벤치마크가 더 이상 오늘날의 성능 수준에서 최첨단 출시를 위한 자율 소프트웨어 엔지니어링 역량의 진전을 측정하는 데 적합하지 않음을 시사합니다:
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., 문장 끝의 콜론(:)이 원문 대비 부자연스럽게 남아 있습니다., "최첨단 출시"는 원문의 frontier launches보다 다소 어색합니다.
- `why-we-no-longer-evaluate-swe-bench-verified.block-019` | overall=83.6
  source: Too narrow and too wide tests
  candidate: 너무 좁고 너무 넓은 테스트
  issues: none
- `why-we-no-longer-evaluate-swe-bench-verified.block-040` | overall=85.7
  source: Gemini 3 Flash, when given no further information regarding the task besides the ID, is able to output verbatim details from the task description and the gold patch. This includes the new regex formula for username validation and the exact line numbers for the change.
  candidate: Gemini 3 Flash는 과제 ID 외에 추가 정보가 전혀 주어지지 않아도, 과제 설명과 골드 패치의 세부 사항을 그대로 출력할 수 있습니다. 여기에는 사용자 이름 검증을 위한 새 regex 수식과 변경된 정확한 줄 번호가 포함됩니다.
  issues: "regex"는 번역어로 남기기보다 한국어 문맥에 맞게 "정규식"으로 통일하는 편이 자연스럽습니다., "골드 패치"는 의미는 전달되지만 기술 문서에서는 "정답 패치" 또는 원문 용어 일관성을 더 점검할 여지가 있습니다., "변경된 정확한 줄 번호"는 어색하므로 "변경 사항의 정확한 줄 번호"처럼 다듬는 것이 좋습니다.

## Terminology Mismatch Examples

- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | terminology_consistency_score=50.0
  source: In a new analysis, we found two major issues with the Verified set that indicate the benchmark is no longer suitable for measuring progress on autonomous software engineering capabilities for frontier launches at today’s performance levels:
  candidate: 새로운 분석에서 우리는 Verified 세트에 두 가지 주요 문제가 있음을 확인했으며, 이는 이 벤치마크가 더 이상 오늘날의 성능 수준에서 최첨단 출시를 위한 자율 소프트웨어 엔지니어링 역량의 진전을 측정하는 데 적합하지 않음을 시사합니다:
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., 문장 끝의 콜론(:)이 원문 대비 부자연스럽게 남아 있습니다., "최첨단 출시"는 원문의 frontier launches보다 다소 어색합니다.
- `why-we-no-longer-evaluate-swe-bench-verified.block-005` | terminology_consistency_score=50.0
  source: Training on solutions: Because large frontier models can learn information from their training, it is important that they are never trained on problems and solutions they are evaluated on. This is akin to sharing problems and solutions for an upcoming test with students before the test - they may not memorize the answer but students who have seen the answers before will certainly do better than those without. SWE-bench problems are sourced from open-source repositories many model providers use for training purposes. In our analysis we found that all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference, known as the gold patch, or verbatim problem statement specifics for certain tasks, indicating that all of them have seen at least some of the problems and solutions during training.
  candidate: 해결책에 대한 학습: 대형 최첨단 모델은 학습 과정에서 정보를 습득할 수 있으므로, 평가 대상인 문제와 해결책을 학습하지 않도록 하는 것이 매우 중요합니다. 이는 학생들에게 시험 전에 예정된 시험의 문제와 답을 미리 공유하는 것과 비슷합니다. 정답을 외우지 못할 수도 있지만, 답을 미리 본 학생이 그렇지 않은 학생보다 분명히 더 좋은 성과를 낼 것입니다. SWE-bench 문제는 많은 모델 제공업체가 학습 목적으로 사용하는 오픈소스 저장소에서 출처를 가져옵니다. 우리의 분석에서 테스트한 모든 최첨단 모델은 정답 참조로 사용되는 원래의 인간 작성 버그 수정, 즉 gold patch, 또는 특정 작업에 대한 문제 설명의 세부 사항을 그대로 재현할 수 있었으며, 이는 이들 모두가 학습 과정에서 적어도 일부 문제와 해결책을 보았음을 보여줍니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., "대형 최첨단 모델"은 원문의 large frontier models보다 다소 어색합니다., "정답 참조로 사용되는 원래의 인간 작성 버그 수정"은 용어가 장황하고 다소 부자연스럽습니다., "문제 설명의 세부 사항"은 original problem statement specifics의 뉘앙스를 충분히 살리지 못합니다.
- `why-we-no-longer-evaluate-swe-bench-verified.block-001` | terminology_consistency_score=75.0
  source: Since we first published SWE-bench Verified in August 2024, the industry has widely used it to measure the progress of models on autonomous software engineering tasks. After its release, SWE-bench Verified provided a strong signal of capability progress and became a standard metric reported in frontier model releases. Tracking and forecasting progress of these capabilities is also an important part of OpenAI’s Preparedness Framework. When we created the Verified benchmark initially, we attempted to solve issues in the original evaluation that made certain tasks impossible to accomplish in the SWE-bench dataset.
  candidate: 2024년 8월 SWE-bench Verified를 처음 공개한 이후, 업계에서는 이를 자율 소프트웨어 엔지니어링 작업에서 모델의 진전을 측정하는 지표로 널리 사용해 왔습니다. 출시 이후 SWE-bench Verified는 역량 발전을 보여주는 강력한 신호를 제공했으며, 최첨단 모델 공개에서 보고되는 표준 지표가 되었습니다. 이러한 역량의 진전을 추적하고 예측하는 일은 OpenAI의 Preparedness Framework에서도 중요한 부분입니다. 당초 Verified 벤치마크를 만들 때, SWE-bench 데이터셋의 일부 작업을 해결 불가능하게 만들던 기존 평가상의 문제를 해결하려고 했습니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'.

## Backtranslation Mismatch Examples

- `why-we-no-longer-evaluate-swe-bench-verified.block-019` | backtranslation_similarity_score=81.2
  source: Too narrow and too wide tests
  candidate: 너무 좁고 너무 넓은 테스트
  issues: none
- `why-we-no-longer-evaluate-swe-bench-verified.block-016` | backtranslation_similarity_score=87.3
  source: Many task statements were underspecified, which could lead to multiple valid interpretations - while the tests only covered a specific one.
  candidate: 많은 과제 설명이 충분히 구체적이지 않아 여러 가지 유효한 해석이 가능했지만, 테스트는 그중 특정한 하나만을 다루고 있었습니다.
  issues: none
- `why-we-no-longer-evaluate-swe-bench-verified.block-024` | backtranslation_similarity_score=87.4
  source: The remaining 5.1% of tasks had miscellaneous issues that were not well grouped with this taxonomy.
  candidate: 나머지 5.1%의 작업에는 이 분류 체계로는 잘 묶이지 않는 기타 문제가 있었습니다.
  issues: none
- `why-we-no-longer-evaluate-swe-bench-verified.block-014` | backtranslation_similarity_score=87.6
  source: We found many issues with that evaluation that could lead to underreporting the capability of models.
  candidate: 우리는 이 평가에 모델의 능력을 과소평가하게 만들 수 있는 여러 문제를 발견했습니다.
  issues: none
- `why-we-no-longer-evaluate-swe-bench-verified.block-017` | backtranslation_similarity_score=89.1
  source: Depending on setup of the environment (for example Linux vs Windows, or the python version), some tests could spuriously fail
  candidate: 환경 설정에 따라(예: Linux vs Windows, 또는 python 버전) 일부 테스트가 우연히 실패할 수 있습니다
  issues: 영문 현재형("can")에 비해 한국어가 과거형처럼 읽힐 수 있습니다., "우연히 실패"는 원문의 "spuriously fail" 의미를 잘 전달하지만, 공식 문체에서는 "오탐으로 실패"가 더 자연스럽습니다.

## Human Review Queue

- `why-we-no-longer-evaluate-swe-bench-verified.block-001` | overall=92.8 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | overall=82.4 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-005` | overall=81.2 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-040` | overall=85.7 | reasons: llm_judge_score < 75
- `why-we-no-longer-evaluate-swe-bench-verified.block-041` | overall=82.2 | reasons: llm_judge_score < 75
