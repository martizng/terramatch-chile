"""Loads config/terramatch_config.json, the single place where the rules of the project doc v2.0 live."""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "terramatch_config.json"


def load(path=CONFIG_PATH):
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    w = sum(v["weight"] for v in cfg["variables"].values())
    assert abs(w - 1) < 1e-6, "weights must sum to 1"
    return cfg


CFG = load()
VARS = tuple(CFG["variables"])
