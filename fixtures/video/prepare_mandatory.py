"""Recreate manually prepared video Layer fragments; no LLM API is claimed.

Book quotes are copied verbatim from PDF-page marked source markdown. This is
P4 input preparation, not a replacement for the team's full P1 teaching layers.
"""
from pathlib import Path
import json

from contracts.models import Layer, Routing, Script, SceneSpec
from pipeline.ingest.parse import split_pages
from pipeline.video.inputs import check_pair
from pipeline.video.spec_check import check_script, check_scene, param_source_problems, sources_table
from pipeline.video.templates import load_template_config

ROOT = Path(__file__).resolve().parents[2]


def write(path, model):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(model.model_dump_json(by_alias=True, indent=2) + '\n', encoding='utf-8')


def make(ch, slug, title, book, template, definitions, phrases):
    pages = dict(split_pages((ROOT / book).read_text(encoding='utf-8')))
    nid = ch + '.' + slug
    claims = []
    for i, (page, needle, meaning, kind) in enumerate(definitions, 1):
        line = next(x.strip() for x in pages[page].splitlines() if needle in x)
        assert line in pages[page]
        claims.append(dict(id=f'{nid}#c{i}', text=meaning, kind='inference', page_pdf=page,
                           quote=line, source_kind=kind, by_model=True,
                           ext={'video': {'quote_verified_exact': True}}))
    field = lambda x: dict(text=x, by_model=True)
    node = dict(id=nid, order=1, title=title, why_here=field(title),
                difficulty=dict(primary='Ф' if template == 'T1' else 'И'), threshold=True,
                layers={k: field(v) for k, v in dict(topic=title, main=claims[0]['text'],
                    mechanism=claims[1]['text'], practice=claims[-1]['text'],
                    nuances='Численные настройки показа не являются измерениями пласта; пределы вывода оговариваются.').items()},
                claims=claims, links=[], data_meaning=dict(from_chapter=field(claims[0]['text']),
                    breaks=field('Нельзя переносить вывод за пределы допущений модели или условий интерпретации.')),
                it_analogy=dict(text='Автоматизация сопоставляет синхронные значения и проверяет условия.',
                    breaks_where='Алгоритм не заменяет физическую модель и проверку специалистом.', by_model=True),
                terms_introduced=['пьезопроводность', 'давление', 'скважина'] if template == 'T1' else ['сопротивление', 'пористость', 'каротаж'], pages=sorted(set(c['page_pdf'] for c in claims)),
                ext={'video': {'preparation': 'manual_layer_fragment', 'mentor_approved': False}})
    layer = Layer(chapter=ch, source=book, nodes=[node], generated_by='Codex: вручную подготовленный фрагмент слоя для P4; API не использовался',
                  ext={'video': {'manual_preparation': True, 'full_chapter_layer': False, 'mentor_approved': False}})
    fmt = 'short' if template == 'T1' else 'long'
    script = Script(video_id=nid + '.' + fmt, node_id=nid, format=fmt,
        phrases=[dict(id=f'p{i}', beat=beat, text=text, on_screen=screen, claim_id=f'{nid}#c{claim}',
                      pause_after_s=1.2 if beat == 'prediction' else 0, is_analogy=False)
                 for i, (beat,text,screen,claim) in enumerate(phrases,1)],
        prediction_question=next(p[1] for p in phrases if p[0]=='prediction'),
        transfer_question=next(p[1] for p in phrases if p[0]=='transfer'),
        data_it_bridge='Одно состояние управляет изображением и данными; наблюдение отделено от решения.',
        ext={'video': {'manual_preparation': True, 'mentor_approved': False}})
    demo = 't1_demo' if template == 'T1' else 't2_volve'
    specdata = json.loads((ROOT / 'fixtures/video' / demo / 'scene_spec.json').read_text(encoding='utf-8'))
    specdata.update(video_id=script.video_id,node_id=nid)
    if template == 'T1':
        specdata['params'].update(kappa_m2_s=1.0, pressure_mode='relative', threshold_mpa=0.2, r_max_m=450)
        del specdata['params']['pressure_scale_mpa']
        specdata['convention']='Падение давления, делённое на амплитуду A: относительные единицы, не МПа. Расстояние — метры.'
        specdata['assumptions']=['Бесконечный однородный пласт; постоянный дебит; слабосжимаемая жидкость.',
            'Пьезопроводность и радиус — пример Басниева, PDF стр. 492. Амплитуда не задана: показывается относительное падение.',
            'Окно, время и порог условной границы — настройки расчётной иллюстрации, не измерения месторождения.']
        specdata['data_sources']=[book + ', PDF стр. 488–492, формула 23.52']
        param_sources={'kappa_m2_s':dict(claim_ids=[f'{nid}#c4'],numbers=['1'],factor=1),
                       'r_well_m':dict(claim_ids=[f'{nid}#c4'],numbers=['0,1'],factor=1)}
    else:
        # Diameter is a property of the supplied LAS, not a number invented by the book model.
        param_sources={}
        specdata['assumptions'] += ['Методика сопоставления — Латышова, PDF стр. 97; пороги — условный фильтр, не оценка насыщения.',
            'Кривые Volve — дополнительный открытый пример; не данные из учебника. Насыщение и запасы здесь не вычисляются.']
    ts = len(phrases)-1
    plaque = 'не в масштабе: скважина крупнее в 100 раз' if template=='T1' else 'не в масштабе: ствол шире в 20 раз'
    specdata['shots']=[dict(id=f's{i}',phrase_ids=[f'p{i}'],frame_class='B' if template=='T1' else 'A',
        label='симуляция' if template=='T1' else 'реальные данные', shows=screen,
        plaque=None if i==ts else plaque) for i,(_,_,screen,_) in enumerate(phrases,1)]
    specdata['true_scale_shot_id']=f's{ts}'
    specdata['params']['evolve_shot_ids']=[f's{i}' for i,p in enumerate(phrases,1)
        if i<ts and p[0] not in ('hook','prediction','decision')]
    specdata['ext']={'video':dict(manual_preparation=True, mentor_approved=False,
        note='Учебная иллюстрация по фрагменту слоя. Ручная подготовка входов без API; ментор не проверял.',
        param_sources=param_sources)}
    spec=SceneSpec.model_validate(specdata)
    spec.ext['video']['sources']=sources_table(script, layer.nodes[0])
    errors=check_script(script,layer.nodes[0],fmt)+check_scene(spec,script,real_data_ok=template=='T2')
    cfg=load_template_config(ROOT/'domain/geology/templates',template)
    errors+=param_source_problems(spec,layer.nodes[0],cfg)
    check_pair(script,spec)
    assert not errors, errors
    folder=ROOT/'fixtures/video'/('mandatory_basniev' if template=='T1' else 'mandatory_latyshova')
    route = Routing(chapter=ch, routes=[dict(node_id=nid, format='шортс' if fmt=='short' else 'длинное видео',
        template=template, video_scores=dict(time=2, invisible=2, scale=2, counterintuitive=1, cause_effect=2),
        why='Ручной выбор обязательного ролика P4 по ТЗ; не результат API-маршрутизации.')],
        ext={'video': {'manual_preparation': True}})
    for file,obj in [('layer.json',layer),('routing.json',route),('script.json',script),('scene_spec.json',spec)]:write(folder/file,obj)
    print(folder.name, script.video_id, 'phrases',len(phrases),'sources',len(claims),flush=True)


if __name__ == '__main__':
    make('basniev_gl23-24','pressure_diffusion','Как распространяется падение давления',
        'data/books/train_basniev.md','T1',[
        (488,'Пусть в неограниченном','После пуска скважины с постоянным дебитом возникает неустановившийся радиальный поток.','text'),
        (481,'В.Н.Щелкачев назвал','Перераспределение давления описывает пьезопроводность.','text'),
        (491,'(23.52)','При постоянных параметрах одинаковому относительному падению соответствует радиус, пропорциональный корню из времени.','formula'),
        (492,'Оценим практическое','В примере книги пьезопроводность 1 м²/с, радиус скважины 0,1 м.','text'),
        (489,'(23.43)','Автомодельная координата пропорциональна расстоянию, делённому на корень из произведения пьезопроводности и времени.','formula'),
        (492,'Строго говоря','Решение для точечного стока и неограниченного пласта имеет пределы применимости.','text')],[
        ('hook','Скважину пустили. Давление меняется везде сразу?','Когда пласт почувствует скважину?',1),
        ('problem','После пуска перераспределяется давление. Но это не резкий фронт, движущийся с постоянной скоростью.','Давление перераспределяется постепенно',3),
        ('solution','Посмотрим на карту пласта и профиль вдоль линии: они рассчитаны для одного момента.','Карта и профиль синхронны',3),
        ('naming','Этот процесс описывает пьезопроводность. В основе расчёта — решение из книги Басниева.','Пьезопроводность пласта',2),
        ('solution','Радиус скважины и пьезопроводность взяты из примера книги. Падение показано в относительных единицах.','Относительное падение, не измерение',4),
        ('prediction','Как думаете, пунктирная граница будет удаляться от скважины с постоянной скоростью?','Граница движется равномерно?',5),
        ('data','Нет. При выбранном постоянном пороге её радиус растёт как корень из времени.','Радиус растёт всё медленнее',3),
        ('decision','Пунктир — условный порог падения, не край возмущения. Специалист учитывает время после пуска.','Сигнал: падение. Вывод: влияние меняется',3),
        ('final','Теперь истинный масштаб: скважина меньше точки. Модель предполагает однородный пласт без внешней границы.','Истинный масштаб. Учитывайте допущения',6),
        ('transfer','Как при том же времени изменится зона влияния, если пьезопроводность пласта станет больше?','А если пьезопроводность больше?',5)])
    make('latyshova_gl5_par17-20','resistivity_porosity','Почему одного сопротивления недостаточно',
        'data/books/train_latyshova.md','T2',[
        (90,'Данные геофизических исследований поисковых','Комплекс ГИС используют для выделения коллекторов и оценки их свойств.','text'),
        (97,'Определение характера насыщения коллектора.','Для оценки насыщения нужны сопротивление неизменённой части пласта, пористость и свойства пластовой воды.','text'),
        (97,'В межзерновых коллекторах при больших','При изменчивой пористости диапазоны сопротивлений могут перекрываться; сравнивают методы сопротивления и пористости.','text'),
        (96,'Отсутствие заметного градиента','Отсутствие заметного градиента сопротивления не исключает коллектор.','text'),
        (90,'Состав методов оптимального комплекса','Условия бурения и промывочная жидкость влияют на качество данных и выбор комплекса.','text'),
        (97,'Чистые, высокопористые','Упрощённая оценка по сопротивлению допустима при дополнительных условиях, включая близкую пористость и одинаковую воду.','text')],[
        ('hook','Высокое сопротивление. Значит, нашли нефть?','Высокое сопротивление — это нефть?',3),
        ('problem','По одной кривой легко сделать поспешный вывод. Латышова предлагает рассматривать данные в комплексе.','Одна кривая может обмануть',2),
        ('solution','Сопоставим сопротивление с пористостью на одной глубине. Затем отделим наблюдение от решения специалиста.','Сначала сопоставить, потом решать',2),
        ('naming','Это комплексная интерпретация каротажа: показания приборов помогают оценивать свойства коллектора, но требуют проверки условий.','Комплексная интерпретация каротажа',1),
        ('data','Перед нами открытые данные месторождения Волве. Это дополнительный пример, а не диаграммы из учебника.','Реальные данные Volve',1),
        ('data','Прибор на схеме движется вниз. На той же глубине раскрываются соответствующие участки кривых.','Прибор и кривые на одной глубине',1),
        ('data','Слева гамма-каротаж, рядом сопротивление и нейтронная пористость. Схема прибора показывает назначение измерений.','Сопоставляем разные измерения',1),
        ('problem','Важно: нейтронная кривая сама по себе ещё не даёт окончательного заключения о насыщении.','Показание ещё не заключение',2),
        ('solution','В книге сопротивление неизменённой части пласта сопоставляют с оценкой того же пласта в водонасыщенном состоянии.','Нужна водонасыщенная опора',2),
        ('solution','Для такой оценки нужны сведения о пористости и пластовой воде. Эти условия нельзя пропускать.','Пористость и свойства воды важны',2),
        ('prediction','Отметит ли показанный фильтр каждый участок высокого сопротивления, если остальные признаки не совпадут?','Одного высокого сопротивления хватит?',3),
        ('data','Нет. В этой демонстрации отметка появляется только там, где выполнены все условия показанного правила.','Отметка только при совместных условиях',3),
        ('data','Пороги здесь условные, выбраны для объяснения работы фильтра. Это не нормативы Латышовой и не диагноз.','Пороги условные, не из учебника',3),
        ('data','Посмотрите: высокое сопротивление встречается и без отметки. Значит, остальные условия этого фильтра не выполнены.','Контрпример: высокий сигнал без отметки',3),
        ('decision','Отмеченный интервал — кандидат для дальнейшей проверки. Мы не называем его доказанной нефтенасыщенной толщей.','Сигнал → кандидат для проверки',2),
        ('decision','По Латышовой, изменчивая пористость может приводить к перекрытию диапазонов сопротивлений. Поэтому одного сигнала недостаточно.','Разные свойства дают похожий сигнал',3),
        ('decision','Отсутствие градиента сопротивления тоже не исключает коллектор. Отрицательный признак требует аккуратного толкования.','Нет градиента — не значит нет коллектора',4),
        ('decision','Проверим условия бурения и свойства промывочной жидкости: они влияют на информацию, которую регистрируют приборы.','Условия измерения влияют на вывод',5),
        ('decision','Простая оценка по сопротивлению возможна лишь при дополнительных условиях. Нельзя переносить её на любой разрез.','Проверьте условия применимости',6),
        ('final','Запомним порядок: совмещаем глубину, сравниваем признаки, проверяем условия, затем формулируем ограниченный вывод.','Глубина → признаки → проверка → вывод',2),
        ('final','Ствол теперь в истинном масштабе. Размеры прибора на поясняющей схеме условные; кривые остаются данными.','Истинный масштаб ствола',1),
        ('transfer','Каких данных о пластовой воде и пористости не хватает, чтобы перейти от кандидата к оценке насыщения?','Что нужно проверить перед оценкой насыщения?',2)])
