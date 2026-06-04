# Report — MagicSquare_1004

## 문서 목록

| 파일 | STEP | 설명 |
|------|------|------|
| [`01.magic-square-mom-test-step1-report.md`](01.magic-square-mom-test-step1-report.md) | 1 | Mom Test **인터뷰 원본** Q&A·증거·채점 |
| [`01.MagicSquare_ProblemDefinition_Report.md`](01.MagicSquare_ProblemDefinition_Report.md) | 1+3 | Mom Test + **세션 3** 통합·Rule/Command/Test Loop |
| [`02.MagicSquare_Harness_CursorRules_Report.md`](02.MagicSquare_Harness_CursorRules_Report.md) | 2 | ECB Harness · `.cursorrules` · `spec` push |
| [`export-transcript-2026-06-04-harness-session.md`](export-transcript-2026-06-04-harness-session.md) | 2 | Agent 대화 **export transcript** (Harness 세션) |
| [`03.MagicSquare_RED_D_LOC_01_Skeleton_Report.md`](03.MagicSquare_RED_D_LOC_01_Skeleton_Report.md) | RED | D-LOC-01 스켈레톤 · pytest RED |
| [`../Prompting/export-transcript-2026-06-04-red-d-loc-01-skeleton.md`](../Prompting/export-transcript-2026-06-04-red-d-loc-01-skeleton.md) | RED | Agent **export transcript** (D-LOC-01) |
| [`04.MagicSquare_GREEN_D_LOC_01_Report.md`](04.MagicSquare_GREEN_D_LOC_01_Report.md) | GREEN | D-LOC-01 `find_blank_coords` · pytest PASS · G1 좌표 정정 |
| [`../Prompting/export-transcript-2026-06-04-green-d-loc-01.md`](../Prompting/export-transcript-2026-06-04-green-d-loc-01.md) | GREEN | Agent **export transcript** (D-LOC-01) |
| [`05.MagicSquare_GREEN_D_SOL_01_Report.md`](05.MagicSquare_GREEN_D_SOL_01_Report.md) | GREEN | D-SOL-01 `solve_step_a` · int[6] · pytest PASS |
| [`../Prompting/export-transcript-2026-06-04-green-d-sol-01.md`](../Prompting/export-transcript-2026-06-04-green-d-sol-01.md) | GREEN | Agent **export transcript** (D-SOL-01) |

## 읽는 순서

1. STEP 1 원본 → `01.magic-square-mom-test-step1-report.md`
2. 문제 정의 통합 → `01.MagicSquare_ProblemDefinition_Report.md`
3. 구현 계약 → [`docs/PRD.md`](../docs/PRD.md)
4. Harness·규칙 → `02.MagicSquare_Harness_CursorRules_Report.md` (+ transcript)
5. RED D-LOC-01 → `03.MagicSquare_RED_D_LOC_01_Skeleton_Report.md` (+ [`Prompting/`](../Prompting/) transcript)
6. GREEN D-LOC-01 → `04.MagicSquare_GREEN_D_LOC_01_Report.md` (+ green transcript)
7. GREEN D-SOL-01 → `05.MagicSquare_GREEN_D_SOL_01_Report.md` (+ green transcript) → `/golden-master`

## Prompt 연동

| Prompt | 용도 |
|--------|------|
| [`Prompt/01...`](../Prompt/01.magic-square-mom-test-step1-interview-prompt.md) | Mom Test ①~④·채점 |
| [`Prompt/02...`](../Prompt/02.magic-square-session3-workbook-prompt.md) | 세션 3·문서 생성 |
| [`Prompt/03...`](../Prompt/03.magic-square-mom-test-question-bank-prompt.md) | 질문 뱅크 10개 |

**갱신:** 2026-06-04
