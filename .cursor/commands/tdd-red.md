# TDD RED — 실패 테스트 먼저

MagicSquare_1004 **Dual-Track TDD** — **RED 단계만**. 구현(`src/`) 변경 없이 `tests/`에 실패하는 테스트를 추가한다.

상위: [`.cursorrules`](../../.cursorrules) · [`docs/PRD.md`](../../docs/PRD.md) · D-ID: [`.cursor/skills/magic-square-tdd/reference.md`](../skills/magic-square-tdd/reference.md)

전체 사이클(GREEN·REFACTOR)은 Skill `magic-square-tdd` — 본 Command는 **RED 조각**만.

---

## 필수 선언

응답 **첫 줄**에 반드시 출력:

```
Phase: RED | Layer: entity|control|boundary | Track: Logic|UI | TL: TL-0N | ID: D-0N|U-0N
```

- **Logic Track** → `D-*`, `tests/entity/` 또는 `tests/control/`, `test_d_*.py`
- **UI Track** → `U-*`, `tests/boundary/`, `test_u_*.py`
- **1차 범위:** TL-01~04, CMD `ValidateInput` / `CheckTenLines` / `AssertComplete`만 (Solver·`int[6]` 금지)

---

## 절차

1. **ID 확인** — 사용자 또는 PRD에서 **TL-xx** 확정 → `reference.md`에서 **D-ID/U-ID**, Layer, Command 매핑 확인.
2. **계약 확인** — 해당 TL의 FR·AC·Mom Test 의도(예: TL-01 = 행합만 34여도 `AssertComplete` → `false`).
3. **파일 위치** — Track·Layer에 맞는 `tests/<layer>/test_d_*.py` 또는 `test_u_*.py` (신규 또는 기존 파일에 테스트 1개 추가).
4. **AAA 테스트 작성**
   - **Arrange** — 4×4 `matrix` fixture; 상수는 MagicConstant SSOT(없으면 테스트 내 임시 상수만, **리터럴 34/16 산재 금지**는 구현 시 적용 — RED에서는 fixture 헬퍼 허용).
   - **Act** — 대상 Command 호출(아직 없으면 `pytest.raises(ImportError)` 또는 스텁 import **금지** → **미구현 시 실패**가 나도록 실제 import 경로 사용).
   - **Assert** — AC를 **엄격히** 표현; `pytest.approx`로 합 34 완화 금지.
5. **docstring** — Track, Layer, TL, FR/AC, D-ID/U-ID 명시.
6. **pytest FAIL** — 아래 bash 실행; **반드시 실패** 확인(0 failed면 RED 아님 → assert/import 점검).
7. **보고** — 아래 보고 섹션 형식으로 종료.

---

## pytest 예시 (bash)

```bash
cd c:\DEV\MagicSquare_1004
python -m pip install -e ".[dev]" -q

# 단일 RED 파일 (권장)
python -m pytest tests/entity/test_d_assert_complete_row_only.py -v

# TL-04 boundary 예
python -m pytest tests/boundary/test_u_validate_input_empty_count.py -v

# 디렉터리 단위 (해당 Layer만)
python -m pytest tests/entity/ -v --tb=short -x
```

**RED 성공 조건:** `FAILED` ≥ 1 (의도된 실패). `passed`만 나오면 테스트가 너무 약하거나 이미 구현됨.

---

## 보고

RED 종료 시 다음만 간결히 보고:

| 항목 | 내용 |
|------|------|
| **테스트 ID** | D-0N 또는 U-0N, TL-0N |
| **FAIL 요약** | 실패 테스트명 + assert/ImportError 한 줄 |
| **변경 파일** | `tests/` 아래 경로만 (목록) |
| **다음** | GREEN 시 수정할 `src/` Layer 힌트 1줄 |

---

## 금지

| 금지 | 이유 |
|------|------|
| **`src/` 수정** | RED는 테스트만 |
| **Logic Track에서 Domain Mock** | `unittest.mock`·패치로 합산/판정/행렬 조작 금지 |
| **assert 완화·`skip`·`xfail`** | Mom Test·TL 의도 훼손 |
| **GREEN·REFACTOR 작업** | `/tdd-green` 등 별 Command(후속) 또는 Skill |
| **테스트 통과시키기 위한 구현** | FAIL이 목적 |
| **1차 범위 밖** Solver·`int[6]` RED | PRD Out-of-Scope |

**허용 (UI Track만):** CLI·파일·환경 **I/O Mock** — 도메인 계산 Mock은 여전히 금지.

---

## TL 빠른 참조

| TL | Track | ID 예 | Command |
|----|-------|-------|---------|
| TL-01 | Logic | D-01 | `AssertComplete` |
| TL-02 | Logic | D-02 | `CheckTenLines` |
| TL-03 | Logic | D-03 | `CheckTenLines` |
| TL-04 | UI | U-01~U-04 | `ValidateInput` |
