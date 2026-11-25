"""Счёт ответа модуля проверки скриптом организаторов (как считает жюри).

python -m pipeline.verify.eval --answer <ответ.json> [--key <key.json>]

По умолчанию ключ — контрольный пакет. Запускать ТОЛЬКО после прогона модуля:
вывод раскрывает, какие цели были ошибками.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK_DIR = ROOT / "data" / "organizers" / "02_модуль_проверки"
SCORER = CHECK_DIR / "score_review.py"
CONTROL_KEY = CHECK_DIR / "контрольный_пакет" / "key.json"


def score(answer, key=CONTROL_KEY):
    for p in (SCORER, Path(answer), Path(key)):
        if not Path(p).exists():
            raise FileNotFoundError(f"{p} не найден")
    r = subprocess.run([sys.executable, str(SCORER), str(answer), str(key)], capture_output=True,
                       text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
    if r.returncode != 0:
        raise RuntimeError(f"score_review.py упал:\n{r.stderr}")
    return r.stdout


def main(argv=None):
    ap = argparse.ArgumentParser(description="Счёт ответа модуля проверки по ключу")
    ap.add_argument("--answer", required=True)
    ap.add_argument("--key", default=str(CONTROL_KEY))
    a = ap.parse_args(argv)
    print(score(a.answer, a.key), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
