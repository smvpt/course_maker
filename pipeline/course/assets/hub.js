/* Главная всех курсов. Без сети и fetch: данные курсов и индекс поиска встроены в страницу.
   Читает localStorage: course:last ({ch, step, title}) и по каждому курсу course:<ch>:done / tasks / understood / last.
   Если localStorage недоступен (file:// в части браузеров) — все статусы «Не начат», без ошибок. */
(function () {
  "use strict";
  function readJSON(id) { return JSON.parse(document.getElementById(id).textContent); }
  function get(k, dflt) {
    try { var v = localStorage.getItem(k); return v === null ? dflt : JSON.parse(v); } catch (e) { return dflt; }
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function norm(t) { return String(t).toLowerCase().replace(/ё/g, "е"); }
  function plural(n, one, few, many) { var m = n % 100, d = n % 10; return m > 10 && m < 20 ? many : d === 1 ? one : d >= 2 && d <= 4 ? few : many; }

  var courses = readJSON("hub-data"), root = document.documentElement;
  var byCh = {};
  courses.forEach(function (c) { byCh[c.ch] = c; });

  /* ---------- прогресс по курсам ---------- */
  function progress(c) {
    var ids = c.steps.map(function (s) { return s.id; });
    var done = (get("course:" + c.ch + ":done", []) || []).filter(function (id) { return ids.indexOf(id) >= 0; }).length;
    var tasks = get("course:" + c.ch + ":tasks", {}) || {};
    var understood = get("course:" + c.ch + ":understood", []) || [];
    var answered = c.task_ids.filter(function (id) { return tasks[id] === "ok" || tasks[id] === "bad"; }).length;
    var bad = c.task_ids.filter(function (id) { return tasks[id] === "bad" && understood.indexOf(id) < 0; }).length;
    var started = done > 0 || answered > 0 || !!get("course:" + c.ch + ":last", null);
    return { done: done, total: ids.length, bad: bad, status: done === ids.length ? "done" : started ? "progress" : "new" };
  }
  var STATUS = { "new": "Не начат", progress: "В процессе", done: "Пройден" };
  var stats = {};
  courses.forEach(function (c) { stats[c.ch] = progress(c); });

  document.querySelectorAll(".course-card").forEach(function (card) {
    var st = stats[card.dataset.ch], c = byCh[card.dataset.ch];
    var s = card.querySelector(".status");
    s.dataset.status = st.status;
    s.textContent = STATUS[st.status];
    card.querySelector(".bar span").style.width = Math.round(100 * st.done / st.total) + "%";
    card.querySelector(".course-done").textContent = st.status === "new" ? "" : "Пройдено " + st.done + " из " + st.total;
  });

  /* ---------- «Продолжить» / «Начните с» ---------- */
  var last = get("course:last", null);
  var resume = document.getElementById("hub-resume"), ring = document.getElementById("hub-ring");
  var cur = last && byCh[last.ch] && last.step ? last : null;
  if (cur) {
    var c = byCh[cur.ch], st = stats[cur.ch], step = c.steps.filter(function (s) { return s.id === cur.step; })[0];
    resume.href = cur.ch + "/course/step-" + cur.step + ".html";
    document.getElementById("hub-resume-label").textContent = "Продолжить:";
    document.getElementById("hub-resume-title").textContent = c.title;
    document.getElementById("hub-resume-sub").textContent = (step ? step.title : cur.title) + " · пройдено " + st.done + " из " + st.total;
    var len = 2 * Math.PI * ring.r.baseVal.value;
    ring.style.strokeDasharray = String(len);
    ring.style.strokeDashoffset = String(len * (1 - st.done / st.total));
  } else {
    var first = courses[0];
    document.getElementById("hub-resume-sub").textContent = first.steps.length + " " + plural(first.steps.length, "шаг", "шага", "шагов") + " · ≈ " + first.minutes + " мин";
    var len0 = 2 * Math.PI * ring.r.baseVal.value;
    ring.style.strokeDasharray = String(len0);
    ring.style.strokeDashoffset = String(len0);
  }

  /* ---------- «Повторить сегодня»: неверные задания по всем курсам ---------- */
  var review = document.getElementById("hub-review"), list = document.getElementById("hub-review-list"), anyBad = 0;
  courses.forEach(function (c) {
    var n = stats[c.ch].bad;
    if (!n) return;
    anyBad += n;
    var li = el("li"), a = el("a", "review-link");
    a.href = c.ch + "/course/mistakes.html";
    a.appendChild(el("strong", null, n + " " + plural(n, "неверное задание", "неверных задания", "неверных заданий")));
    a.appendChild(el("span", "muted", " · " + c.title));
    li.appendChild(a);
    list.appendChild(li);
  });
  review.hidden = anyBad === 0;

  /* ---------- тема ---------- */
  var MODES = ["system", "light", "dark"], NAMES = { system: "Системная", light: "Светлая", dark: "Тёмная" };
  var mode = get("course:theme", "system");
  if (MODES.indexOf(mode) < 0) mode = "system";
  var tbtn = document.getElementById("hub-theme");
  requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add("theme-ready"); }); });
  function paintTheme() {
    if (mode === "system") delete root.dataset.theme; else root.dataset.theme = mode;
    document.getElementById("hub-theme-label").textContent = "Тема: " + NAMES[mode].toLowerCase();
    tbtn.title = "Тема: " + NAMES[mode].toLowerCase(); tbtn.setAttribute("aria-label", tbtn.title);
  }
  paintTheme();
  tbtn.addEventListener("click", function () {
    mode = MODES[(MODES.indexOf(mode) + 1) % MODES.length];
    root.classList.add("theme-anim");
    setTimeout(function () { root.classList.remove("theme-anim"); }, 260);
    paintTheme();
    try { localStorage.setItem("course:theme", JSON.stringify(mode)); } catch (e) { /* без сохранения */ }
  });

  /* ---------- поиск по всем курсам ---------- */
  var index = readJSON("hub-search"), input = document.getElementById("search-input"), box = document.getElementById("search-results");
  function stem(w) { return w.length > 4 ? w.slice(0, w.length - 2) : w; }
  function words(q) { return norm(q).split(/[^a-zа-я0-9]+/).filter(function (w) { return w.length > 1; }).map(stem); }
  function run(q) {
    var ws = words(q), found = [];
    if (!ws.length) return found;
    index.forEach(function (e, i) {
      var hay = e._n || (e._n = norm(e.x));
      for (var k = 0; k < ws.length; k++) if (hay.indexOf(ws[k]) < 0) return;
      found.push({ e: e, i: i, at: hay.indexOf(ws[0]), score: (e.k === "step" ? 20 : e.k === "term" ? 15 : 1) });
    });
    found.sort(function (a, b) { return b.score - a.score || a.i - b.i; });
    return found.slice(0, 12);
  }
  function snippet(text, ws, at) {
    var from = Math.max(0, at - 50), to = Math.min(text.length, from + 150);
    if (from > 0) { var sp = text.indexOf(" ", from); if (sp >= 0 && sp < at) from = sp + 1; }          // по границам слов: без «т множественные» и «нарушает пр…»
    if (to < text.length) { var sp2 = text.lastIndexOf(" ", to); if (sp2 > at) to = sp2; }
    var cut = text.slice(from, to), low = norm(cut), ranges = [];
    ws.forEach(function (w) {
      for (var p = low.indexOf(w); p >= 0; p = low.indexOf(w, p + w.length)) {
        var end = p + w.length;
        while (end < low.length && /[a-zа-я0-9]/.test(low.charAt(end))) end++;                           // подсвечиваем слово целиком, а не только основу
        ranges.push([p, end]);
      }
    });
    ranges.sort(function (a, b) { return a[0] - b[0]; });
    var out = el("span", "sr-snippet"), pos = 0;
    if (from > 0) out.appendChild(document.createTextNode("… "));
    ranges.forEach(function (r) {
      if (r[0] < pos) return;
      out.appendChild(document.createTextNode(cut.slice(pos, r[0])));
      out.appendChild(el("mark", null, cut.slice(r[0], r[1])));
      pos = r[1];
    });
    out.appendChild(document.createTextNode(cut.slice(pos) + (to < text.length ? " …" : "")));
    return out;
  }
  function close() { box.hidden = true; input.setAttribute("aria-expanded", "false"); }
  function render() {
    var ws = words(input.value), res = run(input.value);
    box.textContent = "";
    if (!ws.length) { close(); return; }
    if (!res.length) box.appendChild(el("p", "sr-empty", "Ничего не найдено: попробуйте другое слово."));
    res.forEach(function (r) {
      var e = r.e, a = el("a", "sr-item");
      a.href = e.c + "/course/step-" + e.s + ".html" + (e.a ? "#" + e.a : "");
      a.setAttribute("role", "option");
      var head = el("span", "sr-head");
      head.appendChild(el("strong", null, e.ct));
      head.appendChild(el("span", "sr-block", " · " + e.t + " · " + e.b));
      a.appendChild(head);
      a.appendChild(snippet(e.x, ws, Math.max(0, r.at)));
      box.appendChild(a);
    });
    box.hidden = false;
    input.setAttribute("aria-expanded", "true");
  }
  input.addEventListener("input", render);
  input.addEventListener("focus", function () { if (input.value) render(); });
  input.addEventListener("keydown", function (ev) {
    var items = [].slice.call(box.querySelectorAll(".sr-item"));
    if (ev.key === "Enter") { ev.preventDefault(); if (items[0]) location.href = items[0].href; }
    else if (ev.key === "ArrowDown" && items[0]) { ev.preventDefault(); items[0].focus(); }
    else if (ev.key === "Escape") { if (input.value) { input.value = ""; render(); } else input.blur(); }
  });
  box.addEventListener("keydown", function (ev) {
    var items = [].slice.call(box.querySelectorAll(".sr-item")), i = items.indexOf(document.activeElement);
    if (ev.key === "ArrowDown" && i < items.length - 1) { ev.preventDefault(); items[i + 1].focus(); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); if (i > 0) items[i - 1].focus(); else input.focus(); }
    else if (ev.key === "Escape") { close(); input.focus(); }
  });
  document.addEventListener("click", function (ev) { if (!box.contains(ev.target) && ev.target !== input) close(); });
  var openSearch = document.getElementById("open-search"), host = document.querySelector(".top");
  openSearch.addEventListener("click", function () {
    var on = !host.classList.contains("search-open");
    host.classList.toggle("search-open", on);
    openSearch.setAttribute("aria-expanded", String(on));
    if (on) input.focus();
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "/" || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    var t = ev.target, tag = t && t.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || (t && t.isContentEditable)) return;
    ev.preventDefault();
    if (getComputedStyle(openSearch).display !== "none") { host.classList.add("search-open"); openSearch.setAttribute("aria-expanded", "true"); }
    input.focus();
  });
})();
