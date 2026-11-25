/* Курс открывается из файла: без сети, без fetch, данные — во встроенных <script type="application/json">.

   Хранилище (localStorage, ключи с префиксом course:<глава>:):
     done        [id шага, ...]                  шаг пройден (чек-лист выполнен)
     last        id шага                         последний открытый шаг
     checks      {id шага: {read, video}}        ручные пункты чек-листа
     cards       {id шага: "know" | "repeat"}    карточки
     tasks       {id задания: "ok" | "bad"}      результат последней проверки
     answers     {id задания: ответ ученика}     single: id варианта; multiple и order: список id; gap: список слов;
                                                 calc: число. После перезагрузки показываем выбор ученика
     guess       {id шага: "true"|"false"|"skip"}  ответ на вопрос «сначала угадай»
     understood  [id задания, ...]               «Я понял» в списке ошибок; логика заданий убирает id,
                                                 если то же задание снова решено неверно
   Тема и подсветка «автор / модель» — общие для всех глав: course:theme, course:by. */
(function () {
  "use strict";

  var meta = JSON.parse(document.getElementById("course-meta").textContent);
  var ch = meta.ch;
  var page = document.body.dataset.page;

  /* localStorage на file:// может быть запрещён (приватный режим, политика браузера): курс работает и без него */
  var store = {
    get: function (k, dflt) {
      try { var v = localStorage.getItem(k); return v === null ? dflt : JSON.parse(v); } catch (e) { return dflt; }
    },
    set: function (k, v) {
      try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* без сохранения прогресса */ }
    }
  };
  var K = {};
  ["done", "last", "checks", "cards", "tasks", "answers", "understood", "guess"].forEach(function (n) { K[n] = "course:" + ch + ":" + n; });
  K.theme = "course:theme";
  K.by = "course:by";

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function readJSON(id) {
    var s = document.getElementById(id);
    return s ? JSON.parse(s.textContent) : null;
  }
  function claimAnchor(claimId) { return claimId.replace("#", "--"); }

  /* ---------- состояние ---------- */
  var stepById = {};
  meta.steps.forEach(function (s) { stepById[s.id] = s; });
  var tasksOf = {};
  meta.tasks.forEach(function (t) { (tasksOf[t.step_id] = tasksOf[t.step_id] || []).push(t); });

  var done = store.get(K.done, []);
  var taskRes = store.get(K.tasks, {});
  var answers = store.get(K.answers, {});
  var understood = store.get(K.understood, []);
  var cardMarks = store.get(K.cards, {});

  function isDone(id) { return done.indexOf(id) >= 0; }
  function setDone(id, on) {
    done = done.filter(function (x) { return x !== id; });
    if (on) done.push(id);
    store.set(K.done, done);
  }
  function taskState(id) { return taskRes[id] === "ok" || taskRes[id] === "bad" ? taskRes[id] : "none"; }
  function stepStats(stepId) {
    var list = tasksOf[stepId] || [];
    var st = { total: list.length, ok: 0, bad: 0, openBad: 0 };
    list.forEach(function (t) {
      var s = taskState(t.id);
      if (s === "ok") st.ok++;
      if (s === "bad") { st.bad++; if (understood.indexOf(t.id) < 0) st.openBad++; }
    });
    return st;
  }
  /* освоено: все задания верно; повторить: есть неверное; закрепить: остальное */
  function mastery(stepId) {
    var st = stepStats(stepId);
    if (!st.total) return null;
    if (st.ok === st.total) return "mastered";
    if (st.bad > 0) return "repeat";
    return "reinforce";
  }
  function needsRepeat(stepId) { return cardMarks[stepId] === "repeat" || stepStats(stepId).openBad > 0; }
  var STATE_RU = { ok: "верно", bad: "неверно", none: "не решено" };
  var GLYPH = { ok: "✓", bad: "✕", none: "○" };

  /* ---------- окна ---------- */
  var lastTrigger = null;
  function openDialog(dlg, trigger) {
    lastTrigger = trigger || document.activeElement;
    dlg.showModal();
  }
  document.querySelectorAll("dialog").forEach(function (dlg) {
    dlg.addEventListener("close", function () { if (lastTrigger && lastTrigger.focus) lastTrigger.focus(); });
    dlg.addEventListener("click", function (ev) { if (ev.target === dlg) dlg.close(); });
  });

  /* ---------- тема, «автор / модель» ---------- */
  var root = document.documentElement;
  var storedTheme = store.get(K.theme, null);
  var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = storedTheme || (prefersDark ? "dark" : "light");
  var tbtn = document.getElementById("toggle-theme");
  if (tbtn) tbtn.addEventListener("click", function () {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    store.set(K.theme, root.dataset.theme);
  });

  var bybtn = document.getElementById("toggle-by");
  function applyBy(on) {
    document.body.classList.toggle("show-by", on);
    if (bybtn) bybtn.setAttribute("aria-pressed", on ? "true" : "false");
  }
  applyBy(store.get(K.by, false));
  if (bybtn) bybtn.addEventListener("click", function () {
    var on = !document.body.classList.contains("show-by");
    applyBy(on); store.set(K.by, on);
  });

  /* ---------- общее: счётчик ✦, отметки «пройден», состояния заданий ---------- */
  function updateCounter() {
    var counter = document.getElementById("solved-count");
    if (!counter) return;
    var solved = meta.tasks.filter(function (t) { return taskState(t.id) === "ok"; }).length;
    counter.textContent = String(solved);
    document.getElementById("solved-link").setAttribute("aria-label", "Решено заданий: " + solved + " из " + meta.tasks.length);
  }
  updateCounter();
  document.querySelectorAll("li[data-node]").forEach(function (li) { li.classList.toggle("done", isDone(li.dataset.node)); });
  document.querySelectorAll("[data-task-chip]").forEach(function (chip) {
    var s = taskState(chip.dataset.taskChip);
    chip.dataset.state = s;
    chip.setAttribute("aria-label", "Задание " + chip.textContent.trim() + ": " + STATE_RU[s]);
  });
  document.querySelectorAll("[data-task-state]").forEach(function (e) { e.textContent = STATE_RU[taskState(e.dataset.taskState)]; });

  /* ---------- меню пути (мобильная шторка) ---------- */
  var drawerBtn = document.getElementById("open-drawer");
  if (drawerBtn) drawerBtn.addEventListener("click", function () { openDialog(document.getElementById("drawer"), drawerBtn); });

  /* ---------- страница шага ---------- */
  var stepData = readJSON("step-data");
  if (stepData) initStep(stepData);

  function highlightEl(target) {
    for (var p = target.parentElement; p; p = p.parentElement) if (p.tagName === "DETAILS") p.open = true;
    target.scrollIntoView({ block: "center" });
    target.classList.add("hl");
    setTimeout(function () { target.classList.remove("hl"); }, 4000);
  }
  /* «Перечитать»: абзац шага, который ссылается на утверждение; если такого нет — сам блок утверждения с цитатой */
  function highlightClaim(claimId) {
    var target = document.querySelector('.para[data-claims~="' + claimId + '"]') || document.getElementById(claimAnchor(claimId));
    if (!target) return false;
    highlightEl(target);
    return true;
  }


  /* ---------- интерактив: слайдер → график. Значения посчитал код (Python) и положил в страницу, здесь только рисуем ---------- */
  function se(tag, attrs, text) {                   // адрес пространства имён — литералом: var ниже вызова initStep был бы ещё undefined
    var e = document.createElementNS("http://www.w3.org/2000/svg", tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function ruNum(v) {
    var s = (v === Math.round(v) && Math.abs(v) < 1e7) ? String(Math.round(v)) : String(Number(v.toPrecision(4)));
    if (/e/.test(s)) { var m = s.split("e"); s = m[0] + "·10^" + parseInt(m[1], 10); }
    return s.replace(".", ",");
  }
  function niceTicks(lo, hi, n) {
    var span = hi - lo;
    if (span <= 0) return [lo];
    var raw = span / (n - 1), mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var step = [1, 2, 2.5, 5, 10].map(function (m) { return m * mag; }).filter(function (v) { return v >= raw; })[0];
    var out = [];
    for (var t = Math.ceil(lo / step - 1e-9) * step; t <= hi + step * 1e-9; t += step) out.push(Number(t.toPrecision(10)));
    return out;
  }
  function wrapText(text, max) {
    var lines = [], cur = "";
    text.split(/\s+/).forEach(function (w) {
      if (cur && cur.length + 1 + w.length > max) { lines.push(cur); cur = w; } else { cur = (cur + " " + w).trim(); }
    });
    if (cur) lines.push(cur);
    return lines;
  }

  function initInteractive(d) {
    var P = d.palette, S = d.slider, Y = d.y, X = d.x, T = d.template;
    var svg = document.getElementById("inter-chart"), slider = document.getElementById("inter-slider"), out = document.getElementById("inter-readout");
    var W = 400, FS = 18, LH = 25, pl = 74, pr = T === "growth" ? 296 : 372, n = S.values.length;      // правый край с запасом: подпись последней отметки (напр. «1940») не должна уходить за рисунок
    function lab(o) { return o.unit ? o.label + ", " + o.unit : o.label; }
    var hlo, hhi, vlo, vhi, hlab, vlab, depth = T === "profile";
    if (T === "profile") {
      hlo = Y.min; hhi = Y.max; vlo = S.values[0]; vhi = S.values[n - 1]; hlab = lab(Y); vlab = lab(S) + " (глубина растёт вниз)";
      var pad = (hhi - hlo) * 0.05; hlo -= pad; hhi += pad;
    } else if (T === "distribution") {
      hlo = X.values[0]; hhi = X.values[X.values.length - 1]; vlo = Y.min; vhi = Y.max; hlab = lab(X); vlab = lab(Y);
    } else {
      hlo = S.values[0]; hhi = S.values[n - 1]; vlo = Y.min; vhi = Y.max; hlab = lab(S); vlab = lab(Y);
    }
    var top = wrapText("по вертикали: " + vlab, 34), bot = wrapText("по горизонтали: " + hlab, 34);
    var pt = 16 + top.length * LH + 8, ph = 240, pb = pt + ph;
    var H = pb + 34 + bot.length * LH + 8 + 32 + 16;
    var hp = function (v) { return pl + (v - hlo) / ((hhi - hlo) || 1) * (pr - pl); };
    var vp = function (v) { var f = (v - vlo) / ((vhi - vlo) || 1); return depth ? pt + f * ph : pb - f * ph; };
    svg.textContent = "";
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.setAttribute("font-family", "system-ui, 'Segoe UI', sans-serif");
    svg.appendChild(se("rect", { width: W, height: H, rx: 12, fill: P.bg }));
    top.forEach(function (l, i) { svg.appendChild(se("text", { x: 16, y: 16 + FS - 4 + i * LH, "font-size": FS, fill: P.muted }, l)); });
    niceTicks(hlo, hhi, 4).forEach(function (t) {
      svg.appendChild(se("line", { x1: hp(t), y1: pt, x2: hp(t), y2: pb, stroke: P.muted, "stroke-width": 1, "stroke-opacity": 0.35 }));
      svg.appendChild(se("text", { x: hp(t), y: pb + 24, "font-size": FS, fill: P.text, "text-anchor": "middle" }, ruNum(t)));
    });
    niceTicks(vlo, vhi, 5).forEach(function (t) {
      svg.appendChild(se("line", { x1: pl, y1: vp(t), x2: pr, y2: vp(t), stroke: P.muted, "stroke-width": 1, "stroke-opacity": 0.35 }));
      svg.appendChild(se("text", { x: pl - 8, y: vp(t) + 6, "font-size": FS, fill: P.text, "text-anchor": "end" }, ruNum(t)));
    });
    svg.appendChild(se("line", { x1: pl, y1: pt, x2: pl, y2: pb, stroke: P.muted, "stroke-width": 2 }));
    svg.appendChild(se("line", { x1: pl, y1: depth ? pt : pb, x2: pr, y2: depth ? pt : pb, stroke: P.muted, "stroke-width": 2 }));
    bot.forEach(function (l, i) { svg.appendChild(se("text", { x: 16, y: pb + 34 + FS - 4 + i * LH, "font-size": FS, fill: P.muted }, l)); });

    var line = { fill: "none", "stroke-linejoin": "round", "stroke-linecap": "round" };
    var ghosts = [], full = null, cur, dot, hline = null, bar = null;
    if (T === "distribution") {
      [0, n - 1].forEach(function (k) {
        var g = se("polyline", Object.assign({}, line, { stroke: P.muted, "stroke-width": 2, "stroke-dasharray": "6 5",
          points: X.values.map(function (x, j) { return hp(x) + "," + vp(d.series[k][j]); }).join(" ") }));
        svg.appendChild(g);
      });
    } else {
      var pts = S.values.map(function (s, k) { return depth ? hp(d.series[k]) + "," + vp(s) : hp(s) + "," + vp(d.series[k]); }).join(" ");
      svg.appendChild(se("polyline", Object.assign({}, line, { stroke: P.color, "stroke-opacity": 0.3, "stroke-width": 2.5, points: pts })));
    }
    cur = se("polyline", Object.assign({}, line, { stroke: P.color, "stroke-width": 3.5, points: "" }));
    svg.appendChild(cur);
    if (depth) { hline = se("line", { x1: pl, x2: pr, stroke: P.muted, "stroke-width": 2, "stroke-dasharray": "6 5" }); svg.appendChild(hline); }
    if (T !== "distribution") { dot = se("circle", { r: 7, fill: P.color, stroke: P.bg, "stroke-width": 2 }); svg.appendChild(dot); }
    if (T === "growth") {
      svg.appendChild(se("rect", { x: 316, y: pt, width: 62, height: ph, rx: 6, fill: "none", stroke: P.muted, "stroke-width": 2 }));
      bar = se("rect", { x: 318, width: 58, rx: 4, fill: P.color });
      svg.appendChild(bar);
    }
    var bw = "симуляция".length * FS * 0.6 + 28, by = H - 16 - 32;
    svg.appendChild(se("rect", { x: W - 16 - bw, y: by, width: bw, height: 32, rx: 16, fill: P.badge }));
    svg.appendChild(se("text", { x: W - 16 - bw / 2, y: by + 22, "font-size": FS, "font-weight": 700, fill: P.badgeText, "text-anchor": "middle" }, "симуляция"));

    function update(i) {
      var sv = S.values[i], text;
      if (T === "distribution") {
        var row = d.series[i];
        cur.setAttribute("points", X.values.map(function (x, j) { return hp(x) + "," + vp(row[j]); }).join(" "));
        text = lab(S) + ": " + ruNum(sv) + " · " + Y.label + ": от " + ruNum(Math.min.apply(null, row)) + " до " + ruNum(Math.max.apply(null, row)) + (Y.unit ? " " + Y.unit : "");
      } else {
        var yv = d.series[i], p = [];
        for (var k = 0; k <= i; k++) p.push(depth ? hp(d.series[k]) + "," + vp(S.values[k]) : hp(S.values[k]) + "," + vp(d.series[k]));
        cur.setAttribute("points", p.join(" "));
        dot.setAttribute("cx", depth ? hp(yv) : hp(sv));
        dot.setAttribute("cy", depth ? vp(sv) : vp(yv));
        if (hline) { hline.setAttribute("y1", vp(sv)); hline.setAttribute("y2", vp(sv)); }
        if (bar) { var hh = Math.max(2, (yv - vlo) / ((vhi - vlo) || 1) * (ph - 4)); bar.setAttribute("y", pb - 2 - hh); bar.setAttribute("height", hh); }
        text = lab(S) + ": " + ruNum(sv) + " → " + lab(Y) + ": " + ruNum(yv);
      }
      out.textContent = text;
      slider.setAttribute("aria-valuetext", text);
    }
    slider.addEventListener("input", function () { update(Number(slider.value)); });
    slider.value = String(Math.round((n - 1) * 0.4));
    update(Number(slider.value));
  }

  function initStep(data) {
    var nodeId = data.node_id;
    store.set(K.last, nodeId);

    /* оглавление страницы: на узком экране свёрнуто */
    var toc = document.getElementById("toc-details");
    if (toc && window.matchMedia("(max-width: 767.98px)").matches) toc.open = false;

    /* чек-лист → прогресс шага → «Шаг пройден» */
    var checks = store.get(K.checks, {});
    var mine = checks[nodeId] || {};
    var boxes = document.querySelectorAll("[data-check]");
    var taskList = tasksOf[nodeId] || [];
    function refresh() {
      var okCount = 0;
      boxes.forEach(function (b) {
        if (b.dataset.check === "tasks") b.checked = taskList.length > 0 && stepStats(nodeId).ok === taskList.length;
        else b.checked = !!mine[b.dataset.check];
        if (b.checked) okCount++;
      });
      var tp = document.getElementById("tasks-progress");
      if (tp) tp.textContent = stepStats(nodeId).ok + " из " + taskList.length;
      document.getElementById("step-bar").style.width = Math.round(100 * okCount / boxes.length) + "%";
      document.getElementById("step-progress-text").textContent = "Прогресс шага: " + okCount + " из " + boxes.length;
      var all = okCount === boxes.length;
      document.getElementById("done-banner").hidden = !all;
      if (isDone(nodeId) !== all) setDone(nodeId, all);
      document.querySelectorAll('li[data-node="' + nodeId + '"]').forEach(function (li) { li.classList.toggle("done", all); });
    }
    boxes.forEach(function (b) {
      if (b.dataset.check === "tasks") return;
      b.addEventListener("change", function () {
        mine[b.dataset.check] = b.checked;
        checks[nodeId] = mine;
        store.set(K.checks, checks);
        refresh();
      });
    });
    var video = document.querySelector("#b-media video");
    if (video) video.addEventListener("ended", function () {
      mine.video = true; checks[nodeId] = mine; store.set(K.checks, checks); refresh();
    });
    refresh();

    /* «проверь по книге» */
    var dlg = document.getElementById("book");
    var body = document.getElementById("book-body");
    var VSTAT = {
      ok: "Проверка: замечаний к утверждению нет",
      not_checked: "Проверка ещё не запускалась",
      remark: "Замечание проверки"
    };
    function claimBlock(id) {
      var c = data.claims[id];
      var box = el("div", "dlg-claim");
      box.appendChild(el("p", "muted", "стр. " + c.page + (c.page_print ? " (печатная " + c.page_print + ")" : "")));
      var q = el("blockquote", "quote");
      q.setAttribute("data-by", "author");
      q.appendChild(el("span", null, "«" + c.quote + "»"));
      box.appendChild(q);
      var t = el("p", null, "В курсе: " + c.text);
      t.setAttribute("data-by", c.by);
      box.appendChild(t);
      var v = c.verify;
      box.appendChild(el("p", "vstat " + v.status, VSTAT[v.status] + (v.status === "remark" ? " (" + v.severity + "): " + v.problem : "")));
      return box;
    }
    function scanBlock(p) {
      var info = data.pages[String(p)];
      if (info && info.scan) {
        var img = el("img", "scan");
        img.src = info.scan;
        img.alt = "Скан страницы " + p + " книги";
        return img;
      }
      return el("p", "muted", "Скан страницы " + p + " в курс не добавлен.");
    }
    function openBook(claimId, pageNo, trigger) {
      body.textContent = "";
      var p = pageNo;
      if (claimId) {
        body.appendChild(claimBlock(claimId));
        p = data.claims[claimId].page;
      } else {
        var ids = (data.pages[String(p)] || { claim_ids: [] }).claim_ids;
        if (!ids.length) body.appendChild(el("p", "muted", "На этой странице у шага нет утверждений с цитатой."));
        ids.forEach(function (id) { body.appendChild(claimBlock(id)); });
      }
      body.appendChild(scanBlock(p));
      openDialog(dlg, trigger);
    }
    document.addEventListener("click", function (ev) {
      var b = ev.target.closest(".pg");
      if (!b) return;
      openBook(b.dataset.claim || null, b.dataset.page ? Number(b.dataset.page) : null, b);
    });

    /* формулы: KaTeX из assets курса; если он не загрузился, остаётся подписанный моноширинный блок */
    document.querySelectorAll(".tex[data-tex]").forEach(function (el) {
      if (window.katex) {
        window.katex.render(el.dataset.tex.replace(/^\s*\$+|\$+\s*$/g, ""), el, { displayMode: true, throwOnError: false, strict: "ignore" });
      } else {
        console.error("KaTeX не загружен: формула показана исходным текстом");
      }
      el.classList.add("rendered");
    });

    /* задания */
    var specs = readJSON("tasks-data") || {};
    document.querySelectorAll(".task").forEach(function (task) { initTask(task, specs[task.dataset.task]); });

    function paintChip(taskId) {
      document.querySelectorAll('[data-task-chip="' + taskId + '"]').forEach(function (chip) {
        var st = taskState(taskId);
        chip.dataset.state = st;
        chip.setAttribute("aria-label", "Задание " + chip.textContent.trim() + ": " + STATE_RU[st]);
      });
    }
    function saveResult(taskId, state, ans) {
      if (state) { taskRes[taskId] = state; answers[taskId] = ans; } else { delete taskRes[taskId]; delete answers[taskId]; }
      store.set(K.tasks, taskRes);
      store.set(K.answers, answers);
      if (state === "bad") {                 // снова ошиблись: задание возвращается в «Мои ошибки»
        understood = understood.filter(function (x) { return x !== taskId; });
        store.set(K.understood, understood);
      }
      paintChip(taskId);
      updateCounter();
      refresh();
    }
    function normWord(w) { return String(w).trim().toLowerCase().replace(/ё/g, "е").replace(/\s+/g, " "); }

    function initTask(task, spec) {
      var id = task.dataset.task;
      var checkBtn = task.querySelector('[data-action="check"]');
      var fb = task.querySelector(".feedback");
      var msg = task.querySelector(".task-msg");
      var list = task.querySelector(".order");
      var controls = task.querySelectorAll("input, .order-btns button");

      function answerFromPage() {
        if (spec.type === "single") {
          var r = task.querySelector("input[type=radio]:checked");
          return r ? r.value : null;
        }
        if (spec.type === "multiple") {
          var v = [].map.call(task.querySelectorAll("input[type=checkbox]:checked"), function (i) { return i.value; });
          return v.length ? v : null;
        }
        if (spec.type === "order") {
          return [].map.call(list.children, function (li) { return li.dataset.id; });
        }
        if (spec.type === "gap") {
          var gaps = [].slice.call(task.querySelectorAll(".gap")).sort(function (a, b) { return a.dataset.gap - b.dataset.gap; });
          var words = gaps.map(function (g) { return g.value.trim(); });
          return words.every(Boolean) ? words : null;
        }
        var n = parseFloat(task.querySelector(".calc-input").value.replace(",", "."));
        return isNaN(n) ? null : n;
      }
      function isRight(ans) {
        if (spec.type === "single") return ans === spec.answer;
        if (spec.type === "multiple") return ans.length === spec.answer.length && ans.every(function (x) { return spec.answer.indexOf(x) >= 0; });
        if (spec.type === "order") return ans.join("|") === spec.answer.join("|");
        if (spec.type === "gap") return ans.every(function (w, i) { return normWord(w) === normWord(spec.answer[i]); });
        return Math.abs(ans - spec.answer) <= (spec.tolerance || 0) + 1e-9;
      }
      var EMPTY_MSG = {
        single: "Выбери один вариант и нажми «Проверить».", multiple: "Отметь варианты и нажми «Проверить».",
        gap: "Заполни все пропуски.", calc: "Введи число."
      };
      function lock(on) {
        controls.forEach(function (c) { c.disabled = on; });
        if (list) list.classList.toggle("locked", on);
        checkBtn.hidden = on;
      }
      function mark(ans) {
        if (spec.type === "single" || spec.type === "multiple") {
          var right = [].concat(spec.answer);
          task.querySelectorAll(".opt").forEach(function (opt) {
            var inp = opt.querySelector("input");
            var isRightOpt = right.indexOf(inp.value) >= 0;
            opt.classList.toggle("correct", isRightOpt);
            opt.classList.toggle("wrong", !isRightOpt && inp.checked);
          });
        } else if (spec.type === "order") {
          [].forEach.call(list.children, function (li, i) {
            var ok = li.dataset.id === spec.answer[i];
            li.classList.toggle("correct", ok);
            li.classList.toggle("wrong", !ok && ans !== null);
          });
        } else if (spec.type === "gap" && ans) {
          task.querySelectorAll(".gap").forEach(function (g, i) {
            var ok = normWord(g.value) === normWord(spec.answer[g.dataset.gap - 1]);
            g.classList.toggle("correct", ok);
            g.classList.toggle("wrong", !ok);
          });
        } else if (spec.type === "calc" && ans !== null) {
          task.querySelector(".calc-input").classList.add(isRight(ans) ? "correct" : "wrong");
        }
      }
      function setOrder(ids) {
        ids.forEach(function (oid) {
          list.appendChild([].filter.call(list.children, function (li) { return li.dataset.id === oid; })[0]);
        });
      }
      /* вернуть на страницу выбор ученика (после перезагрузки) */
      function applyAnswer(ans) {
        if (spec.type === "single") {
          var r = task.querySelector('input[type=radio][value="' + ans + '"]');
          if (r) r.checked = true;
        } else if (spec.type === "multiple") {
          task.querySelectorAll("input[type=checkbox]").forEach(function (c) { c.checked = ans.indexOf(c.value) >= 0; });
        } else if (spec.type === "order") {
          setOrder(ans);
        } else if (spec.type === "gap") {
          task.querySelectorAll(".gap").forEach(function (g) { g.value = ans[g.dataset.gap - 1] || ""; });
        } else {
          task.querySelector(".calc-input").value = String(ans);
        }
      }
      function show(ok, ans) {
        if (ans === null) {
          if (spec.type === "order") setOrder(spec.answer);   // выбор не сохранён (старые данные): показываем верный порядок
        } else {
          applyAnswer(ans);
        }
        mark(ans);
        fb.hidden = false;
        fb.dataset.result = ok ? "ok" : "bad";
        lock(true);
      }
      function clear() {
        fb.hidden = true;
        msg.textContent = "";
        task.querySelectorAll(".correct, .wrong").forEach(function (e) { e.classList.remove("correct", "wrong"); });
        task.querySelectorAll("input[type=radio], input[type=checkbox]").forEach(function (i) { i.checked = false; });
        task.querySelectorAll(".gap, .calc-input").forEach(function (i) { i.value = ""; });
        lock(false);
      }

      checkBtn.addEventListener("click", function () {
        var ans = answerFromPage();
        if (ans === null) { msg.textContent = EMPTY_MSG[spec.type]; return; }
        msg.textContent = "";
        var ok = isRight(ans);
        show(ok, ans);
        saveResult(id, ok ? "ok" : "bad", ans);
        fb.focus();
        fb.scrollIntoView({ block: "nearest" });
      });
      task.querySelector('[data-action="reread"]').addEventListener("click", function (ev) {
        highlightClaim(ev.currentTarget.dataset.claim);
      });
      var got = task.querySelector('[data-action="understood"]');
      got.setAttribute("aria-pressed", understood.indexOf(id) >= 0 ? "true" : "false");
      got.addEventListener("click", function () {
        var on = got.getAttribute("aria-pressed") !== "true";
        got.setAttribute("aria-pressed", on ? "true" : "false");
        understood = understood.filter(function (x) { return x !== id; });
        if (on) understood.push(id);
        store.set(K.understood, understood);
      });
      task.querySelector('[data-action="again"]').addEventListener("click", function () {
        clear();
        saveResult(id, null);
        checkBtn.focus();
      });

      /* порядок: кнопки ↑↓ (клавиатура) и перетаскивание за ручку (pointer events: мышь и палец) */
      if (list) {
        var announce = function (li) {
          var items = [].slice.call(list.children);
          msg.textContent = "«" + li.querySelector(".opt-text").textContent + "»: позиция " + (items.indexOf(li) + 1) + " из " + items.length;
        };
        list.addEventListener("click", function (ev) {
          var b = ev.target.closest("[data-move]");
          if (!b || b.disabled) return;
          var li = b.closest(".order-item");
          var other = b.dataset.move === "up" ? li.previousElementSibling : li.nextElementSibling;
          if (other) {
            if (b.dataset.move === "up") list.insertBefore(li, other); else list.insertBefore(other, li);
            b.focus();                         // перенос узла в DOM сбрасывает фокус
          }
          announce(li);
        });
        var dragged = null;
        list.addEventListener("pointerdown", function (ev) {
          var h = ev.target.closest(".drag-handle");
          if (!h || list.classList.contains("locked")) return;
          ev.preventDefault();
          dragged = h.closest(".order-item");
          dragged.classList.add("dragging");
          list.setPointerCapture(ev.pointerId);   // захват на списке: сам элемент при перестановке переносится в DOM
        });
        list.addEventListener("pointermove", function (ev) {
          if (!dragged) return;
          var before = null;
          [].some.call(list.children, function (li) {
            if (li === dragged) return false;
            var r = li.getBoundingClientRect();
            if (ev.clientY < r.top + r.height / 2) { before = li; return true; }
            return false;
          });
          if (before !== dragged.nextElementSibling) list.insertBefore(dragged, before);
        });
        var drop = function () {
          if (!dragged) return;
          dragged.classList.remove("dragging");
          announce(dragged);
          dragged = null;
        };
        list.addEventListener("pointerup", drop);
        list.addEventListener("pointercancel", drop);
      }

      /* уже решённое: выбор ученика, верные ответы и разбор */
      if (taskState(id) !== "none") show(taskState(id) === "ok", id in answers ? answers[id] : null);
    }

    /* «Сначала угадай»: шаг открывается вопросом; без ответа тело шага скрыто (кроме перехода по ссылке на абзац) */
    var box = document.getElementById("guess");
    if (box) {
      var body0 = document.getElementById("step-body"), res = box.querySelector(".guess-result");
      var gbtns = box.querySelectorAll("[data-answer]"), gskip = box.querySelector('[data-action="skip"]');
      var truth = box.dataset.truth === "true", saved = store.get(K.guess, {});
      var reveal = function (answer) {
        body0.hidden = false;
        gbtns.forEach(function (b) { b.disabled = true; b.setAttribute("aria-pressed", b.dataset.answer === answer ? "true" : "false"); });
        gskip.hidden = true;
        if (answer !== "skip") { res.dataset.result = answer === String(truth) ? "ok" : "bad"; res.hidden = false; }
      };
      var choose = function (answer) {
        saved[nodeId] = answer;
        store.set(K.guess, saved);
        reveal(answer);
        if (answer !== "skip") res.focus();
      };
      if (saved[nodeId]) reveal(saved[nodeId]);
      else if (location.hash.length < 2) body0.hidden = true;
      gbtns.forEach(function (b) { b.addEventListener("click", function () { choose(b.dataset.answer); }); });
      gskip.addEventListener("click", function () { choose("skip"); });
    }

    /* «Решение на данных» по шагам: признаки → правило → вывод (без JS видно всё сразу) */
    var flow = document.querySelector(".sig-flow[data-stepper]");
    if (flow) {
      var ctl = flow.parentElement.querySelector(".stepper-ctl"), stext = ctl.querySelector(".stepper-text");
      var snext = ctl.querySelector("[data-stepper-next]"), sall = ctl.querySelector("[data-stepper-all]");
      var counterEx = flow.parentElement.querySelector(".counter");
      var NAMES = ["признаки", "правило", "вывод"], NEXT = ["Дальше: правило", "Дальше: вывод", "Сначала"], stage = 1;
      var paint = function () {
        flow.dataset.stage = String(stage);
        stext.textContent = "Шаг " + stage + " из 3: " + NAMES[stage - 1];
        snext.textContent = NEXT[stage - 1];
        sall.hidden = stage === 3;
        if (counterEx) counterEx.hidden = stage < 3;
      };
      ctl.hidden = false;
      paint();
      snext.addEventListener("click", function () { stage = stage === 3 ? 1 : stage + 1; paint(); });
      sall.addEventListener("click", function () { stage = 3; paint(); });
    }

    var idata = readJSON("inter-data");
    if (idata) initInteractive(idata);

    /* переход по ссылке «Перечитать»: #<id абзаца> или #task-…; якоря оглавления (разделы) браузер ведёт сам */
    function focusHash() {
      if (location.hash.length < 2) return;
      var id = decodeURIComponent(location.hash.slice(1));
      var m = /^(.+)--(c\d+)$/.exec(id);
      if (m) { highlightClaim(m[1] + "#" + m[2]); return; }
      var t = document.getElementById(id);
      if (t && (t.classList.contains("para") || t.classList.contains("task"))) highlightEl(t);
    }
    /* после load: браузер сам доскролливает к якорю уже после наших скриптов и перебил бы подсветку */
    if (document.readyState === "complete") focusHash();
    else window.addEventListener("load", function () { setTimeout(focusHash, 0); });
    window.addEventListener("hashchange", focusHash);
  }

  /* ---------- путь ---------- */
  if (page === "index") {
    var n = meta.steps.filter(function (s) { return isDone(s.id); }).length;
    document.getElementById("progress-bar").style.width = Math.round(100 * n / meta.steps.length) + "%";
    document.getElementById("progress-text").textContent = "Пройдено " + n + " из " + meta.steps.length;
    var ring = document.getElementById("ring-fg");
    if (ring) {
      var len = 2 * Math.PI * ring.r.baseVal.value;
      ring.style.strokeDasharray = String(len);
      ring.style.strokeDashoffset = String(len * (1 - n / meta.steps.length));
    }

    var last = store.get(K.last, null);
    if (last && stepById[last]) {
      var r = document.getElementById("resume");
      r.href = "step-" + last + ".html";
      document.getElementById("resume-label").textContent = "Продолжить";
      document.getElementById("resume-title").textContent = stepById[last].title;
      var lastLi = document.querySelector('.steps-list li[data-node="' + last + '"]');
      if (lastLi) lastLi.classList.add("last");
    }

    document.querySelectorAll(".badge[data-badge]").forEach(function (b) {
      var st = stepStats(b.dataset.badge);
      b.textContent = "решено " + st.ok + "/" + st.total;
      b.classList.toggle("complete", st.ok === st.total);
    });

    var filter = { part: "", seg: "all" };
    function applyFilter() {
      var shown = 0;
      document.querySelectorAll(".part").forEach(function (sec) {
        var visible = 0;
        var partOk = !filter.part || sec.dataset.part === filter.part;
        sec.querySelectorAll("li[data-node]").forEach(function (li) {
          var ok = partOk && (filter.seg === "all" || needsRepeat(li.dataset.node));
          li.hidden = !ok;
          if (ok) visible++;
        });
        sec.hidden = visible === 0;
        shown += visible;
      });
      document.getElementById("steps-empty").hidden = shown !== 0;
    }
    function bindGroup(selector, key, attr) {
      var btns = document.querySelectorAll(selector);
      btns.forEach(function (b) {
        b.addEventListener("click", function () {
          filter[key] = b.dataset[attr];
          btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          applyFilter();
        });
      });
    }
    bindGroup(".part-tabs button", "part", "part");
    bindGroup(".segment button", "seg", "seg");
  }

  /* ---------- карточки ---------- */
  if (page === "cards") {
    var paint = function (card) {
      var m = cardMarks[card.dataset.node];
      card.classList.toggle("mark-know", m === "know");
      card.classList.toggle("mark-repeat", m === "repeat");
      card.querySelectorAll("[data-mark]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.mark === m ? "true" : "false"); });
    };
    document.querySelectorAll(".card").forEach(function (card) {
      paint(card);
      card.querySelectorAll("[data-mark]").forEach(function (b) {
        b.addEventListener("click", function () {
          cardMarks[card.dataset.node] = b.dataset.mark; store.set(K.cards, cardMarks); paint(card);
        });
      });
    });
    var only = document.getElementById("only-repeat");
    only.addEventListener("change", function () { document.body.classList.toggle("only-repeat", only.checked); });
  }

  /* ---------- «Мой прогресс» ---------- */
  if (page === "progress" && meta.tasks.length) renderProgress();

  function renderProgress() {
    var groups = { repeat: [], reinforce: [], mastered: [] };
    meta.steps.forEach(function (s) { var m = mastery(s.id); if (m) groups[m].push(s); });
    var total = groups.repeat.length + groups.reinforce.length + groups.mastered.length;
    var pct = Math.round(100 * groups.mastered.length / total);
    document.getElementById("mastery-pct").textContent = pct + "% освоено";
    ["repeat", "reinforce", "mastered"].forEach(function (k) {
      document.querySelector('[data-seg-bar="' + k + '"]').style.width = (100 * groups[k].length / total) + "%";
      document.querySelector('[data-tab-n="' + k + '"]').textContent = String(groups[k].length);
    });
    var legend = "Нужно повторить: " + groups.repeat.length + " · Закрепить: " + groups.reinforce.length + " · Освоено: " + groups.mastered.length;
    document.getElementById("mastery-legend").textContent = legend;
    document.getElementById("mastery-bar").setAttribute("aria-label", pct + "% освоено. " + legend);

    var tabs = document.querySelectorAll(".tabs button");
    var list = document.getElementById("progress-list");
    var empty = document.getElementById("progress-empty");
    function show(tab) {
      tabs.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.tab === tab ? "true" : "false"); });
      list.textContent = "";
      groups[tab].forEach(function (s) { list.appendChild(progressRow(s)); });
      empty.hidden = groups[tab].length > 0;
    }
    tabs.forEach(function (b) { b.addEventListener("click", function () { show(b.dataset.tab); }); });
    show(["repeat", "reinforce", "mastered"].filter(function (k) { return groups[k].length; })[0]);
  }

  function progressRow(s) {
    var li = el("li");
    li.appendChild(el("p", "pl-title", s.title));
    var segs = el("div", "msegs");
    var list = tasksOf[s.id];
    var firstBad = null;
    list.forEach(function (t, i) {
      var st = taskState(t.id);
      if (st === "bad" && !firstBad) firstBad = t;
      var seg = el("span", "mseg");
      seg.dataset.state = st;
      seg.setAttribute("role", "img");
      seg.setAttribute("aria-label", "Задание " + (i + 1) + ": " + STATE_RU[st]);
      var g = el("span", null, GLYPH[st]);
      g.setAttribute("aria-hidden", "true");
      seg.appendChild(g);
      segs.appendChild(seg);
    });
    li.appendChild(segs);
    var btns = el("div", "pl-btns");
    var target = firstBad || list[0];
    var reread = el("a", "btn-small", "Перечитать");
    reread.href = "step-" + s.id + ".html#" + claimAnchor(target.claim_ids[0]);
    var tasks = el("a", "btn-small", "Задания");
    tasks.href = "step-" + s.id + ".html#b-quiz";
    btns.appendChild(reread);
    btns.appendChild(tasks);
    li.appendChild(btns);
    return li;
  }

  /* ---------- «Мои ошибки» ---------- */
  if (page === "mistakes" && meta.tasks.length) renderMistakes();

  function renderMistakes() {
    var bad = meta.tasks.filter(function (t) { return taskState(t.id) === "bad"; });
    var open = bad.filter(function (t) { return understood.indexOf(t.id) < 0; });
    var nums = document.getElementById("mistake-nums");
    var list = document.getElementById("mistakes-list");
    nums.textContent = "";
    list.textContent = "";
    open.forEach(function (t, i) {
      var a = el("a", "tnum", String(i + 1));
      a.href = "#m-" + t.id;
      a.dataset.state = "bad";
      a.setAttribute("aria-label", "Ошибка " + (i + 1) + ": неверно");
      nums.appendChild(a);

      var li = el("li");
      li.id = "m-" + t.id;
      var step = el("p", "m-step");
      var link = el("a", null, stepById[t.step_id].title);
      link.href = "step-" + t.step_id + ".html";
      step.appendChild(document.createTextNode("Ошибка " + (i + 1) + " · шаг «"));
      step.appendChild(link);
      step.appendChild(document.createTextNode("»"));
      li.appendChild(step);
      li.appendChild(el("p", "prompt", t.prompt));
      li.appendChild(el("p", "muted", t.explanation));
      var row = el("div", "pl-btns");
      var reread = el("a", "btn-small", "Перечитать");
      reread.href = "step-" + t.step_id + ".html#" + claimAnchor(t.claim_ids[0]);
      row.appendChild(reread);
      var flip = el("label", "m-flip");
      var box = el("input");
      box.type = "checkbox";
      box.addEventListener("change", function () {
        understood.push(t.id);
        store.set(K.understood, understood);
        renderMistakes();
      });
      flip.appendChild(box);
      flip.appendChild(el("span", null, "Я понял"));
      row.appendChild(flip);
      li.appendChild(row);
      list.appendChild(li);
    });
    nums.hidden = open.length === 0;
    document.getElementById("mistakes-empty").hidden = open.length !== 0;
    var back = bad.length - open.length;
    document.getElementById("mistakes-understood").hidden = back === 0;
    document.getElementById("understood-n").textContent = String(back);
    document.getElementById("restore-understood").onclick = function () {
      var badIds = bad.map(function (t) { return t.id; });
      understood = understood.filter(function (x) { return badIds.indexOf(x) < 0; });
      store.set(K.understood, understood);
      renderMistakes();
    };
  }

  /* ---------- карта ---------- */
  if (page === "map") {
    document.querySelectorAll(".map-node").forEach(function (a) { if (isDone(a.dataset.node)) a.classList.add("done"); });
  }
})();
