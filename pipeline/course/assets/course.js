/* Курс открывается из файла: без сети, без fetch, данные — во встроенных <script type="application/json">.

   Хранилище (localStorage, ключи с префиксом course:<глава>:):
     done        [id шага, ...]                  шаг пройден (чек-лист выполнен)
     last        id шага                         последний открытый шаг
     checks      {id шага: {read, video}}        ручные пункты чек-листа
     cards       {id шага: "know" | "repeat"}    карточки
     tasks       {id задания: "ok" | "bad"}      результат последней проверки (пишет логика заданий, задача 3)
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
  ["done", "last", "checks", "cards", "tasks", "understood"].forEach(function (n) { K[n] = "course:" + ch + ":" + n; });
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
  var solved = meta.tasks.filter(function (t) { return taskState(t.id) === "ok"; }).length;
  var counter = document.getElementById("solved-count");
  if (counter) {
    counter.textContent = String(solved);
    document.getElementById("solved-link").setAttribute("aria-label", "Решено заданий: " + solved + " из " + meta.tasks.length);
  }
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

  function highlightPara(id) {
    var target = document.getElementById(id);
    if (!target) return false;
    for (var p = target.parentElement; p; p = p.parentElement) if (p.tagName === "DETAILS") p.open = true;
    target.scrollIntoView({ block: "center" });
    target.classList.add("hl");
    setTimeout(function () { target.classList.remove("hl"); }, 4000);
    return true;
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

    /* «Перечитать» / «Я понял» в разборе ответа (проверка ответа — логика заданий, задача 3) */
    document.querySelectorAll(".task").forEach(function (task) {
      var reread = task.querySelector('[data-action="reread"]');
      if (reread) reread.addEventListener("click", function () { highlightPara(claimAnchor(reread.dataset.claim)); });
      var got = task.querySelector('[data-action="understood"]');
      if (got) got.addEventListener("click", function () {
        var id = task.dataset.task;
        var on = got.getAttribute("aria-pressed") !== "true";
        got.setAttribute("aria-pressed", on ? "true" : "false");
        understood = understood.filter(function (x) { return x !== id; });
        if (on) understood.push(id);
        store.set(K.understood, understood);
      });
    });

    /* переход по ссылке «Перечитать»: #<id абзаца> или #task-…; якоря оглавления (разделы) браузер ведёт сам */
    function focusHash() {
      if (location.hash.length < 2) return;
      var id = decodeURIComponent(location.hash.slice(1));
      var t = document.getElementById(id);
      if (t && (t.classList.contains("para") || t.classList.contains("task"))) highlightPara(id);
    }
    focusHash();
    window.addEventListener("hashchange", focusHash);
  }

  /* ---------- путь ---------- */
  if (page === "index") {
    var n = meta.steps.filter(function (s) { return isDone(s.id); }).length;
    document.getElementById("progress-bar").style.width = Math.round(100 * n / meta.steps.length) + "%";
    document.getElementById("progress-text").textContent = "Пройдено " + n + " из " + meta.steps.length;

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
