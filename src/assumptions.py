from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSUMPTIONS_PATH = PROJECT_ROOT / "data" / "assumptions.yaml"


def load_assumptions(path: Path = ASSUMPTIONS_PATH) -> dict:
    """Load valuation assumptions from a YAML file."""
    with open(path, "r") as file:
        return yaml.safe_load(file)