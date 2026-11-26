"""out/<ch>/metrics.csv по шаблону организаторов: строка на этап (layer, routing, course, video, review).

Токены и деньги — из out/_metrics/llm_calls.jsonl (только настоящие вызовы, попадания в кэш не в счёт).
Человеко-минуты — из journal/manual_edits.csv (по файлу правки определяется этап).
Секунды видео — из passport.json роликов главы.
python -m pipeline.common.metrics --ch <id>
"""
import argparse
import csv
import json
from pathlib import Path

from contracts.models import Layer, MetricsRow
from pipeline.common import io, paths

JOURNAL = paths.ROOT / "journal" / "manual_edits.csv"
STAGES = ["layer", "routing", "course", "video", "review"]
PROMPT_STAGE = {"core/route": "routing", "core": "layer", "course": "course", "video": "video", "verify": "review"}
FIELDS = [f for f in MetricsRow.model_fields if f != "ext"]   # ext — не колонка шаблона


def prompt_stage(prompt: str) -> str:
    if prompt in PROMPT_STAGE:
        return PROMPT_STAGE[prompt]
    head = prompt.split("/", 1)[0]
    if head not in PROMPT_STAGE:
        raise ValueError(f"промпт {prompt}: неизвестно, к какому этапу metrics.csv он относится")
    return PROMPT_STAGE[head]


def file_stage(path: str) -> str:
    p = path.replace("\\", "/")
    for key, stage in (("routing", "routing"), ("/verify", "review"), ("verify/", "review"), ("video", "video"),
                       ("course", "course"), ("illus", "course")):
        if key in p:
            return stage
    return "layer"


def video_seconds(ch: str) -> float:
    total = 0.0
    for f in (paths.out_dir(ch) / "videos").glob("*/passport.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        total += float(d.get("duration_s") or d.get("duration") or 0)
    return total


def build(ch: str) -> list[MetricsRow]:
    acc = {s: {"in": 0, "out": 0, "usd": 0.0, "min": 0} for s in STAGES}
    log = paths.metrics_dir() / "llm_calls.jsonl"
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            c = json.loads(line)
            if c.get("chapter") != ch or c.get("cache_hit"):
                continue
            a = acc[prompt_stage(c["prompt"])]
            a["in"] += c.get("tokens_in") or 0
            a["out"] += c.get("tokens_out") or 0
            a["usd"] += c.get("money_usd") or 0.0
    if JOURNAL.exists():
        with open(JOURNAL, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("chapter") == ch:
                    acc[file_stage(r.get("file", ""))]["min"] += int(float(r.get("person_minutes") or 0))
    nodes = len(io.load(Layer, paths.layer(ch)).nodes) if paths.layer(ch).exists() else 0
    vsec = video_seconds(ch)
    total_min = sum(a["min"] for a in acc.values())
    return [MetricsRow(chapter=ch, stage=s, nodes=nodes, llm_tokens_in=a["in"], llm_tokens_out=a["out"],
                       money_usd=round(a["usd"], 6), person_minutes=a["min"], mentor_minutes=0,
                       video_seconds=vsec if s == "video" else 0.0,
                       manual_share=round(a["min"] / total_min, 3) if total_min else 0.0)
            for s, a in acc.items()]


def write(ch: str) -> Path:
    out = paths.out_dir(ch) / "metrics.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in build(ch):
            w.writerow(r.model_dump(include=set(FIELDS)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pipeline.common.metrics", description="metrics.csv главы")
    ap.add_argument("--ch", required=True)
    print(write(ap.parse_args(argv).ch))


if __name__ == "__main__":
    main()
