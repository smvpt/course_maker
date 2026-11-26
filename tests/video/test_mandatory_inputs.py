import json
from pathlib import Path

import jsonschema
import pytest

from contracts.models import Layer, Script, SceneSpec
from pipeline.ingest.parse import split_pages
from pipeline.video.spec import pair_problems, load_route

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize('name', ['mandatory_basniev', 'mandatory_latyshova'])
def test_book_video_inputs_have_verbatim_sources_and_pass_production_checks(name):
    folder = ROOT / 'fixtures/video' / name
    layer = Layer.model_validate_json((folder / 'layer.json').read_text(encoding='utf-8'))
    script = Script.model_validate_json((folder / 'script.json').read_text(encoding='utf-8'))
    scene = SceneSpec.model_validate_json((folder / 'scene_spec.json').read_text(encoding='utf-8'))
    pages = dict(split_pages((ROOT / layer.source).read_text(encoding='utf-8')))
    node = layer.nodes[0]
    assert node.terms_introduced
    assert layer.ext['video']['manual_preparation'] is True
    assert layer.ext['video']['full_chapter_layer'] is False
    assert all(c.quote in pages[c.page_pdf] for c in node.claims)
    schema = json.loads((ROOT / 'data/organizers/01_схемы/node.schema.json').read_text(encoding='utf-8'))
    jsonschema.validate(json.loads(layer.model_dump_json(by_alias=True)), schema)
    assert pair_problems(script, scene, node, script.format, ROOT / 'domain/geology/templates') == []
    loaded, route, fmt = load_route(layer.chapter, node.id, folder/'layer.json', folder/'routing.json', ROOT/'out')
    assert loaded.id == node.id and route.template == scene.template and fmt == script.format
