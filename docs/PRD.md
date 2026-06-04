# PRD — MagicSquare_1004 (4×4 부분 마방진 · 검증·판정)

**버전:** 1.0  
**작성 기준일:** 2026-06-04  
**상위 문서:** [`Report/01.MagicSquare_ProblemDefinition_Report.md`](../Report/01.MagicSquare_ProblemDefinition_Report.md)

---

## 1. 개요

### 1.1 배경 (Mom Test)

**페르소나:** 4×4 부분 마방진(빈칸 2개)을 손/코드로 다루는 학습자.

**진짜 문제:** ‘맞다’고 볼 **검산 기준·순서가 흔들려** 행합만 맞다고 보고 숫자를 반복 바꿔 넣다가, 열·대각 불일치를 뒤늦게 알아 **~20분** 같은 비용을 쓴다.

**Mom Test 증거:**

1. 대각선 하나 빼먹어 **20분** 날림  
2. 바꿔 넣을 때 **행 합만 34**  
3. 빈칸 불일치 → **열합 ≠ 34** → **직접 대각선 합**

### 1.2 주제 (한 문장)

4×4 부분 마방진에서 **‘맞다’는 판정**을, **10개 라인**(4행·4열·2대각) 검산을 빠짐없이 거친 뒤에만 내릴 수 있게 한다.

### 1.3 1차 범위 (In-Scope)

- 입력 계약 검증 (`ValidateInput`)
- 10라인 합 검산 및 실패 라인 식별 (`CheckTenLines`)
- 완성 판정 (`AssertComplete`) — **행합만 통과 금지**

### 1.4 1차 비범위 (Out-of-Scope)

- 빈칸 2개 **자동 Solver**, `int[6]` 좌표·숫자 출력
- PyQt/GUI 워크벤치, Cursor 플러그인 등 **솔루션 UI**
- ECB/TDD **교육 툴** 제품화
- DB·파일 영속화

---

## 2. R-G-I-O

| | 정의 |
|---|------|
| **Role** | 학습자 또는 검증 API 호출자 |
| **Goal** | 10라인 합 34 기준으로 **재현 가능한** 완성/미완성 판정 |
| **Input** | `matrix: int[4][4]` — 규칙见 §3 |
| **Output** | §4 출력 계약 |

---

## 3. 입력 계약

| ID | 규칙 | 위반 시 오류 |
|----|------|--------------|
| I1 | 정확히 4×4 | `E_INPUT_SIZE` |
| I2 | `0`은 정확히 2개 | `E_EMPTY_COUNT` |
| I3 | 각 값 ∈ {0} ∪ [1,16] | `E_VALUE_RANGE` |
| I4 | 0 제외 값 중복 없음 | `E_DUPLICATE` |

**도메인 상수:** `MAGIC_SUM = 34`, `LINE_COUNT = 10`

---

## 4. 출력 계약

### 4.1 `CheckTenLines(matrix)` → `LineCheckResult`

| 필드 | 타입 | 설명 |
|------|------|------|
| `lines` | 10 entries | 각 라인: `id`, `type`(row\|col\|diag), `index`, `sum`, `ok` |
| `all_ok` | bool | 10라인 모두 `ok` |
| `first_failing` | optional | SC-2: 첫 실패 라인 (고정 순서: row→col→diag) |

### 4.2 `AssertComplete(matrix)` → `bool`

- `true` **iff** 10라인 모두 합 34  
- **행합만 34**이고 열/대각 실패 시 **반드시 `false`** (SC-1)

### 4.3 `ValidateInput(matrix)`

- I1~I4 위반 시 해당 `E_*` 예외(또는 Result Err) — **검산 로직 미진입**

---

## 5. 기능 요구 (FR)

| ID | 요구 | Mom Test / SC |
|----|------|----------------|
| FR-01 | I1~I4 검증, 고정 오류 4종 | TL-04 |
| FR-02 | 10라인 각각 합 계산, `MAGIC_SUM`과 비교 | 도메인 10선·34 |
| FR-03 | 실패 시 **라인 종류·인덱스** 반환 | SC-2 ↔ ①③ |
| FR-04 | `AssertComplete`는 FR-02 `all_ok`와 동치 | SC-1 ↔ ② |
| FR-05 | 동일 입력 2회 호출 시 결과 동일 | SC-3 |

---

## 6. 성공 기준 (Acceptance)

| ID | Given | When | Then |
|----|-------|------|------|
| AC-01 | 행합만 34, 열 또는 대각 실패 보드 | `AssertComplete` | `false` (SC-1) |
| AC-02 | 행·열 OK, 주대각(또는 부대각) 실패 | `CheckTenLines` | `first_failing.type == diag` (SC-2) |
| AC-03 | 유효 4×4 보드 | `CheckTenLines` ×2 | 동일 `lines`, `all_ok` (SC-3) |
| AC-04 | 빈칸 3개 / 5×5 / 값 17 | `ValidateInput` | `E_*`, 검산 미호출 |

---

## 7. 10라인 정의

| type | index | 설명 |
|------|-------|------|
| row | 1..4 | 행 합 |
| col | 1..4 | 열 합 |
| diag | 1 | 주대각 (1,1)-(4,4) |
| diag | 2 | 부대각 (1,4)-(4,1) |

---

## 8. Test Loop (RED → GREEN)

| TL ID | 테스트 요지 | 상태 |
|-------|-------------|------|
| TL-01 | 행합만 34 보드 → complete false | RED |
| TL-02 | 대각 실패 → diag 라인 ID | RED |
| TL-03 | 동일 보드 2회 동일 결과 | RED |
| TL-04 | 입력 계약 4종 오류 | RED |

**루프:** Rule 확정 → Command 시그니처 → pytest RED → (다음 세션) GREEN

---

## 9. Rule · Command · Skill 매핑

| Rule | Command | Skill |
|------|---------|-------|
| R-IN-01~03 | CMD-01 `ValidateInput` | — |
| R-VAL-01~03 | CMD-02 `CheckTenLines` | SK-01, SK-02 |
| R-VAL-02 | CMD-03 `AssertComplete` | SK-01 |

---

## 10. 후속 PRD (2차, 미작성)

- 빈칸 2개 위치 탐색, 누락 수 2개, `int[6]` 출력 `[r1,c1,n1,r2,c2,n2]` (1-index)
- Solver 및 Dual-Track Boundary — **Mom Test 1차 범위 외**

---

## 11. 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-06-04 | Mom Test·세션 3 초안 반영, 검증·판정 1차 범위 |
