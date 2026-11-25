"""Пути репозитория. Корни out/ и cache/ можно переопределить через OUT_DIR / CACHE_DIR (тесты)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
CONFIG = ROOT / "config"
PROMPTS = ROOT / "prompts"
DOMAIN = ROOT / "domain"
ORGANIZERS = DATA / "organizers"
SCHEMAS = ORGANIZERS / "01_схемы"


def out_root() -> Path:
    return Path(os.environ.get("OUT_DIR") or ROOT / "out")


def cache_root() -> Path:
    return Path(os.environ.get("CACHE_DIR") or ROOT / "cache")


def out_dir(ch: str) -> Path:
    return out_root() / ch


def metrics_dir() -> Path:
    return out_root() / "_metrics"


def pages_dir(ch: str) -> Path:
    return DATA / "pages" / ch


def units(ch: str) -> Path:
    return out_dir(ch) / "units.json"


def layer(ch: str) -> Path:
    return out_dir(ch) / "layer.json"


def coverage(ch: str) -> Path:
    return out_dir(ch) / "coverage.json"


def routing(ch: str) -> Path:
    return out_dir(ch) / "routing.json"
