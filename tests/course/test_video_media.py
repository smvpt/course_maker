"""Видео П4: out/<ch>/videos/<узел>.short|long/ с <video_id>.mp4, <video_id>.vtt и passport.json. Старый videos/<узел>/ — запасной."""
import json
import re
from pathlib import Path

from contracts.models import Layer
from pipeline.course.build import build, video_dirs

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
RES, PORO = "mini.resistivity_depends_on_fluid", "mini.porosity_basics"
SCORES = {"time": 1, "invisible": 1, "scale": 1, "counterintuitive": 1, "cause_effect": 1}


def _out(tmp_path, routes=None) -> Path:
    layer = Layer.model_validate_json(MINI.read_text(encoding="utf-8"))
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    if routes:
        (d / "routing.json").write_text(json.dumps({"chapter": "mini_test", "routes": [
            {"node_id": n, "format": f, "video_scores": SCORES, "why": "тест"} for n, f in routes]}, ensure_ascii=False), encoding="utf-8")
    return tmp_path / "out"


def _video(out, vid, mp4=True, vtt=True, passport=True, mp4_name=None):
    d = out / "mini_test/videos" / vid
    d.mkdir(parents=True)
    if mp4:
        (d / (mp4_name or f"{vid}.mp4")).write_bytes(b"\x00\x00\x00\x18ftypmp42")
    if vtt:
        (d / f"{vid}.vtt").write_text("WEBVTT\n\n00:00.000 --> 00:02.000\nПривет\n", encoding="utf-8")
    if passport:
        (d / "passport.json").write_text("{}", encoding="utf-8")
    (d / "script.json").write_text("{}", encoding="utf-8")


def _html(tmp_path, out, nid=RES):
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    return course, (course / f"step-{nid}.html").read_text(encoding="utf-8")


def test_short_video_is_the_main_player_with_subtitles_and_passport(tmp_path):
    out = _out(tmp_path)
    _video(out, f"{RES}.short")
    course, html = _html(tmp_path, out)
    assert f'<video controls preload="metadata" src="media/{RES}.short/{RES}.short.mp4">' in html
    assert re.search(rf'<track kind="subtitles" srclang="ru" label="[^"]+" src="media/{re.escape(RES)}\.short/{re.escape(RES)}\.short\.vtt"', html)
    assert f'href="media/{RES}.short/passport.json"' in html and html.count("<video") == 1
    for name in (f"{RES}.short.mp4", f"{RES}.short.vtt", "passport.json"):
        assert (course / f"media/{RES}.short/{name}").exists()


def test_long_video_is_a_second_player_under_more(tmp_path):
    out = _out(tmp_path)
    _video(out, f"{RES}.short")
    _video(out, f"{RES}.long")
    course, html = _html(tmp_path, out)
    assert html.count("<video") == 2
    main, more = html[html.index("<video"):].split("</video>")[:2]
    assert f"{RES}.short.mp4" in main and f"{RES}.long.mp4" in more
    assert 'preload="none"' in more and f"{RES}.long.vtt" in more                 # второй плеер не грузится, пока не раскрыт
    assert "Подробнее: длинный разбор" in html and re.search(r"<details class=\"fold\">(?:(?!</details>).)*<video", html, re.S)
    assert f'href="media/{RES}.long/passport.json"' in html and f'href="media/{RES}.short/passport.json"' in html
    assert (course / f"media/{RES}.long/{RES}.long.mp4").exists()


def test_only_long_video_becomes_the_main_player(tmp_path):
    out = _out(tmp_path)
    _video(out, f"{RES}.long")
    _, html = _html(tmp_path, out)
    assert html.count("<video") == 1 and f"media/{RES}.long/{RES}.long.mp4" in html and "Подробнее" not in html


def test_catalog_without_mp4_is_not_a_video(tmp_path):
    out = _out(tmp_path, routes=[(RES, "шортс")])
    _video(out, f"{RES}.short", mp4=False, vtt=False)
    _, html = _html(tmp_path, out)
    assert "<video" not in html
    assert f'href="media/{RES}.short/passport.json"' in html and "паспорте ролика" in html     # как раньше: ссылка на спецификацию сцены


def test_spec_only_long_next_to_real_short_does_not_make_a_second_player(tmp_path):
    out = _out(tmp_path)
    _video(out, f"{RES}.short")
    _video(out, f"{RES}.long", mp4=False)
    _, html = _html(tmp_path, out)
    assert html.count("<video") == 1 and "Подробнее" not in html


def test_missing_subtitles_mean_no_track_and_any_mp4_name_is_accepted(tmp_path):
    out = _out(tmp_path)
    _video(out, f"{RES}.short", vtt=False, mp4_name="render_final.mp4")
    _, html = _html(tmp_path, out)
    assert "render_final.mp4" in html and "<track" not in html


def test_old_layout_by_node_id_still_works(tmp_path):
    out = _out(tmp_path)
    _video(out, RES, mp4_name="clip.mp4")
    (out / f"mini_test/videos/{RES}/{RES}.vtt").rename(out / f"mini_test/videos/{RES}/clip.vtt")
    course, html = _html(tmp_path, out)
    assert f'src="media/{RES}/clip.mp4"' in html and f'src="media/{RES}/clip.vtt"' in html


def test_video_dirs_order_and_index_icon(tmp_path):
    out = _out(tmp_path)
    _video(out, f"{RES}.long")
    _video(out, f"{RES}.short")
    _video(out, RES, mp4_name="clip.mp4")
    assert [(f, v) for f, v, _ in video_dirs(out / "mini_test", RES)] == [("short", f"{RES}.short"), ("long", f"{RES}.long"), ("legacy", RES)]
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    index = (course / "index.html").read_text(encoding="utf-8")
    assert "ролик" in index.split(f'data-node="{RES}"')[1].split("</li>")[0]
    text = (course / "assets/course-data.js").read_text(encoding="utf-8")
    steps = json.loads(text[len("window.COURSE_DATA = "):].rstrip().rstrip(";"))["meta"]["steps"]
    assert steps[0]["video"] in (True, False) and [s for s in steps if s["id"] == RES][0]["video"] is True


def test_step_without_any_video_dir_has_no_media_block(tmp_path):
    out = _out(tmp_path)
    _, html = _html(tmp_path, out, PORO)
    assert 'id="b-media"' not in html
