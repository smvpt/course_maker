"""Репозиторий собирается с чистого клона: make install ставит зависимости всех модулей."""
import re

from pipeline.common import paths


def test_requirements_include_every_module_file_pinned():
    root = (paths.ROOT / "requirements.txt").read_text(encoding="utf-8")
    included = set(re.findall(r"^-r\s+(\S+)\s*$", root, re.M))
    for f in sorted((paths.ROOT / "requirements").glob("*.txt")):
        rel = f"requirements/{f.name}"
        assert rel in included, f"{rel} не включён в requirements.txt — у жюри не установится"
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.split("#")[0].strip()
            if line and not line.startswith("-"):
                assert re.fullmatch(r"[A-Za-z0-9_.\[\],-]+==[\w.]+", line), f"{rel}: версия не закреплена: {line}"
