/* Курс открывается из файла: без сети, без fetch, данные — во встроенных <script type="application/json">. */
(function () {
  "use strict";
  var ch = document.body.dataset.ch;
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
  var K = { done: "course:" + ch + ":done", last: "course:" + ch + ":last", cards: "course:" + ch + ":cards",
            theme: "course:theme", by: "course:by" };

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

  /* ---------- тема ---------- */
  var root = document.documentElement;
  var stored = store.get(K.theme, null);
  var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = stored || (dark ? "dark" : "light");
  var tbtn = document.getElementById("toggle-theme");
  if (tbtn) tbtn.addEventListener("click", function () {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    store.set(K.theme, root.dataset.theme);
  });

  /* ---------- автор / модель ---------- */
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

  var done = store.get(K.done, []);
  function isDone(id) { return done.indexOf(id) >= 0; }
  function setDone(id, on) {
    done = done.filter(function (x) { return x !== id; });
    if (on) done.push(id);
    store.set(K.done, done);
  }

  /* ---------- страница шага ---------- */
  var stepData = readJSON("step-data");
  if (stepData) {
    var nodeId = stepData.node_id;
    store.set(K.last, nodeId);

    var mbtn = document.getElementById("mark-done");
    function showDone() { mbtn.setAttribute("aria-pressed", isDone(nodeId) ? "true" : "false"); }
    mbtn.addEventListener("click", function () { setDone(nodeId, !isDone(nodeId)); showDone(); });
    showDone();
    var next = document.querySelector('a[rel="next"]');
    if (next) next.addEventListener("click", function () { setDone(nodeId, true); });

    /* «проверь по книге» */
    var dlg = document.getElementById("book");
    var body = document.getElementById("book-body");
    var VSTAT = {
      ok: "Проверка: замечаний к утверждению нет",
      not_checked: "Проверка ещё не запускалась",
      remark: "Замечание проверки"
    };
    function claimBlock(id) {
      var c = stepData.claims[id];
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
      var s = el("p", "vstat " + v.status, VSTAT[v.status] + (v.status === "remark" ? " (" + v.severity + "): " + v.problem : ""));
      box.appendChild(s);
      return box;
    }
    function scanBlock(p) {
      var info = stepData.pages[String(p)];
      if (info && info.scan) {
        var img = el("img", "scan");
        img.src = info.scan;
        img.alt = "Скан страницы " + p + " книги";
        return img;
      }
      return el("p", "muted", "Скан страницы " + p + " в курс не добавлен.");
    }
    function openBook(claimId, pageNo) {
      body.textContent = "";
      var p = pageNo;
      if (claimId) {
        body.appendChild(claimBlock(claimId));
        p = stepData.claims[claimId].page;
      } else {
        var ids = (stepData.pages[String(p)] || { claim_ids: [] }).claim_ids;
        if (!ids.length) body.appendChild(el("p", "muted", "На этой странице у шага нет утверждений с цитатой."));
        ids.forEach(function (id) { body.appendChild(claimBlock(id)); });
      }
      body.appendChild(scanBlock(p));
      dlg.showModal();
    }
    document.addEventListener("click", function (ev) {
      var b = ev.target.closest(".pg");
      if (!b) return;
      openBook(b.dataset.claim || null, b.dataset.page ? Number(b.dataset.page) : null);
    });
    dlg.addEventListener("click", function (ev) { if (ev.target === dlg) dlg.close(); });
  }

  /* ---------- путь ---------- */
  var steps = readJSON("steps-data");
  if (steps) {
    var n = 0;
    document.querySelectorAll(".steps-list li").forEach(function (li) {
      if (isDone(li.dataset.node)) { li.classList.add("done"); n++; }
    });
    document.getElementById("progress-bar").style.width = Math.round(100 * n / steps.length) + "%";
    document.getElementById("progress-text").textContent = "Пройдено " + n + " из " + steps.length;
    var last = store.get(K.last, null);
    var lastStep = steps.filter(function (s) { return s.id === last; })[0];
    if (lastStep) {
      var r = document.getElementById("resume");
      r.href = "step-" + lastStep.id + ".html";
      r.querySelector("span").textContent = "Продолжить: " + lastStep.title;
      var li = document.querySelector('.steps-list li[data-node="' + lastStep.id + '"]');
      if (li) li.classList.add("last");
    }
  }

  /* ---------- карточки ---------- */
  if (page === "cards") {
    var marks = store.get(K.cards, {});
    function paint(card) {
      var m = marks[card.dataset.node];
      card.classList.toggle("mark-know", m === "know");
      card.classList.toggle("mark-repeat", m === "repeat");
      card.querySelectorAll("[data-mark]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.mark === m ? "true" : "false"); });
    }
    document.querySelectorAll(".card").forEach(function (card) {
      paint(card);
      card.querySelectorAll("[data-mark]").forEach(function (b) {
        b.addEventListener("click", function () {
          marks[card.dataset.node] = b.dataset.mark; store.set(K.cards, marks); paint(card);
        });
      });
    });
    var only = document.getElementById("only-repeat");
    only.addEventListener("change", function () { document.body.classList.toggle("only-repeat", only.checked); });
  }

  /* ---------- карта ---------- */
  if (page === "map") {
    document.querySelectorAll(".map-node").forEach(function (a) { if (isDone(a.dataset.node)) a.classList.add("done"); });
  }
})();
