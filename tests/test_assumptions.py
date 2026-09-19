from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.assumptions import load_assumptions


def test_load_assumptions():
    assumptions = load_assumptions()

    assert isinstance(assumptions, dict)
    assert "forecast" in assumptions
    assert "terminal" in assumptions