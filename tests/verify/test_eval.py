import json

from pipeline.verify.eval import score


def test_score_with_own_key(tmp_path):
    key = {"package_id": "x",
           "errors": [{"target": "C001", "severity": "critical", "pages": [2]},
                      {"target": "C002", "severity": "minor", "pages": [3]}],
           "tricky_true": [{"target": "C003"}]}
    ans = {"package_id": "x", "remarks": [
        {"target": "C001", "category": "sign_flip", "severity": "critical", "problem": "p", "fix": "f", "page_pdf": 2},
        {"target": "C003", "category": "other", "severity": "minor", "problem": "p", "fix": "f", "page_pdf": 1}]}
    (tmp_path / "k.json").write_text(json.dumps(key), encoding="utf-8")
    (tmp_path / "a.json").write_text(json.dumps(ans), encoding="utf-8")
    out = score(tmp_path / "a.json", tmp_path / "k.json")
    assert "Найдено полностью: 1, наполовину: 0, пропущено: 1" in out
    assert "Ложных тревог: 1, из них на верных, но неожиданных элементах: 1" in out
