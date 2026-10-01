// 語言：網址錨點 > 上次選擇 > 裝置語言。
// 以同步 script 放在 <head>，在繪製前決定，避免閃一下另一種語言。
(function () {
  var root = document.documentElement;
  root.className += " js";

  function fromHash() {
    var h = location.hash;
    if (/^#en/.test(h)) return "en";
    if (h.length > 1) return "zh";
    return null;
  }

  function saved() {
    try {
      var s = localStorage.getItem("lang");
      return s === "en" || s === "zh" ? s : null;
    } catch (e) {
      return null;
    }
  }

  function device() {
    var l = (navigator.languages && navigator.languages[0]) || navigator.language || "";
    return /^zh/i.test(l) ? "zh" : "en";
  }

  function apply(lang) {
    root.setAttribute("data-lang", lang);
    root.lang = lang === "en" ? "en" : "zh-Hant";
  }

  apply(fromHash() || saved() || device());

  window.addEventListener("hashchange", function () {
    var lang = fromHash();
    if (lang) apply(lang);
  });

  // 切換語言時停在對應段落（例如中文「使用條款」→ 英文 Terms），不跳回頁首
  function counterpartId(lang) {
    var block = document.querySelector('main[data-block="' + (lang === "en" ? "zh" : "en") + '"]');
    if (!block) return null;
    var current = null;
    var heads = block.querySelectorAll("h2[id]");
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top <= 80) current = heads[i].id;
    }
    if (!current) return null;
    return lang === "en" ? "en-" + current : current.replace(/^en-/, "");
  }

  function closeMenus(except) {
    var menus = document.querySelectorAll(".lang-menu[open]");
    for (var i = 0; i < menus.length; i++) {
      if (menus[i] !== except) menus[i].removeAttribute("open");
    }
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-set-lang]");
    if (a) {
      e.preventDefault();
      var lang = a.getAttribute("data-set-lang");
      var target = counterpartId(lang);
      try {
        localStorage.setItem("lang", lang);
      } catch (err) {}
      apply(lang);
      closeMenus(null);
      var el = target && document.getElementById(target);
      if (el) {
        el.scrollIntoView({ block: "start" });
      } else {
        window.scrollTo(0, 0);
      }
      history.replaceState(null, "", "#" + (target || lang));
      return;
    }
    var menu = e.target.closest && e.target.closest(".lang-menu");
    closeMenus(menu);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenus(null);
  });
})();
