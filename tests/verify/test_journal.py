import csv
import subprocess

import pytest

from contracts.models import MANUAL_EDITS_HEADER, ManualEdit
from journal import cli


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True,
                          encoding="utf-8").stdout.strip()


@pytest.fixture
def repo(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "t")
    (tmp_path / "out/ch1/course").mkdir(parents=True)
    (tmp_path / "out/ch1/course/step.json").write_text("{}", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "init")
    return tmp_path


def _rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_add_writes_row_and_commits(repo):
    f = repo / "out/ch1/course/step.json"
    f.write_text('{"x": 1}', encoding="utf-8")
    row = cli.add(repo, ch="ch1", minutes=6, what="исправлено число", files=["out/ch1/course/step.json"],
                  reason="число с соседней страницы", people=1, run_no=2)

    rows = _rows(repo / "journal/manual_edits.csv")
    assert list(rows[0].keys())[:len(MANUAL_EDITS_HEADER)] == MANUAL_EDITS_HEADER
    assert len(rows) == 1
    r = rows[0]
    ManualEdit.model_validate({k: r[k] for k in MANUAL_EDITS_HEADER})
    assert r["chapter"] == "ch1" and r["person_minutes"] == "6" and r["run_no"] == "2"
    assert r["file"] == "out/ch1/course/step.json"
    # хэш в записи — коммит с правкой файла
    assert r["commit"] == row["commit"]
    assert "out/ch1/course/step.json" in _git(repo, "show", "--name-only", "--format=", r["commit"])
    # журнал тоже закоммичен, рабочее дерево чистое
    assert _git(repo, "status", "--porcelain") == ""


def test_add_without_changes_fails(repo):
    with pytest.raises(RuntimeError):
        cli.add(repo, ch="ch1", minutes=1, what="ничего", files=["out/ch1/course/step.json"], reason="r")
    assert not (repo / "journal/manual_edits.csv").exists()


def test_add_missing_file_fails(repo):
    with pytest.raises(FileNotFoundError):
        cli.add(repo, ch="ch1", minutes=1, what="x", files=["out/ch1/nope.json"], reason="r")


def test_mentor_and_report(repo):
    for i, m in enumerate((6, 4)):
        (repo / "out/ch1/course/step.json").write_text(f'{{"x": {i}}}', encoding="utf-8")
        cli.add(repo, ch="ch1", minutes=m, what="правка", files=["out/ch1/course/step.json"], reason="r")
    cli.add_mentor(repo, ch="ch1", minutes=15, what="слот по спецификации")
    assert cli.minutes(repo) == {"ch1": {"person_minutes": 10, "mentor_minutes": 15, "edits": 2}}
    assert _git(repo, "status", "--porcelain") == ""
