# MagicSquare_1004

4×4 **부분 마방진**(빈칸 `0` 2개, 1~16, **10라인 합 34**)을 다룰 때, **‘맞다’는 판정**이 행합만으로 흔들리지 않도록 **검증·판정 계약**을 고정하는 프로젝트입니다.

**단일 진실 공급원:** [`docs/PRD.md`](docs/PRD.md)  
**문제 정의·Mom Test:** [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md)

---

## 왜 이 프로젝트인가 (Mom Test 한 줄)

학습자가 빈칸을 맞출 때 검산 기준·순서가 흔들려 **행합만 34**로 맞다고 보다 **20분** 같은 시행착오가 난다 — 우선 **10라인 검산 후에만** 완성 판정한다.

---

## 도메인 (고정)

| 항목 | 값 |
|------|-----|
| 격자 | 4×4 |
| 빈칸 | `0`, 정확히 **2개** |
| 값 | `0` 또는 **1~16**, 0 제외 중복 없음 |
| 마방 상수 | **34** |
| 검산 | **10라인** (4행 + 4열 + 2대각) |

---

## 1차 범위 / 비범위

**포함:** 입력 검증, 10라인 합 검사, 실패 라인 식별, 완성 판정(`AssertComplete`)

**제외:** 자동 Solver, `int[6]` 출력, GUI 워크벤치, ECB/TDD 툴 제품화

---

## 폴더 구조

```
MagicSquare_1004/
├── README.md
├── docs/
│   └── PRD.md
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md   # Mom Test + 세션 3
│   └── 01.magic-square-mom-test-step1-report.md     # 인터뷰 원본
├── Report/README.md
└── Prompt/
    ├── 01.magic-square-mom-test-step1-interview-prompt.md
    ├── 02.magic-square-session3-workbook-prompt.md
    └── 03.magic-square-mom-test-question-bank-prompt.md
```

---

## Mom Test → 구현 흐름

1. **STEP 1** — Mom Test 인터뷰 ([`Prompt/01...`](Prompt/01.magic-square-mom-test-step1-interview-prompt.md))
2. **세션 3** — 주제·R-G-I-O·Rule/Command/Test Loop ([`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md))
3. **PRD** — FR·AC·입출력 계약 ([`docs/PRD.md`](docs/PRD.md))
4. **(다음)** — pytest RED (`TL-01`~`04`) → GREEN

### 인터뷰 프롬프트 요약

| 단계 | 내용 |
|------|------|
| ① 시작 | `MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자. 질문 1개만. 솔루션 금지.` |
| ② 답변 후 | `[답변] → 사실성 평가 + 추궁 1개 + 불편 요약` |
| ③ 종료 | `표면 vs 진짜 문제 + 증거 3줄` |
| ④ 세션 3 | `진짜 문제 → R-G-I-O + 주제 + 성공 기준` |

---

## 테스트 (예정)

```bash
# 구현·tests/ 추가 후
python -m pytest tests/ -v
```

현재 저장소는 **문서·계약 단계**이며, `TL-01`~`04` RED 테스트는 후속 커밋에서 추가한다.

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [Problem Definition Report](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test 워크북, 세션 3, 8계층(Rule/Command/Skill/Test Loop) |
| [PRD](docs/PRD.md) | FR, AC, 입출력·오류 계약 |
| [Mom Test STEP1 Report](Report/01.magic-square-mom-test-step1-report.md) | 인터뷰 Q&A 원본 |
| [Report 인덱스](Report/README.md) | 보고서 목록·읽는 순서 |
| [Prompt 02 세션3](Prompt/02.magic-square-session3-workbook-prompt.md) | 워크북·PRD 생성 |
| [Prompt 03 질문뱅크](Prompt/03.magic-square-mom-test-question-bank-prompt.md) | Mom Test 질문 10개 |

---

**작성 기준일:** 2026-06-04
