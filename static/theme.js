
(() => {
  const KEY = 'theme';
  const root = document.documentElement;

  // 起動時：保存テーマを適用
  const saved = localStorage.getItem(KEY);
  if (saved === 'dark') {
    root.setAttribute('data-theme', 'dark');
  } else if (saved === 'light') {
    root.removeAttribute('data-theme');
  }

  // トグルボタンを先に取得
  const btn = document.getElementById('theme-toggle');

  // ボタンの表示を現在状態に合わせる関数
  function updateLabel() {
    if (!btn) return;
    const isDark = root.getAttribute('data-theme') === 'dark';
    btn.textContent = isDark ? '☀️ ライト' : '🌙 ダーク';
    btn.setAttribute('aria-pressed', String(isDark));
  }

  // 初期ラベル反映
  updateLabel();

  // クリックで切替 + 保存 + ラベル更新
  if (btn) {
    btn.addEventListener('click', () => {
        const isDark = root.getAttribute('data-theme') === 'dark';
        if (isDark) {
            root.removeAttribute('data-theme');
            localStorage.setItem(KEY, 'light');
        } else {
            root.setAttribute('data-theme', 'dark');
            localStorage.setItem(KEY, 'dark');
        }
      updateLabel();
    });
  }
})();