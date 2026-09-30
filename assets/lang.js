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

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".lang-switch a");
    if (!a) return;
    try {
      localStorage.setItem("lang", a.getAttribute("data-lang"));
    } catch (err) {}
  });
})();
