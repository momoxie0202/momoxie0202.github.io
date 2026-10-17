(function () {
  var menu = document.querySelector(".lang-menu");
  var current = document.documentElement.lang.toLowerCase().slice(0, 2);
  var pages = {
    zh: { url: "/apps/undercover/", text: "這個頁面有繁體中文版" },
    en: { url: "/apps/undercover/en/", text: "This page is available in English" },
    vi: { url: "/apps/undercover/vi/", text: "Trang này có bản tiếng Việt" }
  };

  document.addEventListener("click", function (event) {
    if (menu && !menu.contains(event.target)) menu.open = false;
  });

  var wanted = (navigator.language || "").toLowerCase().slice(0, 2);
  if (!pages[wanted] || wanted === current) return;
  try { if (localStorage.getItem("undercover_lang_dismiss")) return; } catch (e) {}

  var box = document.getElementById("lang-suggest");
  if (!box) return;
  var page = pages[wanted];
  var link = document.createElement("a");
  link.href = page.url;
  link.lang = wanted === "zh" ? "zh-Hant" : wanted;
  link.hreflang = link.lang;
  link.textContent = page.text + " →";
  var close = document.createElement("button");
  close.type = "button";
  close.setAttribute("aria-label", "Close language suggestion");
  close.textContent = "×";
  close.addEventListener("click", function () {
    box.classList.remove("show");
    try { localStorage.setItem("undercover_lang_dismiss", "1"); } catch (e) {}
  });
  box.appendChild(link);
  box.appendChild(close);
  box.classList.add("show");
})();
