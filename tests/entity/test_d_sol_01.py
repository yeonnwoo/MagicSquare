"""Phase: GREEN | Layer: entity | Track: Logic | ID: D-SOL-01 | FR-SOL-01"""

from entity.sol import solve_step_a


def test_d_sol_01_step_a_success(grid_g1):
    """D-SOL-01: solve_step_a — row-sum fill, int[6] 1-index row-major."""
    # Given: G1 격자 (0이 2개, 빈칸 (2,3)·(4,4))
    # When: solve_step_a(grid_g1) 호출
    result = solve_step_a(grid_g1)
    # Then: [r1,c1,n1,r2,c2,n2] = [2,3,11,4,4,2]
    assert result == [2, 3, 11, 4, 4, 2]
