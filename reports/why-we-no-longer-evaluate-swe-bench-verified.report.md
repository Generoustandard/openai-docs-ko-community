# Translation Evaluation Report

## Pair

- pair_slug: `why-we-no-longer-evaluate-swe-bench-verified`
- unit_count: 46
- score_scale: `0-100`
- overall_formula: `0.30 * semantic_similarity_score + 0.25 * backtranslation_similarity_score + 0.15 * terminology_consistency_score + 0.30 * llm_judge_score`

## Artifact Provenance

- generated_at: `2026-03-31T16:59:18.814737+00:00`
- evaluated_at: `2026-03-31T17:02:52.303607+00:00`
- generation_model: `gpt-4.1-mini`
- backtranslation_model: `gpt-4.1-mini`
- judge_model: `gpt-4.1-mini`
- embedding_model: `text-embedding-3-small`

> Note: This report reflects a historical sample run. The current recommended MVP demo configuration uses `gpt-5.4-mini` for generation, backtranslation, and judging.

## Document Summary

- average_overall_score: 92.4
- average_semantic_similarity_score: 89.0
- average_backtranslation_similarity_score: 93.5
- average_terminology_consistency_score: 91.1
- average_llm_judge_score: 95.6
- human_review_count: 7

## Top 5 Problem Items

- `why-we-no-longer-evaluate-swe-bench-verified.block-040` | overall=80.5
  source: Gemini 3 Flash, when given no further information regarding the task besides the ID, is able to output verbatim details from the task description and the gold patch. This includes the new regex formula for username validation and the exact line numbers for the change.
  candidate: Gemini 3 Flash는 작업 ID 외에 추가 정보가 주어지지 않아도 작업 설명과 정답 패치의 내용을 문자 그대로 출력할 수 있습니다. 여기에는 사용자명 검증을 위한 새로운 정규식 공식과 변경된 정확한 라인 번호가 포함됩니다.
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., '정답 패치' term less appropriate than '골드 패치', '공식' less natural than '식' in regex context
- `why-we-no-longer-evaluate-swe-bench-verified.block-034` | overall=80.7
  source: Given a short snippet from the task description, GPT‑5.2 outputs the exact gold patch. In particular, it knows the exact class and method name, and the new early return condition `if username is None or password is None` that is introduced.
  candidate: 작업 설명의 짧은 스니펫만으로 GPT‑5.2는 정확한 정답 패치를 출력합니다. 특히, 정확한 클래스와 메서드 이름, 그리고 새로 도입된 조기 반환 조건인 `if username is None or password is None`을 알고 있습니다.
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., '정답 패치'보다 '골드 패치'가 번역 스타일과 전문성에 더 부합할 수 있음
- `why-we-no-longer-evaluate-swe-bench-verified.block-005` | overall=80.9
  source: Training on solutions: Because large frontier models can learn information from their training, it is important that they are never trained on problems and solutions they are evaluated on. This is akin to sharing problems and solutions for an upcoming test with students before the test - they may not memorize the answer but students who have seen the answers before will certainly do better than those without. SWE-bench problems are sourced from open-source repositories many model providers use for training purposes. In our analysis we found that all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference, known as the gold patch, or verbatim problem statement specifics for certain tasks, indicating that all of them have seen at least some of the problems and solutions during training.
  candidate: 해결책의 훈련 포함: 대규모 최첨단 모델은 훈련에서 정보를 학습할 수 있으므로, 평가 대상인 문제와 해결책에 대해 절대 훈련하면 안 됩니다. 이는 다가오는 시험 문제와 답을 학생들에게 미리 공유하는 것과 유사합니다. 학생들이 답을 외우지 않더라도 이전에 답을 본 학생들이 그렇지 않은 학생보다 성적이 더 좋을 것입니다. SWE-bench 문제들은 많은 모델 제공자가 훈련 목적으로 사용하는 오픈소스 저장소에서 수집되었습니다. 분석 결과, 우리가 테스트한 모든 최첨단 모델들은 기준 진실 참조로 사용되는 원본 인간 작성 버그 수정(골드 패치)이나 특정 과제의 문제 문구를 말 그대로 재현할 수 있었으며, 이는 모든 모델이 훈련 중 최소 일부 문제와 해결책을 접했다는 것을 나타냅니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., '해결책의 훈련 포함' is somewhat unnatural; '해답 학습' or '해답 포함' preferred., Minor terminology nuance on 'gold patch' translation chosen as '골드 패치' rather than localized term.
- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | overall=83.6
  source: In a new analysis, we found two major issues with the Verified set that indicate the benchmark is no longer suitable for measuring progress on autonomous software engineering capabilities for frontier launches at today’s performance levels:
  candidate: 새로운 분석에서 우리는 Verified 세트에 두 가지 주요 문제가 있음을 발견했으며, 이는 현재 성능 수준의 최첨단 출시 모델들을 위한 자율 소프트웨어 엔지니어링 능력 측정에 이 벤치마크가 더 이상 적합하지 않다는 것을 시사합니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., '최첨단 출시 모델들' 표현이 '프런티어 모델 출시에 수반되는'보다 다소 구어적임., Minor style flow discrepancy.
- `why-we-no-longer-evaluate-swe-bench-verified.block-012` | overall=84.3
  source: Regression tests that pass both before and after the fix to ensure unrelated functionality remains intact.
  candidate: 수정 전후 모두 통과하여 관련 없는 기능이 유지되는지 확인하는 회귀 테스트
  issues: '관련 없는 기능' 표현이 '버그 수정과 무관한 기존 기능'보다 미묘하게 의미가 덜 명확함, 좀 더 공식적이고 명확한 번역 가능

## Terminology Mismatch Examples

- `why-we-no-longer-evaluate-swe-bench-verified.block-034` | terminology_consistency_score=0.0
  source: Given a short snippet from the task description, GPT‑5.2 outputs the exact gold patch. In particular, it knows the exact class and method name, and the new early return condition `if username is None or password is None` that is introduced.
  candidate: 작업 설명의 짧은 스니펫만으로 GPT‑5.2는 정확한 정답 패치를 출력합니다. 특히, 정확한 클래스와 메서드 이름, 그리고 새로 도입된 조기 반환 조건인 `if username is None or password is None`을 알고 있습니다.
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., '정답 패치'보다 '골드 패치'가 번역 스타일과 전문성에 더 부합할 수 있음
- `why-we-no-longer-evaluate-swe-bench-verified.block-040` | terminology_consistency_score=0.0
  source: Gemini 3 Flash, when given no further information regarding the task besides the ID, is able to output verbatim details from the task description and the gold patch. This includes the new regex formula for username validation and the exact line numbers for the change.
  candidate: Gemini 3 Flash는 작업 ID 외에 추가 정보가 주어지지 않아도 작업 설명과 정답 패치의 내용을 문자 그대로 출력할 수 있습니다. 여기에는 사용자명 검증을 위한 새로운 정규식 공식과 변경된 정확한 라인 번호가 포함됩니다.
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., '정답 패치' term less appropriate than '골드 패치', '공식' less natural than '식' in regex context
- `why-we-no-longer-evaluate-swe-bench-verified.block-001` | terminology_consistency_score=50.0
  source: Since we first published SWE-bench Verified in August 2024, the industry has widely used it to measure the progress of models on autonomous software engineering tasks. After its release, SWE-bench Verified provided a strong signal of capability progress and became a standard metric reported in frontier model releases. Tracking and forecasting progress of these capabilities is also an important part of OpenAI’s Preparedness Framework. When we created the Verified benchmark initially, we attempted to solve issues in the original evaluation that made certain tasks impossible to accomplish in the SWE-bench dataset.
  candidate: 2024년 8월에 SWE-bench Verified를 처음 공개한 이후, 업계에서는 이를 자율 소프트웨어 엔지니어링 과제에서 모델의 진척도를 측정하는 데 널리 사용해왔습니다. 출시 후 SWE-bench Verified는 능력 향상의 강력한 지표를 제공했으며 최첨단 모델 출시 시 표준 지표로 자리잡았습니다. 이러한 능력의 진척 상황 추적과 예측은 OpenAI의 대비 프레임워크에서도 중요한 부분입니다. Verified 벤치마크를 처음 만들 때 우리는 SWE-bench 데이터셋 내에서 특정 과제를 수행할 수 없게 만들던 기존 평가 문제를 해결하려고 시도했습니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., Terminology mismatch: expected a consistent rendering for 'Preparedness Framework'., 'Preparedness Framework' is translated as '대비 프레임워크' instead of '준비성 평가 프레임워크', losing nuance., Use of '공개' vs '발표' for 'published' is a slightly less formal choice., Minor difference in translation of 'standard metric reported in frontier model releases' as '최첨단 모델 출시 시' instead of '프런티어 모델 출시 시'.
- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | terminology_consistency_score=50.0
  source: In a new analysis, we found two major issues with the Verified set that indicate the benchmark is no longer suitable for measuring progress on autonomous software engineering capabilities for frontier launches at today’s performance levels:
  candidate: 새로운 분석에서 우리는 Verified 세트에 두 가지 주요 문제가 있음을 발견했으며, 이는 현재 성능 수준의 최첨단 출시 모델들을 위한 자율 소프트웨어 엔지니어링 능력 측정에 이 벤치마크가 더 이상 적합하지 않다는 것을 시사합니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., '최첨단 출시 모델들' 표현이 '프런티어 모델 출시에 수반되는'보다 다소 구어적임., Minor style flow discrepancy.
- `why-we-no-longer-evaluate-swe-bench-verified.block-005` | terminology_consistency_score=50.0
  source: Training on solutions: Because large frontier models can learn information from their training, it is important that they are never trained on problems and solutions they are evaluated on. This is akin to sharing problems and solutions for an upcoming test with students before the test - they may not memorize the answer but students who have seen the answers before will certainly do better than those without. SWE-bench problems are sourced from open-source repositories many model providers use for training purposes. In our analysis we found that all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference, known as the gold patch, or verbatim problem statement specifics for certain tasks, indicating that all of them have seen at least some of the problems and solutions during training.
  candidate: 해결책의 훈련 포함: 대규모 최첨단 모델은 훈련에서 정보를 학습할 수 있으므로, 평가 대상인 문제와 해결책에 대해 절대 훈련하면 안 됩니다. 이는 다가오는 시험 문제와 답을 학생들에게 미리 공유하는 것과 유사합니다. 학생들이 답을 외우지 않더라도 이전에 답을 본 학생들이 그렇지 않은 학생보다 성적이 더 좋을 것입니다. SWE-bench 문제들은 많은 모델 제공자가 훈련 목적으로 사용하는 오픈소스 저장소에서 수집되었습니다. 분석 결과, 우리가 테스트한 모든 최첨단 모델들은 기준 진실 참조로 사용되는 원본 인간 작성 버그 수정(골드 패치)이나 특정 과제의 문제 문구를 말 그대로 재현할 수 있었으며, 이는 모든 모델이 훈련 중 최소 일부 문제와 해결책을 접했다는 것을 나타냅니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., '해결책의 훈련 포함' is somewhat unnatural; '해답 학습' or '해답 포함' preferred., Minor terminology nuance on 'gold patch' translation chosen as '골드 패치' rather than localized term.

## Backtranslation Mismatch Examples

- `why-we-no-longer-evaluate-swe-bench-verified.block-019` | backtranslation_similarity_score=74.9
  source: Too narrow and too wide tests
  candidate: 너무 좁거나 너무 넓은 테스트
  issues: 약간 덜 공식적인 '좁거나 넓은' 대신 '제한적이거나 광범위한'이 더 적합
- `why-we-no-longer-evaluate-swe-bench-verified.block-024` | backtranslation_similarity_score=76.7
  source: The remaining 5.1% of tasks had miscellaneous issues that were not well grouped with this taxonomy.
  candidate: 나머지 5.1% 작업은 이 분류법으로 명확히 묶기 어려운 기타 문제를 포함하고 있었습니다.
  issues: Minor variation in phrasing, Candidate is natural and clear, Slight terminology difference: '분류 기준' vs '분류법'
- `why-we-no-longer-evaluate-swe-bench-verified.block-017` | backtranslation_similarity_score=82.2
  source: Depending on setup of the environment (for example Linux vs Windows, or the python version), some tests could spuriously fail
  candidate: 환경 설정(예: Linux 대 Windows, 파이썬 버전)에 따라 일부 테스트가 일시적으로 실패할 수 있습니다.
  issues: '일시적으로 실패' 표현이 원문의 'spuriously fail' 의미를 완전하지 않음, '환경 설정'에서 '설정' 보다는 '환경' 혹은 '구성'이 자연스러움, 문장 마무리가 영어 현재형을 직역해 다소 딱딱함
- `why-we-no-longer-evaluate-swe-bench-verified.block-041` | backtranslation_similarity_score=84.0
  source: Task ID: django__django-11099
  candidate: 작업 ID: django__django-11099
  issues: none
- `why-we-no-longer-evaluate-swe-bench-verified.block-006` | backtranslation_similarity_score=86.3
  source: We also found evidence that models that have seen the problems during training are more likely to succeed, because they have additional information needed to pass the underspecified tests.
  candidate: 또한, 훈련 중 문제를 접한 모델일수록 미확정 테스트를 통과하는 데 필요한 추가 정보를 가지고 있어 성공률이 더 높다는 증거도 발견했습니다.
  issues: '미확정 테스트'는 '명세가 불충분한 테스트'보다 의미 전달이 다소 약함, '훈련 중 문제를 접한 모델' 어투가 다소 직역 느낌, '성공률이 더 높다'는 원문의 '더 likely to succeed' 뉘앙스를 완벽히 담지 못함

## Human Review Queue

- `why-we-no-longer-evaluate-swe-bench-verified.block-001` | overall=88.2 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | overall=83.6 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-005` | overall=80.9 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-031` | overall=88.8 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-034` | overall=80.7 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-040` | overall=80.5 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-045` | overall=91.2 | reasons: terminology_consistency_score < 100
