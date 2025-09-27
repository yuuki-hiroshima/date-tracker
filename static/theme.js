
(() => {
  const KEY = 'theme';
  const root = document.documentElement;
  const btn = document.getElementById('theme-toggle');

  // 初期適用（localStorage優先、なければ base.html 側の即時JSでOS準拠が効いている想定）
  function currentIsDark() {
    return root.getAttribute('data-theme') === 'dark';
  }

  // ボタンの表示を現在状態に合わせる関数
  function updateLabel() {
    if (!btn) return;
    const isDark = currentIsDark();
    btn.textContent = isDark ? '☀️ ライト' : '🌙 ダーク';
    btn.setAttribute('aria-pressed', String(isDark));
    btn.setAttribute('aria-label', isDark ? 'ライトモードに切り替え' : 'ダークモードに切り替え');
  }
  // 初期ラベル反映
  updateLabel();

  // クリックで切替 + 保存 + ラベル更新
  if (btn) {
    btn.addEventListener('click' , () => {
      if (currentIsDark()) {
        root.removeAttribute('data-theme');
        localStorage.setItem(KEY, 'light');
      } else {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem(KEY, 'dark');
      }
      updateLabel();
    });
  }

  // --- 任意: OSのテーマ変更を監視（localStorage 未設定時のみ追従したい場合）
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  function syncToOS(e) {
    if (localStorage.getItem(KEY)) return;    // ユーザーが一度でも明示選択していたら追従しない
    if (e.matches) root.setAttribute('data-theme', 'dark');
    else root.removeAttribute('data-theme');
    updateLabel();
  }
  if (media.addEventListener) media.addEventListener('change', syncToOS);
  else media.addListener(syncToOS);   // 旧ブラウザ互換
})();