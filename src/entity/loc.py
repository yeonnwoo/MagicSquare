"""Blank-cell location — entity layer (FR-LOC-01)."""

from entity.constants import BLANK_VALUE, COORD_INDEX_BASE


def find_blank_coords(matrix: list[list[int]]) -> list[tuple[int, int]]:
    """Return 1-index (row, col) of each blank, row-major order."""
    coords: list[tuple[int, int]] = []
    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            if value == BLANK_VALUE:
                coords.append(
                    (row_idx + COORD_INDEX_BASE, col_idx + COORD_INDEX_BASE)
                )
    return coords
