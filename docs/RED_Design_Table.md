# MagicSquare_1004 RED 설계표 (체크리스트)

**SSOT:** [PRD.md](PRD.md) · **Phase:** RED only · **범위:** `ValidateInput`, `CheckTenLines`, `AssertComplete`

---

## 진행 요약

- [ ] Fixture 검증 완료 (G0 / G1 / G2)
- [ ] Track A — UI/Boundary RED
- [ ] Track B — Domain/Logic RED
- [ ] E001~E004 ↔ PRD `E_*` 매핑 (U-OUT)

---

## 격자 Fixture (Given)

- [ ] **G_null** — `None` → U-IN-01
- [ ] **G_bad_shape** — 5×5 `[[1]*5]*5` → U-IN-02
- [ ] **G_bad_rect** — 3×4 `[[1,2,3],[4,5,6],[7,8,9]]` → U-IN-03
- [ ] **G0** — 10라인 모두 합 34  
  `[[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]` → D-ASM-02, D-CTL-01, D-CHK-05
- [ ] **G1** — 행합만 34 (열·대각 일부 실패, SC-1)  
  `[[16,3,2,13],[5,10,11,8],[9,6,7,12],[3,15,14,2]]`  
  검증: rows `[34,34,34,34]`, cols `[33,34,34,35]`, main_diag `35`, anti_diag `33`  
  → D-ASM-01, D-CHK-02~04
- [ ] **G2** — 행·열 OK, 대각 실패 (SC-2) — 합산 검증 후 matrix 고정 → D-CHK-01, D-ASM-03
- [ ] **G3** — 빈칸 3개 (I2), G0 기반 `0`×3 → U-IN-06, U-FLOW-01~02
- [ ] **G4** — 값 17 (I3), G0 + `(0,0)=17` → U-IN-08, U-OUT-03
- [ ] **G5** — 중복 (I4), G0 + 동일 값 중복 → U-IN-10, U-OUT-04
- [ ] **G6** — 빈칸 1개 `0`×1 → U-IN-07
- [ ] **G7** — 빈칸 0개 → U-IN-05

---

## Track A — UI/Boundary RED

**Layer:** `boundary` · **파일:** `tests/boundary/test_u_*.py` · **Command:** `ValidateInput` · **TL:** TL-04

### U-IN (입력 계약)

- [ ] **U-IN-01** — Given: `matrix=None` · Then: `E_INPUT_SIZE` (또는 `E001`) · RED: `ImportError` / `TypeError`
- [ ] **U-IN-02** — Given: `G_bad_shape` (5×5) · Then: `E_INPUT_SIZE` (I1) · RED: `AssertionError`
- [ ] **U-IN-03** — Given: `G_bad_rect` (3×4) · Then: `E_INPUT_SIZE` (I1) · RED: `AssertionError`
- [ ] **U-IN-04** — Given: `matrix=[]` · Then: `E_INPUT_SIZE` (I1) · RED: `AssertionError`
- [ ] **U-IN-05** — Given: `G7` (빈칸 0개) · Then: `E_EMPTY_COUNT` (I2) · RED: `AssertionError`
- [ ] **U-IN-06** — Given: `G3` (빈칸 3개) · Then: `E_EMPTY_COUNT` (I2) · AC-04 · RED: `AssertionError`
- [ ] **U-IN-07** — Given: `G6` (빈칸 1개) · Then: `E_EMPTY_COUNT` (I2) · RED: `AssertionError`
- [ ] **U-IN-08** — Given: `G4` (값 17) · Then: `E_VALUE_RANGE` (I3) · AC-04 · RED: `AssertionError`
- [ ] **U-IN-09** — Given: G0 + `(-1)` · Then: `E_VALUE_RANGE` (I3) · RED: `AssertionError`
- [ ] **U-IN-10** — Given: `G5` (중복) · Then: `E_DUPLICATE` (I4) · RED: `AssertionError`

### U-OUT (boundary 오류 노출)

- [ ] **U-OUT-01** — Given: `G_bad_shape` · Then: `E001` ↔ `E_INPUT_SIZE` · RED: `AssertionError` / `KeyError`
- [ ] **U-OUT-02** — Given: `G3` · Then: `E002` ↔ `E_EMPTY_COUNT` · RED: `AssertionError`
- [ ] **U-OUT-03** — Given: `G4` · Then: `E003` ↔ `E_VALUE_RANGE` · RED: `AssertionError`
- [ ] **U-OUT-04** — Given: `G5` · Then: `E004` ↔ `E_DUPLICATE` · RED: `AssertionError`

### U-FLOW (검산 미호출 · 오케스트레이션)

- [ ] **U-FLOW-01** — Given: `G3` + `CheckTenLines` spy · Then: `ValidateInput` 실패 후 CheckTenLines **0회** (AC-04) · RED: `pytest.fail("RED: CheckTenLines called")`
- [ ] **U-FLOW-02** — Given: `G3` + `AssertComplete` spy · Then: `ValidateInput` 실패 후 AssertComplete **0회** · RED: `pytest.fail("RED: AssertComplete called")`
- [ ] **U-FLOW-03** — Given: `G0` 유효 입력 · Then: `ValidateInput` 통과 → `CheckTenLines` 1회 · RED: `AssertionError`
- [ ] **U-FLOW-04** — Given: `G_null` · Then: 진입점 0회 또는 즉시 `E_INPUT_SIZE` · RED: `ImportError` / `pytest.fail() RED`

### Track A 권장 RED 순서

- [ ] U-IN-06 → U-IN-08 → U-FLOW-01 → U-FLOW-02 → U-OUT-01~04

---

## Track B — Domain/Logic RED

**파일:** `tests/entity/test_d_*.py`, `tests/control/test_d_*.py`

### D-ASM (`AssertComplete`)

- [ ] **D-ASM-01** — `AssertComplete(G1)` → `False` · Invariant: SC-1, FR-04, I1~I4 · TL-01
- [ ] **D-ASM-02** — `AssertComplete(G0)` → `True` · Invariant: R-VAL-02, MAGIC_SUM=34
- [ ] **D-ASM-03** — `AssertComplete(G2)` → `False` · Invariant: SC-1 (대각 미충족)

### D-CHK (`CheckTenLines`)

- [ ] **D-CHK-01** — `CheckTenLines(G2)` → `first_failing.type == "diag"` · Invariant: SC-2, FR-03, SK-02 · TL-02
- [ ] **D-CHK-02** — `CheckTenLines(G1)` → `all_ok == False` · Invariant: FR-02, R-VAL-01
- [ ] **D-CHK-03** — `CheckTenLines(G1)` → `len(result.lines) == 10` · Invariant: LINE_COUNT=10 · (D-04)
- [ ] **D-CHK-04** — `CheckTenLines(G1)` → 첫 실패 순서 row → col → diag · Invariant: SK-02, PRD §4.1 · TL-02
- [ ] **D-CHK-05** — `CheckTenLines(G0)` → 10라인 `sum==34`, `ok==True` · Invariant: FR-02, MAGIC_SUM · (D-04)
- [ ] **D-CHK-06** — 실패 보드 → 각 line에 `id,type,index,sum,ok` 존재 · Invariant: PRD §4.1 · (D-04)

### D-SUM (Skill SK-01)

- [ ] **D-SUM-01** — `SumRow(G0, 0)` → `34` · Invariant: R-VAL-01, 0-index
- [ ] **D-SUM-02** — `SumCol(G0, 0)` → `34` · Invariant: R-VAL-01
- [ ] **D-SUM-03** — `SumDiag(G0, 1)` 주대각 → `34` · Invariant: PRD diag index 1
- [ ] **D-SUM-04** — `SumDiag(G0, 2)` 부대각 → `34` · Invariant: PRD diag index 2

### D-CTL / D-NEG (control · ECB)

- [ ] **D-CTL-01** — `CheckTenLines(G0)` 2회 → `lines`, `all_ok` deep equal · Invariant: SC-3, FR-05 · TL-03
- [ ] **D-CTL-02** — `G0` → entity `CheckTenLines` 1회 위임 (Mock 금지) · Invariant: ECB control→entity
- [ ] **D-NEG-01** — entity에 `G3` 직접 `CheckTenLines` 호출 금지 · Invariant: entity E001~E005 처리 금지

### Track B 권장 RED 순서

- [ ] D-ASM-01 (TL-01) → D-CHK-01, D-CHK-03 (TL-02) → D-CTL-01 (TL-03)

### 기존 D-ID 매핑

- [ ] D-01 → D-ASM-01
- [ ] D-02 → D-CHK-01
- [ ] D-03 → D-CTL-01
- [ ] D-04 → D-CHK-03, D-CHK-05, D-CHK-06

---

## TL · AC 추적성

- [ ] **TL-01** (AC-01) — D-ASM-01
- [ ] **TL-02** (AC-02) — D-CHK-01, D-CHK-04
- [ ] **TL-03** (AC-03) — D-CTL-01
- [ ] **TL-04** (AC-04) — U-IN-06, U-IN-08, U-FLOW-01, U-FLOW-02

---

## E001~E004 ↔ PRD `E_*` 매핑 (boundary)

- [ ] **E001** ↔ `E_INPUT_SIZE` (I1)
- [ ] **E002** ↔ `E_EMPTY_COUNT` (I2)
- [ ] **E003** ↔ `E_VALUE_RANGE` (I3)
- [ ] **E004** ↔ `E_DUPLICATE` (I4)

---

## RED 테스트 docstring 템플릿

```text
Phase: RED | Layer: entity | Track: Logic | TL: TL-01 | ID: D-ASM-01 | FR-04 AC-01
```

```text
Phase: RED | Layer: boundary | Track: UI | TL: TL-04 | ID: U-IN-06 | FR-01 AC-04
```

---

## pytest 실행 (RED 확인)

```bash
cd c:\DEV\MagicSquare_1004
python -m pip install -e ".[dev]" -q
python -m pytest tests/boundary/test_u_validate_input_empty_count.py -v
python -m pytest tests/entity/test_d_assert_complete_row_only.py -v
```

- [ ] RED 성공 확인: `FAILED` ≥ 1 (의도된 실패)
- [ ] `passed`만 나오면 assert/import 점검

---

## 참고

- **Expected RED Failure:** `ImportError` / `ModuleNotFoundError` · `AssertionError` · `pytest.fail("RED: ...")`
- **1차 비범위:** Solver, `int[6]`, GUI
- **교안 예시** (`find_blank_coords`, I6~I11)와 별도 — 본 체크리스트는 PRD Command·I1~I4 기준
