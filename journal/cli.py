"""Журнал ручных правок (формат организаторов 05_шаблоны/manual_edits.csv) + git commit.

python -m journal.cli add --ch <id> --min <n> --what "..." --files <путь> [<путь> ...] --reason "..."
                          [--people 1] [--run-no 1]
python -m journal.cli add-mentor --ch <id> --min <n> --what "..."
python -m journal.cli report

add: коммитит правленые файлы, затем дописывает строку с хэшем этого коммита (колонка commit
сверх формата организаторов) и коммитит журнал. Журнал совпадает с историей коммитов.
"""
import argparse
import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from contracts.models import MANUAL_EDITS_HEADER, ManualEdit

ROOT = Path(__file__).resolve().parents[1]
EDITS = Path("journal/manual_edits.csv")
MENTOR = Path("journal/mentor_minutes.csv")
EDITS_HEADER = MANUAL_EDITS_HEADER + ["commit"]
MENTOR_HEADER = ["time", "chapter", "mentor_minutes", "what"]


def _git(root, *args):
    r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def _now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M")


def _append(path, header, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        if new:
            w.writeheader()
        w.writerow(row)


def add(root, ch, minutes, what, files, reason, people=1, run_no=1):
    root = Path(root)
    if not files:
        raise ValueError("нужен хотя бы один правленый файл (--files)")
    for f in files:
        if not (root / f).exists():
            raise FileNotFoundError(f"{root / f} не найден")
    row = ManualEdit(time=_now(), chapter=ch, file="; ".join(files), what_changed=what,
                     person_minutes=minutes, people=people, run_no=run_no, reason=reason)
    _git(root, "add", "-f", "--", *files)
    if not _git(root, "diff", "--cached", "--name-only", "--", *files):
        raise RuntimeError(f"в {files} нет изменений — записывать нечего")
    _git(root, "commit", "-q", "-m", f"[journal] {ch}: {what}", "--", *files)
    commit = _git(root, "rev-parse", "HEAD")
    rec = {k: getattr(row, k) for k in MANUAL_EDITS_HEADER} | {"commit": commit}
    _append(root / EDITS, EDITS_HEADER, rec)
    _git(root, "add", "--", str(EDITS))
    _git(root, "commit", "-q", "-m", f"[journal] запись: {ch}, {minutes} мин", "--", str(EDITS))
    return rec


def add_mentor(root, ch, minutes, what):
    root = Path(root)
    _append(root / MENTOR, MENTOR_HEADER, {"time": _now(), "chapter": ch, "mentor_minutes": minutes, "what": what})
    _git(root, "add", "--", str(MENTOR))
    _git(root, "commit", "-q", "-m", f"[journal] ментор: {ch}, {minutes} мин", "--", str(MENTOR))


def _read(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def minutes(root):
    """{глава: {person_minutes, mentor_minutes, edits}} по журналам."""
    root = Path(root)
    out = {}
    for r in _read(root / EDITS):
        d = out.setdefault(r["chapter"], {"person_minutes": 0, "mentor_minutes": 0, "edits": 0})
        d["person_minutes"] += int(r["person_minutes"])
        d["edits"] += 1
    for r in _read(root / MENTOR):
        d = out.setdefault(r["chapter"], {"person_minutes": 0, "mentor_minutes": 0, "edits": 0})
        d["mentor_minutes"] += int(r["mentor_minutes"])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Журнал ручных правок")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="правка результата: коммит файлов + строка журнала")
    a.add_argument("--ch", required=True)
    a.add_argument("--min", type=int, required=True, help="человеко-минуты")
    a.add_argument("--what", required=True)
    a.add_argument("--files", nargs="+", required=True, help="правленые файлы, пути от корня репозитория")
    a.add_argument("--reason", required=True, help="почему понадобилась правка")
    a.add_argument("--people", type=int, default=1)
    a.add_argument("--run-no", type=int, default=1, help="номер прогона, результат которого правили")
    m = sub.add_parser("add-mentor", help="минуты ментора")
    m.add_argument("--ch", required=True)
    m.add_argument("--min", type=int, required=True)
    m.add_argument("--what", required=True)
    sub.add_parser("report", help="минуты по главам")
    ns = ap.parse_args(argv)
    if ns.cmd == "add":
        rec = add(ROOT, ns.ch, ns.min, ns.what, ns.files, ns.reason, ns.people, ns.run_no)
        print(f"записано: {rec['chapter']}, {rec['person_minutes']} мин, коммит {rec['commit'][:8]}")
    elif ns.cmd == "add-mentor":
        add_mentor(ROOT, ns.ch, ns.min, ns.what)
        print(f"записано: ментор {ns.ch}, {ns.min} мин")
    else:
        rows = minutes(ROOT)
        if not rows:
            print("журнал пуст")
        for ch, d in sorted(rows.items()):
            print(f"{ch}: правок {d['edits']}, человеко-минут {d['person_minutes']}, минут ментора {d['mentor_minutes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
