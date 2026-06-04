# MagicSquare_1004

4×4 **부분 마방진**(빈칸 `0` 2개, 1~16, **10라인 합 34**)에서 **‘맞다’는 판정**이 행합만으로 흔들리지 않도록 **검증·판정 계약**을 고정하고, ECB + Dual-Track TDD로 단계적으로 구현하는 프로젝트입니다.

**단일 진실 공급원:** [`docs/PRD.md`](docs/PRD.md)  
**문제 정의·Mom Test:** [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md)  
**보고서·세션 이력:** [`Report/README.md`](Report/README.md)

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
| 마방 상수 | **34** (`MAGIC_SUM`) |
| 검산 | **10라인** (4행 + 4열 + 2대각) |
| Solver 출력 (구현 계약) | **`int[6]`** → `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index** |

도메인 숫자 리터럴은 [`src/entity/constants.py`](src/entity/constants.py) **SSOT**만 사용 (`.cursorrules` MagicConstant).

---

## 현재 구현 상태

| Layer | 상태 | Test ID |
|-------|------|---------|
| **entity** | `find_blank_coords` (D-LOC-01), `solve_step_a` 행합 채움 (D-SOL-01 step A) | `D-LOC-01`, `D-SOL-01` |
| **control** | 미구현 | — |
| **boundary** | 미구현 | — |

**pytest (Logic track):** entity 2건 — 로컬에서 `python -m pytest tests/ -v` 로 확인.

**다음 (REFACTOR 트랙):** `/golden-master` → `/refactor-safe` (안전 원칙·Change Budget은 [`.cursorrules`](.cursorrules) 및 Report 05·스멜 분석 참고).

---

## 1차 범위 / 비범위 (PRD)

**포함 (목표):** 입력 검증, 10라인 합 검사, 실패 라인 식별, 완성 판정(`AssertComplete`)

**제외 (PRD 1.4):** GUI 워크벤치, ECB/TDD 툴 제품화, DB·영속화

**코드 진행 (교안·2차):** entity 레이어에서 빈칸 좌표·Step A 행합 채움까지 GREEN — 상세는 [`Report/04`](Report/04.MagicSquare_GREEN_D_LOC_01_Report.md), [`Report/05`](Report/05.MagicSquare_GREEN_D_SOL_01_Report.md).

---

## 폴더 구조

```
MagicSquare_1004/
├── README.md
├── pyproject.toml
├── .cursorrules
├── docs/
│   └── PRD.md
├── src/
│   └── entity/
│       ├── constants.py   # MAGIC_SUM, GRID_SIZE, …
│       ├── loc.py         # find_blank_coords
│       └── sol.py         # solve_step_a
├── tests/
│   ├── conftest.py        # grid_g1 (G1_LOC)
│   └── entity/
│       ├── test_d_loc_01.py
│       └── test_d_sol_01.py
├── Report/                # 세션·TDD 보고서 (인덱스: Report/README.md)
├── Prompting/             # Agent export transcript
└── Prompt/                # Mom Test·세션 프롬프트
```

---

## Mom Test → 구현 흐름

1. **STEP 1** — Mom Test 인터뷰 ([`Prompt/01...`](Prompt/01.magic-square-mom-test-step1-interview-prompt.md))
2. **세션 3** — 주제·R-G-I-O·Rule/Command/Test Loop ([`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md))
3. **PRD** — FR·AC·입출력 계약 ([`docs/PRD.md`](docs/PRD.md))
4. **Harness** — ECB·Dual-Track·`.cursorrules` ([`Report/02`](Report/02.MagicSquare_Harness_CursorRules_Report.md))
5. **TDD** — RED → GREEN (D-LOC-01, D-SOL-01) → REFACTOR (`/golden-master`, `/refactor-safe`)

### 인터뷰 프롬프트 요약

| 단계 | 내용 |
|------|------|
| ① 시작 | `MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자. 질문 1개만. 솔루션 금지.` |
| ② 답변 후 | `[답변] → 사실성 평가 + 추궁 1개 + 불편 요약` |
| ③ 종료 | `표면 vs 진짜 문제 + 증거 3줄` |
| ④ 세션 3 | `진짜 문제 → R-G-I-O + 주제 + 성공 기준` |

---

## 개발 환경

```bash
# 의존성 (선택)
pip install -e ".[dev]"

# 전체 테스트
python -m pytest tests/ -v
```

`pyproject.toml`의 `pythonpath = ["src"]`와 `tests/conftest.py`의 entity 선로드는 `tests/entity/` 패키지 shadow를 피하기 위한 설정입니다.

---

## 아키텍처 (ECB)

- 의존 방향: **boundary → control → entity**
- **entity:** 도메인 규칙만; `boundary`/`control`/UI import 금지; Boundary 오류 **E001~E005** 처리 금지
- **Dual-Track:** Logic (`test_d_*.py`, Domain Mock 금지) · UI (`test_u_*.py`, boundary, Mock 허용)

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [Problem Definition Report](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test 워크북, 세션 3, 8계층 |
| [PRD](docs/PRD.md) | FR, AC, 입출력·오류 계약 |
| [Harness Report](Report/02.MagicSquare_Harness_CursorRules_Report.md) | ECB Harness · `.cursorrules` |
| [GREEN D-LOC-01](Report/04.MagicSquare_GREEN_D_LOC_01_Report.md) | `find_blank_coords` |
| [GREEN D-SOL-01](Report/05.MagicSquare_GREEN_D_SOL_01_Report.md) | `solve_step_a` · Golden Master 선행 |
| [REFACTOR Smell](Report/06.MagicSquare_REFACTOR_Smell_Report.md) | `/refactor-smell` · `/refactor-safe` 후보 |
| [Report 인덱스](Report/README.md) | 보고서·transcript 목록·읽는 순서 |
| [Prompt 02 세션3](Prompt/02.magic-square-session3-workbook-prompt.md) | 워크북·PRD 생성 |
| [Prompt 03 질문뱅크](Prompt/03.magic-square-mom-test-question-bank-prompt.md) | Mom Test 질문 10개 |

---

**작성 기준일:** 2026-06-04 · **갱신:** entity GREEN (D-LOC-01, D-SOL-01)
