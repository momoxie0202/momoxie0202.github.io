// 主題切換：auto（跟隨系統，預設）/ light / dark，選擇記在 localStorage。
// 讀取與套用的部分在各頁 <head> 內同步執行，避免載入時閃一下白底。
(function () {
  var root = document.documentElement;
  var darkQuery = window.matchMedia("(prefers-color-scheme: dark)");

  function currentMode() {
    var mode = root.getAttribute("data-theme");
    return mode === "light" || mode === "dark" ? mode : "auto";
  }

  function effectiveColor() {
    var mode = currentMode();
    var dark = mode === "dark" || (mode === "auto" && darkQuery.matches);
    return dark ? "#121212" : "#ffffff";
  }

  // 手動模式時，瀏覽器工具列顏色不能再交給 media query 判斷
  function syncThemeColor() {
    var tags = document.querySelectorAll('meta[name="theme-color"]');
    var manual = currentMode() !== "auto";
    for (var i = 0; i < tags.length; i++) {
      if (manual) {
        tags[i].removeAttribute("media");
        tags[i].setAttribute("content", effectiveColor());
      } else {
        tags[i].setAttribute("media", tags[i].dataset.media);
        tags[i].setAttribute("content", tags[i].dataset.content);
      }
    }
  }

  function apply(mode) {
    if (mode === "auto") {
      root.removeAttribute("data-theme");
      try {
        localStorage.removeItem("theme");
      } catch (e) {}
    } else {
      root.setAttribute("data-theme", mode);
      try {
        localStorage.setItem("theme", mode);
      } catch (e) {}
    }
    syncThemeColor();
    render();
  }

  var buttons = [];

  function render() {
    var mode = currentMode();
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute(
        "aria-pressed",
        String(buttons[i].getAttribute("data-mode") === mode)
      );
    }
  }

  function init() {
    var tags = document.querySelectorAll('meta[name="theme-color"]');
    for (var i = 0; i < tags.length; i++) {
      tags[i].dataset.media = tags[i].getAttribute("media") || "";
      tags[i].dataset.content = tags[i].getAttribute("content") || "";
    }

    var container = document.querySelector(".theme-switch .group");
    if (container) {
      buttons = Array.prototype.slice.call(container.querySelectorAll("button"));
      for (var j = 0; j < buttons.length; j++) {
        buttons[j].addEventListener("click", function () {
          apply(this.getAttribute("data-mode"));
        });
      }
      render();
    }

    // auto 模式下系統主題變動時，同步工具列顏色
    var onChange = function () {
      if (currentMode() === "auto") syncThemeColor();
    };
    if (darkQuery.addEventListener) {
      darkQuery.addEventListener("change", onChange);
    } else if (darkQuery.addListener) {
      darkQuery.addListener(onChange);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
