"""Единственная точка вызова LLM (CLAUDE.md §2). Интерфейс фиксирован:

    from pipeline.llm import complete_json, complete_text
    obj = complete_json(prompt="course/step_page", vars={...}, schema=SomeModel,
                        tier="default" | "strong" | "vision", images=[path, ...] | None)
    txt = complete_text(prompt="video/script_draft", vars={...}, tier="default")

- prompt — путь в prompts/ без .md; переменные в файле — {{name}} (имя с буквы: {{1}} не трогается).
  Не хватает переменной или передана лишняя — KeyError.
- Модель — config/llm.yaml по tier; переопределение: LLM_MODEL_<TIER> > LLM_MODEL (.env или окружение).
- Запасные модели (необязательно): LLM_MODEL_FALLBACK_<TIER> > LLM_MODEL_FALLBACK, через запятую.
  Лимит в минуту / перегрузка / таймаут — пауза (сколько просит провайдер) и повтор; дневной лимит или
  повторы кончились — следующая модель списка; кончились все — ProviderUnavailable. Кэш — по основной модели.
- Кэш cache/llm/<sha256>.json по (модель + итоговый текст промпта + картинки). LLM_OFFLINE=1: промах — OfflineCacheMiss.
- Каждый вызов (и попадание в кэш) — строка в out/_metrics/llm_calls.jsonl; глава — из переменной CH.
- complete_json: ответ проверяется pydantic-схемой; при ошибке до json_retries повторов с текстом ошибки, потом LLMJSONError.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from pipeline.common import config, paths

def _load_env(path: Path) -> None:
    """.env в UTF-8 или UTF-16 (так его пишет `>` в Windows PowerShell 5.1)."""
    if not path.exists():
        return
    raw = path.read_bytes()
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"
    load_dotenv(stream=io.StringIO(raw.decode(enc)), override=False)


_load_env(paths.ROOT / ".env")

M = TypeVar("M", bound=BaseModel)
VAR_RE = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}


class OfflineCacheMiss(RuntimeError):
    pass


class LLMJSONError(RuntimeError):
    pass


class ProviderUnavailable(RuntimeError):
    pass


# ---------------------------------------------------------------- промпты

def _fmt(v: Any) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, BaseModel):
        return v.model_dump_json(by_alias=True, indent=1)
    return json.dumps(v, ensure_ascii=False, indent=1, default=str)


def render(prompt: str, vars: dict[str, Any]) -> str:
    path = paths.PROMPTS / f"{prompt}.md"
    if not path.exists():
        raise FileNotFoundError(f"нет файла промпта {path}")
    text = path.read_text(encoding="utf-8")
    names = set(VAR_RE.findall(text))
    missing, extra = names - set(vars), set(vars) - names
    if missing or extra:
        raise KeyError(f"промпт {prompt}: не хватает переменных {sorted(missing)}, лишние {sorted(extra)}")
    return VAR_RE.sub(lambda m: _fmt(vars[m.group(1)]), text)


# ---------------------------------------------------------------- модель и провайдер

def resolve_model(tier: str) -> tuple[str, dict]:
    tiers = config.llm()["tiers"]
    if tier not in tiers:
        raise ValueError(f"неизвестный tier '{tier}', есть: {', '.join(tiers)}")
    t = tiers[tier]
    model = os.environ.get(f"LLM_MODEL_{tier.upper()}") or os.environ.get("LLM_MODEL") or t["model"]
    return model, t


def _price(model: str, tokens_in: int, tokens_out: int, litellm_cost: Optional[float]) -> Optional[float]:
    p = (config.llm().get("prices") or {}).get(model)
    if p:
        return round((tokens_in * p["input"] + tokens_out * p["output"]) / 1e6, 6)
    if litellm_cost is None:
        print(f"[llm] ВНИМАНИЕ: нет цены для {model} — добавь в config/llm.yaml prices; money_usd=null",
              file=sys.stderr)
    return litellm_cost


def _call(model: str, messages: list[dict], max_tokens: int, params: dict) -> tuple[str, int, int, Optional[float]]:
    """Один запрос к провайдеру через litellm. Возвращает (текст, токены входа, токены выхода, цена litellm или None)."""
    # .env уже прочитан нами (_load_env); litellm в режиме DEV читает его сам и падает на UTF-16.
    os.environ.setdefault("LITELLM_MODE", "PRODUCTION")
    os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")   # без похода в сеть за картой цен
    import litellm  # тяжёлый импорт — только при реальном вызове

    extra = {}
    if os.environ.get("LLM_API_KEY"):        # общий ключ; иначе litellm берёт ANTHROPIC_API_KEY / OPENAI_API_KEY / …
        key = os.environ["LLM_API_KEY"].strip()
        if not key.isascii():
            raise RuntimeError("LLM_API_KEY содержит не-ASCII символы — похоже, в .env заглушка вместо ключа")
        extra["api_key"] = key
    if os.environ.get("LLM_API_BASE"):       # свой адрес API (прокси, совместимый сервер)
        extra["api_base"] = os.environ["LLM_API_BASE"]
    resp = litellm.completion(model=model, messages=messages, max_tokens=max_tokens,
                              timeout=config.llm().get("timeout_s", 600), **extra, **params)
    choice = resp.choices[0]
    if choice.finish_reason not in (None, "stop", "end_turn"):
        raise RuntimeError(f"[llm] {model}: ответ оборван, finish_reason={choice.finish_reason} "
                           f"(увеличь max_tokens в config/llm.yaml или раздели запрос)")
    text = choice.message.content
    if not text:
        raise RuntimeError(f"[llm] {model}: пустой ответ")
    try:
        cost = litellm.completion_cost(completion_response=resp)
    except Exception:  # модель неизвестна litellm — цену берём из конфига
        cost = None
    usage = resp.usage
    return text, usage.prompt_tokens, usage.completion_tokens, cost


# Перегрузка и лимиты провайдера — временные (имена классов исключений litellm).
TRANSIENT = {"RateLimitError", "ServiceUnavailableError", "InternalServerError", "BadGatewayError",
             "Timeout", "APITimeoutError", "APIConnectionError"}
RETRY_DELAY_RE = re.compile(r'retryDelay\W*(\d+(?:\.\d+)?)s')


def fallbacks(tier: str) -> list[str]:
    raw = os.environ.get(f"LLM_MODEL_FALLBACK_{tier.upper()}") or os.environ.get("LLM_MODEL_FALLBACK") or ""
    return [m.strip() for m in raw.split(",") if m.strip()]


def _call_chain(models: list[str], messages: list[dict], max_tokens: int, params: dict):
    """Первая модель, которая ответила: (модель, текст, токены входа, выхода, цена litellm)."""
    cfg = config.llm()
    retries, base = cfg.get("transient_retries", 4), cfg.get("transient_backoff_s", 5)
    why = []
    for model in models:
        for attempt in range(retries + 1):
            try:
                return (model, *_call(model, messages, max_tokens, params))
            except Exception as e:
                name, msg = type(e).__name__, str(e)
                if name not in TRANSIENT:
                    raise
                if "PerDay" in msg or "per day" in msg.lower():
                    why.append(f"{model}: дневной лимит исчерпан")
                    print(f"[llm] {model}: дневной лимит исчерпан", file=sys.stderr)
                    break
                if attempt == retries:
                    why.append(f"{model}: {name} после {retries} повторов")
                    break
                m = RETRY_DELAY_RE.search(msg)
                wait = min(float(m.group(1)) + 1 if m else base * 2 ** attempt, 300)
                print(f"[llm] {model}: {name} — повтор {attempt + 1}/{retries} через {wait:.0f} с", file=sys.stderr)
                time.sleep(wait)
        if model != models[-1]:
            print(f"[llm] переход на запасную модель {models[models.index(model) + 1]}", file=sys.stderr)
    raise ProviderUnavailable("ни одна модель не ответила: " + "; ".join(why) +
                              ". Подожди, добавь LLM_MODEL_FALLBACK или смени LLM_MODEL (docs/run.md)")


# ---------------------------------------------------------------- кэш и лог

def _image_part(path: Path) -> tuple[dict, str]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"нет картинки {path}")
    data = path.read_bytes()
    mime = MIME.get(path.suffix.lower())
    if not mime:
        raise ValueError(f"неподдерживаемый формат картинки {path.suffix}: нужен {', '.join(MIME)}")
    url = f"data:{mime};base64,{base64.b64encode(data).decode()}"
    return {"type": "image_url", "image_url": {"url": url}}, hashlib.sha256(data).hexdigest()


def _cache_path(key: str) -> Path:
    return paths.cache_root() / "llm" / f"{key}.json"


def _log(row: dict) -> None:
    d = paths.metrics_dir()
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "llm_calls.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- ядро

def _run(prompt: str, vars: dict, tier: str, images: Optional[Sequence[Path]],
         schema: Optional[type[BaseModel]]) -> str:
    model, t = resolve_model(tier)
    text = render(prompt, vars)
    if schema is not None:
        text += render("core/_json_suffix", {"schema": json.dumps(schema.model_json_schema(), ensure_ascii=False)})

    parts, img_hashes = [], []
    for p in images or []:
        part, h = _image_part(p)
        parts.append(part)
        img_hashes.append(h)
    content: Any = [{"type": "text", "text": text}, *parts] if parts else text
    messages = [{"role": "user", "content": content}]

    key = hashlib.sha256(json.dumps({"model": model, "text": text, "images": img_hashes},
                                    ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    row = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "chapter": os.environ.get("CH"),
           "prompt": prompt, "tier": tier, "model": model, "key": key}

    cp = _cache_path(key)
    if cp.exists():
        cached = json.loads(cp.read_text(encoding="utf-8"))
        _log({**row, "model": cached.get("model", model), "model_requested": model, "cache_hit": True, "tokens_in": cached["tokens_in"], "tokens_out": cached["tokens_out"],
              "money_usd": cached["money_usd"], "attempts": cached["attempts"], "seconds": 0})
        return cached["text"]
    if os.environ.get("LLM_OFFLINE") == "1":
        raise OfflineCacheMiss(f"LLM_OFFLINE=1, а в кэше нет ответа: промпт {prompt}, модель {model}, ключ {key}. "
                               f"Нужен прогон с ключом API (см. docs/run.md)")

    t0 = time.monotonic()
    tin = tout = 0
    money: Optional[float] = 0.0
    attempts = 0
    used = model
    chain = [model, *[m for m in fallbacks(tier) if m != model]]
    retries = config.llm().get("json_retries", 2) if schema is not None else 0
    last_err = ""
    while attempts <= retries:
        attempts += 1
        used, reply, i, o, c = _call_chain(chain, messages, t["max_tokens"], t.get("params") or {})
        tin, tout = tin + i, tout + o
        price = _price(used, i, o, c)
        money = None if (money is None or price is None) else money + price
        if schema is None:
            break
        try:
            reply = schema.model_validate(_extract_json(reply)).model_dump_json(by_alias=True)
            break
        except (ValueError, ValidationError) as e:
            last_err = str(e)[:4000]
            messages = messages + [{"role": "assistant", "content": reply},
                                   {"role": "user", "content": render("core/_json_retry", {"error": last_err})}]
    else:
        _log({**row, "model": used, "model_requested": model, "cache_hit": False, "tokens_in": tin,
              "tokens_out": tout, "money_usd": money, "attempts": attempts,
              "seconds": round(time.monotonic() - t0, 1), "error": last_err[:500]})
        raise LLMJSONError(f"промпт {prompt}: невалидный JSON после {attempts} попыток: {last_err[:1000]}")

    entry = {"text": reply, "model": used, "model_requested": model, "prompt": prompt, "tokens_in": tin, "tokens_out": tout,
             "money_usd": money, "attempts": attempts}
    cp.parent.mkdir(parents=True, exist_ok=True)
    tmp = cp.with_suffix(".tmp")
    tmp.write_text(json.dumps(entry, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(cp)
    _log({**row, "model": used, "model_requested": model, "cache_hit": False, "tokens_in": tin,
          "tokens_out": tout, "money_usd": money, "attempts": attempts, "seconds": round(time.monotonic() - t0, 1)})
    return reply


def _extract_json(reply: str) -> Any:
    s = reply.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, re.S)
    if m:
        s = m.group(1).strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        start = min((i for i in (s.find("{"), s.find("[")) if i >= 0), default=-1)
        if start < 0:
            raise ValueError("в ответе нет JSON")
        obj, _ = json.JSONDecoder().raw_decode(s[start:])
        return obj


def complete_text(prompt: str, vars: dict[str, Any], tier: str = "default",
                  images: Optional[Sequence[Path]] = None) -> str:
    return _run(prompt, vars, tier, images, None)


def complete_json(prompt: str, vars: dict[str, Any], schema: type[M], tier: str = "default",
                  images: Optional[Sequence[Path]] = None) -> M:
    return schema.model_validate_json(_run(prompt, vars, tier, images, schema))
