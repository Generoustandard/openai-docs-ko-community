# Translation Evaluation Report

## Pair

- pair_slug: `why-we-no-longer-evaluate-swe-bench-verified`
- unit_count: 79
- score_scale: `0-100`
- overall_formula: `0.30 * semantic_similarity_score + 0.25 * backtranslation_similarity_score + 0.15 * terminology_consistency_score + 0.30 * llm_judge_score`

## Document Summary

- average_overall_score: 90.6
- average_semantic_similarity_score: 86.1
- average_backtranslation_similarity_score: 90.6
- average_terminology_consistency_score: 93.2
- average_llm_judge_score: 94.0
- human_review_count: 15

## Top 5 Problem Items

- `why-we-no-longer-evaluate-swe-bench-verified.block-054` | overall=51.3
  source: Gold patch
  candidate: 정답 패치
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., Terminology issue: '골드 패치' is a loan translation closely related to the English term 'Gold patch' often used in ML contexts, Candidate '정답 패치' implies 'correct answer patch', which may lose nuance of 'gold standard' or 'reference' patch, Naturalness could be improved by matching common usage in Korean technical literature
- `why-we-no-longer-evaluate-swe-bench-verified.block-029` | overall=71.8
  source: Python
  candidate: 파이썬
  issues: 용어 일관성: 'Python'을 카탈로그 및 전문 문서에서는 원어 표기하는 경우가 많음, 자연스러움: '파이썬'도 충분히 자연스러우나 대문자 표기어와 일치하지 않을 수 있음
- `why-we-no-longer-evaluate-swe-bench-verified.block-031` | overall=71.8
  source: Python
  candidate: 파이썬
  issues: Terminology consistency: 'Python' is a proper noun that is generally not translated in technical contexts., Naturalness: '파이썬' is commonly used but slightly less formal in official documents.
- `why-we-no-longer-evaluate-swe-bench-verified.block-074` | overall=71.8
  source: Python
  candidate: 파이썬
  issues: Candidate uses Korean phonetic '파이썬' whereas reference keeps English 'Python'; inconsistency in terminology
- `why-we-no-longer-evaluate-swe-bench-verified.block-055` | overall=73.3
  source: Python
  candidate: 파이썬
  issues: Terminology consistency: 'Python' is often transliterated as '파이썬' in Korean but some technical texts keep 'Python' in English, Stylistic consistency with the rest of the document could be checked

## Terminology Mismatch Examples

- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | terminology_consistency_score=0.0
  source: In a new analysis, we found two major issues with the Verified set that indicate the benchmark is no longer suitable for measuring progress on autonomous software engineering capabilities for frontier launches at today’s performance levels:
  candidate: 새 분석에서 Verified 세트에 두 가지 주요 문제가 발견되었는데, 이는 오늘날 성능 수준에서 첨단 출시를 위한 자율 소프트웨어 엔지니어링 능력 진전을 측정하는 데 더 이상 적합하지 않음을 나타냅니다:
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., Terminology mismatch: expected a consistent rendering for 'benchmark'.
- `why-we-no-longer-evaluate-swe-bench-verified.block-048` | terminology_consistency_score=0.0
  source: Given a short snippet from the task description, GPT‑5.2 outputs the exact gold patch. In particular, it knows the exact class and method name, and the new early return condition `if username is None or password is None` that is introduced.
  candidate: 작업 설명의 짧은 예시만 주어져도 GPT‑5.2는 정확한 정답 패치를 출력합니다. 특히, 정확한 클래스와 메서드 이름, 그리고 새로 도입된 조기 반환 조건인 `if username is None or password is None`을 알고 있습니다.
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., '짧은 예시' in candidate less formal than '짧은 스니펫' in reference, but understandable., Candidate uses '정답 패치' instead of more formal '골드 패치' from reference., Minor style difference: candidate slightly more casual.
- `why-we-no-longer-evaluate-swe-bench-verified.block-054` | terminology_consistency_score=0.0
  source: Gold patch
  candidate: 정답 패치
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., Terminology issue: '골드 패치' is a loan translation closely related to the English term 'Gold patch' often used in ML contexts, Candidate '정답 패치' implies 'correct answer patch', which may lose nuance of 'gold standard' or 'reference' patch, Naturalness could be improved by matching common usage in Korean technical literature
- `why-we-no-longer-evaluate-swe-bench-verified.block-066` | terminology_consistency_score=0.0
  source: Gemini 3 Flash, when given no further information regarding the task besides the ID, is able to output verbatim details from the task description and the gold patch. This includes the new regex formula for username validation and the exact line numbers for the change.
  candidate: Gemini 3 플래시는 작업 ID 외에 추가 정보가 제공되지 않아도 작업 설명과 정답 패치에 있는 세부사항을 그대로 출력할 수 있습니다. 여기에는 사용자명 검증을 위한 새로운 정규식 공식과 변경 사항이 적용된 정확한 줄 번호가 포함됩니다.
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., '정식' vs '공식' 혼용: '정규식 공식' 대신 '정규식'이나 '정규식 패턴'이 더 자연, '검증' 대신 '유효성 검사' 용어 일관성 필요, '플래시' 한글 표기 통일성 고려 가능
- `why-we-no-longer-evaluate-swe-bench-verified.block-001` | terminology_consistency_score=50.0
  source: Since we first published SWE-bench Verified in August 2024, the industry has widely used it to measure the progress of models on autonomous software engineering tasks. After its release, SWE-bench Verified provided a strong signal of capability progress and became a standard metric reported in frontier model releases. Tracking and forecasting progress of these capabilities is also an important part of OpenAI’s Preparedness Framework. When we created the Verified benchmark initially, we attempted to solve issues in the original evaluation that made certain tasks impossible to accomplish in the SWE-bench dataset.
  candidate: 2024년 8월 SWE-bench Verified를 처음 공개한 이후, 업계에서는 이를 자율 소프트웨어 엔지니어링 작업에서 모델의 진전을 측정하는 데 널리 사용해왔습니다. 출시 후 SWE-bench Verified는 능력 향상의 강력한 신호를 제공하며 첨단 모델 출시에서 표준 지표가 되었습니다. 이러한 능력의 추적 및 예측은 OpenAI 준비 프레임워크의 중요한 부분이기도 합니다. Verified 벤치마크를 처음 만들었을 때, SWE-bench 데이터셋 내 일부 과제가 불가능했던 원래 평가의 문제를 해결하려 시도했습니다.
  issues: Terminology mismatch: expected a consistent rendering for 'frontier'., Terminology mismatch: expected a consistent rendering for 'Preparedness Framework'., 'Preparedness Framework' 번역에서 '준비성 평가 프레임워크'보다 '준비성 프레임워크'가 자연스러움, 'SWE-bench 데이터셋 내 일부 과제' 표현이 원문 'certain tasks' 의미에 비해 다소 제한적임, '능력' 대신 '역량' 용어 일관성 부족

## Backtranslation Mismatch Examples

- `why-we-no-longer-evaluate-swe-bench-verified.block-054` | backtranslation_similarity_score=43.0
  source: Gold patch
  candidate: 정답 패치
  issues: Terminology mismatch: expected a consistent rendering for 'gold patch'., Terminology issue: '골드 패치' is a loan translation closely related to the English term 'Gold patch' often used in ML contexts, Candidate '정답 패치' implies 'correct answer patch', which may lose nuance of 'gold standard' or 'reference' patch, Naturalness could be improved by matching common usage in Korean technical literature
- `why-we-no-longer-evaluate-swe-bench-verified.block-061` | backtranslation_similarity_score=53.7
  source: Prefill
  candidate: 사전 입력
  issues: Backtranslation 'Pre-input' is less natural than 'Prefill' but acceptable.
- `why-we-no-longer-evaluate-swe-bench-verified.block-071` | backtranslation_similarity_score=53.7
  source: Prefill
  candidate: 사전 입력
  issues: backtranslation 'Pre-input' is slightly less natural than 'Prefill'
- `why-we-no-longer-evaluate-swe-bench-verified.block-050` | backtranslation_similarity_score=70.7
  source: Contamination elicitation
  candidate: 오염 유발
  issues: Candidate '오염 유발' is less established term than '오염 발현 유도' in reference., 'Elicitation' implies inducing or eliciting (발현 유도), candidate's '유발' is close but less accurate., Term consistency with domain-specific usage may favor reference.
- `why-we-no-longer-evaluate-swe-bench-verified.block-059` | backtranslation_similarity_score=71.3
  source: Contamination elicitation
  candidate: 오염 유도
  issues: accuracy loss by omitting '발현' (elicitation) nuance, terminology inconsistency

## Human Review Queue

- `why-we-no-longer-evaluate-swe-bench-verified.block-001` | overall=87.4 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-003` | overall=73.8 | reasons: overall_score < 80, terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-005` | overall=81.2 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-028` | overall=78.4 | reasons: overall_score < 80
- `why-we-no-longer-evaluate-swe-bench-verified.block-029` | overall=71.8 | reasons: overall_score < 80
- `why-we-no-longer-evaluate-swe-bench-verified.block-031` | overall=71.8 | reasons: overall_score < 80
- `why-we-no-longer-evaluate-swe-bench-verified.block-045` | overall=89.1 | reasons: terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-048` | overall=78.2 | reasons: overall_score < 80, terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-051` | overall=75.4 | reasons: overall_score < 80
- `why-we-no-longer-evaluate-swe-bench-verified.block-054` | overall=51.3 | reasons: overall_score < 80, terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-055` | overall=73.3 | reasons: overall_score < 80
- `why-we-no-longer-evaluate-swe-bench-verified.block-059` | overall=79.1 | reasons: overall_score < 80, llm_judge_score < 75
- `why-we-no-longer-evaluate-swe-bench-verified.block-066` | overall=75.5 | reasons: overall_score < 80, terminology_consistency_score < 100
- `why-we-no-longer-evaluate-swe-bench-verified.block-069` | overall=74.9 | reasons: overall_score < 80
- `why-we-no-longer-evaluate-swe-bench-verified.block-074` | overall=71.8 | reasons: overall_score < 80
