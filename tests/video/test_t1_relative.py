import json
from pathlib import Path

from contracts.models import SceneSpec, Script
from pipeline.video import t1_template


def test_relative_pressure_has_no_invented_mpa_scale():
    root = Path(__file__).resolve().parents[2]
    spec = SceneSpec.model_validate_json((root / 'fixtures/video/t1_demo/scene_spec.json').read_text(encoding='utf-8'))
    script = Script.model_validate_json((root / 'fixtures/video/t1_demo/script.json').read_text(encoding='utf-8'))
    spec.params['pressure_mode'] = 'relative'
    del spec.params['pressure_scale_mpa']
    spec.params['threshold_mpa'] = 0.2
    prep = t1_template.prepare(spec, script, t1_template.load_config(root / 'domain/geology/templates'))
    assert prep['pressure_unit'] == 'отн. ед.'
    assert prep['model'].scale_mpa == 1


def test_relative_pressure_rejects_dimensional_amplitude():
    import pytest
    from pipeline.video.inputs import VideoInputError
    root = Path(__file__).resolve().parents[2]
    spec = SceneSpec.model_validate_json((root / 'fixtures/video/t1_demo/scene_spec.json').read_text(encoding='utf-8'))
    script = Script.model_validate_json((root / 'fixtures/video/t1_demo/script.json').read_text(encoding='utf-8'))
    spec.params['pressure_mode'] = 'relative'
    with pytest.raises(VideoInputError, match='pressure_scale_mpa'):
        t1_template.prepare(spec, script, t1_template.load_config(root / 'domain/geology/templates'))
