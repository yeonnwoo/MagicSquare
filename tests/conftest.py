"""Shared pytest fixtures — grid data only (no domain logic)."""

import importlib.util
from pathlib import Path

import pytest

# tests/entity/ shadows src/entity on import; load SSOT constants by file path.
_CONSTANTS_PATH = Path(__file__).resolve().parents[1] / "src" / "entity" / "constants.py"
_spec = importlib.util.spec_from_file_location("entity.constants", _CONSTANTS_PATH)
_constants = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_constants)
GRID_SIZE = _constants.GRID_SIZE
MAGIC_SUM = _constants.MAGIC_SUM
VALUE_MAX = _constants.VALUE_MAX

# G1_LOC: 0 at 0-index (1,1) and (2,2) — 1-index blanks (2,2), (3,3); row-major
_G1_LOC = [
    [VALUE_MAX, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


@pytest.fixture
def grid_g1():
    """G1_LOC partial board: exactly two blanks, row-major fixture for D-LOC-*."""
    _ = (GRID_SIZE, MAGIC_SUM)  # SSOT 참조 (픽스처 데이터 검증용 상수)
    return [row[:] for row in _G1_LOC]
