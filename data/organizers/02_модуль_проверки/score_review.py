"""Подсчёт результата модуля проверки по ключу.

Запуск:  python score_review.py <ответ_модуля.json> <key.json>

Правила (как в ТЗ):
- тяжесть: critical = 3, significant = 2, minor = 1;
- находка засчитывается полностью, если замечание указывает на ту же цель,
  в нём есть исправление (fix) и верная страница (одна из pages ключа);
  наполовину — если цель верная, но нет исправления или страница неверная;
- замечание к цели, где ошибки нет, — ложная тревога
  (отдельно считаются ложные тревоги на «верных, но неожиданных» элементах);
- если на одну цель несколько замечаний, засчитывается первое.
"""
import json
import sys

W = {"critical": 3, "significant": 2, "minor": 1}


def main(out_path, key_path):
    out = json.load(open(out_path, encoding="utf-8"))
    key = json.load(open(key_path, encoding="utf-8"))
    errors = {e["target"]: e for e in key["errors"]}
    tricky = {t["target"] for t in key["tricky_true"]}

    seen, remarks = set(), []
    for r in out.get("remarks", []):
        if r.get("target") in seen:
            continue
        seen.add(r.get("target"))
        remarks.append(r)

    total = sum(W[e["severity"]] for e in errors.values())
    got, full, half, false_alarm, false_tricky = 0.0, 0, 0, 0, 0
    missed = set(errors)
    for r in remarks:
        e = errors.get(r.get("target"))
        if e is None:
            false_alarm += 1
            false_tricky += r.get("target") in tricky
            continue
        missed.discard(e["target"])
        ok_page = r.get("page_pdf") in e["pages"]
        ok_fix = bool(str(r.get("fix") or "").strip())
        if ok_page and ok_fix:
            got += W[e["severity"]]; full += 1
        else:
            got += W[e["severity"]] / 2; half += 1

    print(f"Ошибок в ключе: {len(errors)} (вес {total})")
    print(f"Найдено полностью: {full}, наполовину: {half}, пропущено: {len(missed)}")
    print(f"Доля найденного по весу: {got / total:.0%}")
    print(f"Доля найденного по числу (любая находка): {(full + half) / len(errors):.0%}")
    print(f"Ложных тревог: {false_alarm}, из них на верных, но неожиданных элементах: {false_tricky}")
    if missed:
        print("Пропущены:", ", ".join(sorted(missed)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
