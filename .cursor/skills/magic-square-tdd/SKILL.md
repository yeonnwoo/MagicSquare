---
name: magic-square-tdd
description: >-
  MagicSquare_1004 Dual-Track TDD·ECB 개발 절차. RED→GREEN→REFACTOR 전체 사이클,
  Logic/UI Track pytest, Mock·E001~E007·MagicConstant SSOT 준수.
  Use when implementing or testing ValidateInput, CheckTenLines, AssertComplete,
  or when the user mentions Phase RED/GREEN/REFACTOR, D-*/U-* tests, TL-01~04.
disable-model-invocation: true
---

# MagicSquare_1004 — Dual-Track TDD Skill

상위 헌법: [`.cursorrules`](../../.cursorrules) · 계약: [`docs/PRD.md`](../../../docs/PRD.md) · D-ID: [`reference.md`](reference.md)

---

## 언제 이 Skill을 켜는지

| 켜기 (이 Skill 사용) | 끄기 (Command·Loop만) |
|----------------------|------------------------|
| **RED→GREEN→REFACTOR** 한 TL·한 Command를 끝까지 | **RED만** — 실패 테스트 1파일 추가 |
| Logic·UI **Track 선택·Mock 판단**이 필요할 때 | **ECB·계약 리뷰만** — 코드·pytest 없음 |
| Layer(entity/control/boundary) **분산 구현** | 단일 함수 시그니처 1줄 추가 수준 |
| 완료 보고·pytest **게이트**가 필요할 때 | |

시작 시 한 줄 선언:

`Phase: RED|GREEN|REFACTOR | Layer: entity|control|boundary | Track: Logic|UI | TL: TL-0N | D-ID: D-0N`

---

## Logic Track vs UI Track

| Track | Layer | 테스트 ID | 파일 | Mock |
|-------|-------|-----------|------|------|
| **Logic** | entity, control | `D-*` | `tests/*/test_d_*.py` | **금지** — 도메인·합산·판정 Mock/패치 금지 |
| **UI** | boundary | `U-*` | `tests/boundary/test_u_*.py` | **허용** — CLI·파일·포트·시계만 |

| TL | 권장 Track | Layer | 파일 예 |
|----|------------|-------|---------|
| TL-01 | Logic | entity | `tests/entity/test_d_*.py` |
| TL-02 | Logic | entity 또는 control | `tests/entity/` 또는 `tests/control/` |
| TL-03 | Logic | control | `tests/control/test_d_*.py` |
| TL-04 | UI | boundary | `tests/boundary/test_u_*.py` |

---

## ECB · Mock · 오류 코드

**Import (허용만):** `boundary → control → entity`

| 금지 | 허용 |
|------|------|
| entity → boundary/control/I/O | control → entity |
| control → boundary | boundary → control |
| boundary → entity 직접 | |

**오류**

- **boundary**만 **E001~E007** 정의·노출 (PRD `E_*`와 매핑 표는 후속).
- **entity**는 **E001~E005 처리 금지** — 유효 `matrix`만 입력.
- **control**: 오케스트레이션; 입력 위반은 boundary에서 차단 후 진입.

**1차 범위 (PRD §1.3):** `ValidateInput`, `CheckTenLines`, `AssertComplete`만. Solver·`int[6]` RED/구현 **금지**.

**인덱스:** 내부 `matrix` **0-index** `[0..3]` · `int[6]` 좌표만 **1-index** `[1..4]`.

**MagicConstant:** `34`/`16`/`4`/`2`/`10` 리터럴 산재 금지 → SSOT 모듈만.

---

## RED (5~7단계)

1. **선언** — Phase/Layer/Track/TL/D-ID.
2. **계약 확인** — PRD FR·AC·해당 Command 시그니처(머릿속 또는 주석).
3. **테스트 파일** — Track에 맞는 `test_d_*` 또는 `test_u_*` 생성; docstring에 Track·Layer·TL·FR.
4. **실패 assertion** — Mom Test 의도 반영(예: 행합만 34 → `AssertComplete`는 `false`); **skip/xfail/assert 완화 금지**.
5. **fixture** — 4×4 보드·상수는 SSOT·헬퍼 사용; Logic Track에서 도메인 Mock 금지.
6. **실행** — `python -m pytest <해당 경로> -v` → **반드시 실패** 확인.
7. **기록** — 실패 메시지·기대 vs 실제 한 줄; GREEN 전 `src/` 변경 **최소·없음**.

---

## GREEN (5~7단계)

1. **선언** — Phase: GREEN, 동일 TL/D-ID.
2. **최소 구현** — 해당 테스트를 통과시키는 **가장 작은** `src/` 변경만.
3. **Layer 준수** — 도메인 합산·10라인 → entity; Command 조합 → control; E코드 변환 → boundary.
4. **상수** — 새 리터럴 금지; SSOT import.
5. **실행** — `python -m pytest <해당 TL 경로> -v` → **해당 RED 전부 pass**.
6. **회귀** — `python -m pytest tests/ -v` (기존 테스트 유지).
7. **기록** — 변경 파일·통과한 D-ID/U-ID 목록.

---

## REFACTOR (5~7단계)

1. **선언** — Phase: REFACTOR; 테스트 의미 변경 **금지**.
2. **중복 제거** — 합산·라인 순회 등 SK-01/SK-02 후보 추출(entity 우선).
3. **이름·경계** — Command/Skill 역할에 맞게 파일·함수 정리.
4. **import 검사** — ECB 역방향 없음.
5. **실행** — `python -m pytest tests/ -v` — 전부 green 유지.
6. **스냅샷/Golden** — baseline 갱신 시 사용자 **「재생성 승인」** 턴에서만.
7. **기록** — 리팩터 요약; 동작 변경 없음 명시.

---

## Test / Review Loop — pytest 언제

| 시점 | 명령 | 통과 조건 |
|------|------|-----------|
| RED 직후 | `pytest <신규 test 파일> -v` | **실패** (의도된 RED) |
| GREEN 중 | `pytest <TL 관련 path> -v` | 해당 TL **pass** |
| GREEN 끝 | `pytest tests/ -v` | 전체 **pass** |
| REFACTOR 끝 | `pytest tests/ -v` | 전체 **pass**, 의미 동일 |
| Review (코드 없음) | pytest **실행 안 함** | PRD·Report·`.cursorrules` 체크리스트만 |

**금지:** RED에서 skip/xfail; GREEN에서 테스트 완화; 승인 없는 Golden 재생성.

---

## 완료 보고 항목

세션 종료 시 아래를 한국어로 보고:

1. **Phase** 최종 상태 (RED / GREEN / REFACTOR)
2. **Track · Layer · TL · D-ID / U-ID**
3. **변경 파일** (`src/`, `tests/` 목록)
4. **pytest 결과** (명령 + passed/failed 수)
5. **AC·FR·Mom Test** 매핑 한 줄 (예: TL-01 ↔ SC-1 ↔ FR-04)
6. **미완** — 다음 Phase, 남은 TL, 계약 drift 있으면 명시
7. **git** — commit/push는 사용자 요청 시만 수행했는지

---

## Command와의 관계

- **Command** — `ValidateInput` / `CheckTenLines` / `AssertComplete` **단일 호출·시그니처** 수준.
- **이 Skill** — 위 Command를 포함한 **TL 단위 전체 TDD 사이클** + Track·Mock·pytest 게이트.
- Command 파일(`.cursor/commands/`)은 본 Skill과 **별도** 후속 생성.

추가 참고: [`reference.md`](reference.md) (Logic `D-*` ID만)
