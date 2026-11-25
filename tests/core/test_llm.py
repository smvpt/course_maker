"""pipeline/llm.py по интерфейсу CLAUDE.md §2 — без сети: провайдер подменён."""
import json

import pytest
from pydantic import BaseModel

from pipeline import llm


class Answer(BaseModel):
    value: int


@pytest.fixture
def env(tmp_path, monkeypatch):
    prompts = tmp_path / "prompts"
    (prompts / "core").mkdir(parents=True)
    (prompts / "core" / "t.md").write_text("Посчитай {{x}} и {{ y }}. Пропуски задания {{1}} не трогать.",
                                           encoding="utf-8")
    llm_dir = llm.paths.PROMPTS
    for name in ("_json_suffix.md", "_json_retry.md"):
        (prompts / "core" / name).write_text((llm_dir / "core" / name).read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(llm.paths, "PROMPTS", prompts)
    monkeypatch.setenv("OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.delenv("LLM_OFFLINE", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("LLM_MODEL_DEFAULT", raising=False)
    monkeypatch.setenv("CH", "test_ch")
    calls = []

    def install(replies):
        it = iter(replies)

        def fake(model, messages, max_tokens, params):
            calls.append({"model": model, "messages": messages})
            return next(it), 100, 20, 0.5
        monkeypatch.setattr(llm, "_call", fake)
    return tmp_path, calls, install


def log_rows(tmp_path):
    return [json.loads(x) for x in (tmp_path / "out" / "_metrics" / "llm_calls.jsonl").read_text(encoding="utf-8").splitlines()]


def test_text_renders_vars_and_logs(env):
    tmp, calls, install = env
    install(["ответ"])
    assert llm.complete_text("core/t", {"x": 1, "y": "два"}) == "ответ"
    sent = calls[0]["messages"][0]["content"]
    assert "Посчитай 1 и два." in sent and "{{1}}" in sent
    row = log_rows(tmp)[0]
    assert row["prompt"] == "core/t" and row["chapter"] == "test_ch" and row["cache_hit"] is False
    assert row["tokens_in"] == 100 and row["tokens_out"] == 20 and row["money_usd"] == 0.0008   # цена из config/llm.yaml (4 и 20 $ за 1M)


def test_missing_and_extra_vars_fail(env):
    _, _, install = env
    install([])
    with pytest.raises(KeyError):
        llm.complete_text("core/t", {"x": 1})
    with pytest.raises(KeyError):
        llm.complete_text("core/t", {"x": 1, "y": 2, "z": 3})


def test_cache_hit_and_offline(env, monkeypatch):
    tmp, calls, install = env
    install(["ответ"])
    llm.complete_text("core/t", {"x": 1, "y": 2})
    monkeypatch.setenv("LLM_OFFLINE", "1")
    assert llm.complete_text("core/t", {"x": 1, "y": 2}) == "ответ"   # из кэша, без вызова
    assert len(calls) == 1
    assert log_rows(tmp)[-1]["cache_hit"] is True
    with pytest.raises(llm.OfflineCacheMiss):
        llm.complete_text("core/t", {"x": 1, "y": 3})


def test_cache_key_depends_on_model(env, monkeypatch):
    _, calls, install = env
    install(["a", "b"])
    llm.complete_text("core/t", {"x": 1, "y": 2})
    monkeypatch.setenv("LLM_MODEL", "openai/other")
    assert llm.complete_text("core/t", {"x": 1, "y": 2}) == "b"
    assert calls[1]["model"] == "openai/other"


def test_tier_model_override(env, monkeypatch):
    _, calls, install = env
    install(["a"])
    monkeypatch.setenv("LLM_MODEL", "x/all")
    monkeypatch.setenv("LLM_MODEL_STRONG", "x/strong")
    llm.complete_text("core/t", {"x": 1, "y": 2}, tier="strong")
    assert calls[0]["model"] == "x/strong"
    with pytest.raises(ValueError):
        llm.complete_text("core/t", {"x": 1, "y": 2}, tier="nope")


def test_json_valid_with_fence(env):
    _, calls, install = env
    install(['```json\n{"value": 7}\n```'])
    assert llm.complete_json("core/t", {"x": 1, "y": 2}, schema=Answer).value == 7
    assert '"value"' in calls[0]["messages"][0]["content"]   # схема ушла в промпт


def test_json_retry_then_ok(env):
    tmp, calls, install = env
    install(["не json", '{"value": "abc"}', '{"value": 3}'])
    assert llm.complete_json("core/t", {"x": 1, "y": 2}, schema=Answer).value == 3
    assert len(calls) == 3
    last = calls[2]["messages"]
    assert [m["role"] for m in last] == ["user", "assistant", "user", "assistant", "user"]
    assert log_rows(tmp)[-1]["attempts"] == 3


def test_json_gives_up_after_two_retries(env):
    tmp, calls, install = env
    install(["плохо", "плохо", "плохо", '{"value": 1}'])
    with pytest.raises(llm.LLMJSONError):
        llm.complete_json("core/t", {"x": 1, "y": 2}, schema=Answer)
    assert len(calls) == 3
    assert not list((tmp / "cache" / "llm").glob("*.json"))   # провал не кэшируется


def test_images_go_as_content_parts(env, tmp_path):
    _, calls, install = env
    img = tmp_path / "p1.png"
    img.write_bytes(b"\x89PNG fake")
    install(["ok"])
    llm.complete_text("core/t", {"x": 1, "y": 2}, tier="vision", images=[img])
    parts = calls[0]["messages"][0]["content"]
    assert parts[0]["type"] == "text"
    assert parts[1]["image_url"]["url"].startswith("data:image/png;base64,")
    with pytest.raises(FileNotFoundError):
        llm.complete_text("core/t", {"x": 1, "y": 2}, images=[tmp_path / "nope.png"])


class ServiceUnavailableError(Exception):      # имя как у litellm: повтор ловит по имени класса
    pass


class AuthenticationError(Exception):
    pass


def test_transient_errors_are_retried(env, monkeypatch):
    tmp, calls, _ = env
    sleeps = []
    monkeypatch.setattr(llm.time, "sleep", sleeps.append)
    seq = [ServiceUnavailableError("overloaded"), ServiceUnavailableError("overloaded"), "ok"]

    def flaky(model, messages, max_tokens, params):
        x = seq.pop(0)
        if isinstance(x, Exception):
            raise x
        return x, 1, 1, None
    monkeypatch.setattr(llm, "_call", flaky)
    assert llm.complete_text("core/t", {"x": 1, "y": 2}) == "ok"
    assert len(sleeps) == 2 and sleeps[1] > sleeps[0]          # пауза растёт


def test_permanent_errors_fail_at_once(env, monkeypatch):
    monkeypatch.setattr(llm.time, "sleep", lambda s: pytest.fail("не должно ждать"))

    def bad(*a):
        raise AuthenticationError("bad key")
    monkeypatch.setattr(llm, "_call", bad)
    with pytest.raises(AuthenticationError):
        llm.complete_text("core/t", {"x": 1, "y": 2})


def test_transient_gives_up(env, monkeypatch):
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)

    def down(*a):
        raise ServiceUnavailableError("overloaded")
    monkeypatch.setattr(llm, "_call", down)
    with pytest.raises(ServiceUnavailableError):
        llm.complete_text("core/t", {"x": 1, "y": 2})
