"""Shared pytest fixtures — grid data only (no domain logic)."""

import importlib.util
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# tests/entity/ shadows src/entity; preload domain package from src.
_entity_init = _SRC / "entity" / "__init__.py"
_entity_spec = importlib.util.spec_from_file_location(
    "entity",
    _entity_init,
    submodule_search_locations=[str(_SRC / "entity")],
)
_entity = importlib.util.module_from_spec(_entity_spec)
assert _entity_spec.loader is not None
sys.modules["entity"] = _entity
_entity_spec.loader.exec_module(_entity)

# tests/entity/ shadows src/entity on import; load SSOT constants by file path.
_CONSTANTS_PATH = _SRC / "entity" / "constants.py"
_spec = importlib.util.spec_from_file_location("entity.constants", _CONSTANTS_PATH)
_constants = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_constants)
GRID_SIZE = _constants.GRID_SIZE
MAGIC_SUM = _constants.MAGIC_SUM
VALUE_MAX = _constants.VALUE_MAX

# G1_LOC: 0 at 0-index (1,2) and (3,3) — 1-index blanks (2,3), (4,4); row-major
_G1_LOC = [
    [VALUE_MAX, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [3, 15, 14, 0],
]


@pytest.fixture
def grid_g1():
    """G1_LOC partial board: exactly two blanks, row-major fixture for D-LOC-*."""
    _ = (GRID_SIZE, MAGIC_SUM)  # SSOT 참조 (픽스처 데이터 검증용 상수)
    return [row[:] for row in _G1_LOC]
