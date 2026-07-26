/**
 * Site-wide R-18 age gate (shared localStorage key).
 * Include on every public page: <script src="js/age-gate.js" defer></script>
 */
(function () {
  var KEY = "doujin_lab_age_ok";

  function alreadyOk() {
    try {
      return localStorage.getItem(KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function markOk() {
    try {
      localStorage.setItem(KEY, "1");
    } catch (e) {}
  }

  function removeGate(el) {
    if (el && el.parentNode) el.parentNode.removeChild(el);
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
  }

  function showGate() {
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";

    var root = document.createElement("div");
    root.id = "agegate";
    root.className = "agegate";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", "年齢確認");
    // inline styles so gate works even if CSS fails to load
    root.setAttribute(
      "style",
      "position:fixed;inset:0;z-index:2147483646;display:flex;" +
        "align-items:center;justify-content:center;padding:1.5rem;" +
        "background:rgba(15,15,18,0.98);box-sizing:border-box;"
    );
    root.innerHTML =
      '<div class="box" style="max-width:420px;width:100%;background:#22222e;' +
      "border:1px solid #333344;border-radius:16px;padding:1.75rem 1.4rem;" +
      'text-align:center;color:#f2f2f5;font-family:sans-serif;">' +
      '<p class="badge" style="display:inline-block;border:1px solid #555;' +
      'padding:0.15rem 0.5rem;border-radius:999px;color:#aaa;font-size:0.75rem;">R-18</p>' +
      '<h1 style="font-size:1.25rem;margin:0.75rem 0;">18歳未満は閲覧できません</h1>' +
      '<p class="muted" style="color:#a0a0b0;font-size:0.95rem;line-height:1.6;">' +
      "成人向け同人のレビュー・アフィリエイト紹介サイトです。" +
      "各国の法令を守り、自己責任でご利用ください。</p>" +
      '<div class="btns" style="display:flex;gap:0.6rem;margin-top:1.2rem;">' +
      '<button type="button" class="btn-yes" id="age-yes" style="flex:1;border:0;' +
      "border-radius:10px;padding:0.85rem;font-weight:700;cursor:pointer;" +
      'font-size:1rem;background:#ff2d55;color:#fff;">18歳以上である</button>' +
      '<a class="btn-no" href="https://www.google.com/" style="flex:1;border-radius:10px;' +
      "padding:0.85rem;font-weight:700;background:#333;color:#ccc;text-decoration:none;" +
      'display:flex;align-items:center;justify-content:center;">退出</a>' +
      "</div></div>";

    // insert as first child so it sits above content in DOM order too
    if (document.body.firstChild) {
      document.body.insertBefore(root, document.body.firstChild);
    } else {
      document.body.appendChild(root);
    }

    var btn = document.getElementById("age-yes");
    if (btn) {
      btn.addEventListener("click", function () {
        markOk();
        removeGate(root);
      });
    }
  }

  function run() {
    // ?age=reset で確認用にゲートを強制表示
    try {
      var q = new URLSearchParams(window.location.search || "");
      if (q.get("age") === "reset") {
        localStorage.removeItem(KEY);
      }
    } catch (e) {}

    if (alreadyOk()) return;
    showGate();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();

