"""Partial-board solver — entity layer (FR-SOL-01 step A: row-sum fill)."""

from entity.constants import BLANK_VALUE, COORD_INDEX_BASE, MAGIC_SUM
from entity.loc import find_blank_coords


def solve_step_a(matrix: list[list[int]]) -> list[int]:
    """Return int[6]: [r1,c1,n1,r2,c2,n2] — 1-index coords, row-major blanks."""
    out: list[int] = []
    for row_1, col_1 in find_blank_coords(matrix):
        row_0 = row_1 - COORD_INDEX_BASE
        row = matrix[row_0]
        filled_sum = sum(value for value in row if value != BLANK_VALUE)
        out.extend([row_1, col_1, MAGIC_SUM - filled_sum])
    return out
