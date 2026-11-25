"""ffmpeg/ffprobe: декодирование озвучки, нормализация −16 LUFS, сборка H.264 MP4, замеры."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

TARGET_I, TARGET_TP, TARGET_LRA = -16.0, -1.5, 11.0


class ToolError(RuntimeError):
    pass


def require(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise ToolError(f"{name} не найден в PATH. Установите FFmpeg (Windows: winget install Gyan.FFmpeg) "
                        f"и откройте новый терминал.")
    return path


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        err = r.stderr.decode("utf-8", "replace")[-3000:]
        raise ToolError(f"{Path(cmd[0]).name} завершился с кодом {r.returncode}: {' '.join(cmd[1:6])} …\n{err}")
    return r


def version(name: str) -> str:
    return _run([require(name), "-version"]).stdout.decode("utf-8", "replace").splitlines()[0]


def decode_pcm(src: Path, sample_rate: int) -> bytes:
    """Аудиофайл → моно PCM s16le с заданной частотой."""
    r = _run([require("ffmpeg"), "-hide_banner", "-v", "error", "-i", str(src),
              "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", str(sample_rate), "-"])
    if not r.stdout:
        raise ToolError(f"ffmpeg не извлёк звук из {src}")
    return r.stdout


def _loudnorm(**measured: str) -> str:
    f = f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
    if measured:
        f += (f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
              f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
              f":offset={measured['target_offset']}:linear=true")
    return f


def loudnorm_measure(wav: Path) -> dict:
    """Первый проход loudnorm: замер громкости исходной дорожки."""
    r = _run([require("ffmpeg"), "-hide_banner", "-nostats", "-i", str(wav),
              "-af", _loudnorm() + ":print_format=json", "-f", "null", "-"])
    txt = r.stderr.decode("utf-8", "replace")
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", txt, re.S)
    if not m:
        raise ToolError(f"loudnorm не выдал замер громкости:\n{txt[-1500:]}")
    return json.loads(m.group())


def mux(video: Path, wav: Path, out: Path, total_s: float, fps: int, measured: dict, draft: bool) -> None:
    """Видео сцены + дорожка → H.264/AAC MP4 длиной ровно total_s.

    Видео дотягивается последним кадром (tpad), звук нормализуется вторым проходом
    loudnorm (linear) к −16 LUFS; итог режется по длине дорожки, а не по видео,
    поэтому последняя фраза и хвост тишины сохраняются целиком.
    """
    vf = f"tpad=stop_mode=clone:stop_duration={total_s + 1:.3f},fps={fps},format=yuv420p"
    af = _loudnorm(**measured) + ",aresample=48000"
    _run([require("ffmpeg"), "-y", "-hide_banner", "-v", "error",
          "-i", str(video), "-i", str(wav),
          "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]", "-map", "[v]", "-map", "[a]",
          "-c:v", "libx264", "-preset", "veryfast" if draft else "medium", "-crf", "28" if draft else "18",
          "-profile:v", "high", "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
          "-t", f"{total_s:.6f}", "-movflags", "+faststart", str(out)])


def probe(path: Path) -> dict:
    r = _run([require("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-count_frames",
              "-of", "json", str(path)])
    return json.loads(r.stdout.decode("utf-8"))


def loudness(path: Path) -> dict:
    """Итоговая громкость дорожки по EBU R128: интегральная (LUFS) и истинный пик (dBTP)."""
    r = _run([require("ffmpeg"), "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a:0",
              "-af", "ebur128=peak=true", "-f", "null", "-"])
    txt = r.stderr.decode("utf-8", "replace")
    summary = txt[txt.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summary)
    tp = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
    if not (i and tp):
        raise ToolError(f"ebur128 не выдал итог громкости:\n{summary[-800:]}")
    return {"integrated_lufs": float(i.group(1)), "true_peak_dbtp": float(tp.group(1))}


def trailing_silence(path: Path, total_s: float, noise_db: int = -50) -> float:
    """Сколько секунд тишины в конце дорожки (0 — звук идёт до самого конца)."""
    r = _run([require("ffmpeg"), "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a:0",
              "-af", f"silencedetect=noise={noise_db}dB:d=0.1", "-f", "null", "-"])
    txt = r.stderr.decode("utf-8", "replace")
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", txt)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", txt)]
    if not starts:
        return 0.0
    if len(ends) < len(starts) or ends[-1] >= total_s - 0.05:
        return max(0.0, total_s - starts[-1])
    return 0.0


def extract_frame(video: Path, t: float, out_png: Path) -> None:
    """Один кадр ролика в момент t (с) — для визуального ревью."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    _run([require("ffmpeg"), "-y", "-hide_banner", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
          "-frames:v", "1", str(out_png)])
