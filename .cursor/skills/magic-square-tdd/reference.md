# D-* 테스트 ID (Logic Track)

| D-ID | TL | Layer | Command | 요지 |
|------|-----|--------|---------|------|
| D-01 | TL-01 | entity | `AssertComplete` | 행합만 34 → `false` (SC-1) |
| D-02 | TL-02 | entity | `CheckTenLines` | 대각 실패 → `first_failing.type == diag` |
| D-03 | TL-03 | control | `CheckTenLines` | 동일 보드 2회 → 결과 동일 |
| D-04 | TL-02 | entity | `CheckTenLines` | 10라인 합·`all_ok` 필드 구조 |

*입력 계약 TL-04 → UI Track `U-01`~`U-04` (boundary, `test_u_*`).*
