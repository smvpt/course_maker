import sys
from pathlib import Path

# корень репо в sys.path, чтобы pytest работал и без python -m
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _blind_check_off_unless_asked(request, monkeypatch):
    """Слепая проверка ответов — отдельный вызов модели. Тесты генерации заданий её не вызывают (мок «все согласны»);
    тесты самой проверки помечены @pytest.mark.blind и работают с настоящей функцией."""
    if request.node.get_closest_marker("blind"):
        return
    from pipeline.course import tasks
    monkeypatch.setattr(tasks, "blind_check", lambda node, built: {}, raising=False)


def pytest_configure(config):
    config.addinivalue_line("markers", "blind: тест слепой проверки ответа, без подмены blind_check")


@pytest.fixture(autouse=True)
def _one_worker_by_default(monkeypatch):
    """Тесты с моками, считающими вызовы по порядку, идут в одном потоке; параллельные тесты ставят COURSE_WORKERS сами."""
    monkeypatch.setenv("COURSE_WORKERS", "1")
