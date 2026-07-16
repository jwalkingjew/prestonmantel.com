(function () {
  var root = document.documentElement;
  var toggle = document.querySelector('.theme-toggle');
  var metaTheme = document.querySelector('meta[name="theme-color"]');

  function systemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function activeTheme() {
    return root.dataset.theme || systemTheme();
  }

  function updateControl() {
    if (!toggle) return;
    var theme = activeTheme();
    toggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    toggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    if (metaTheme) metaTheme.setAttribute('content', theme === 'dark' ? '#151b22' : '#f3ede2');
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = activeTheme() === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      localStorage.setItem('theme', next);
      updateControl();
    });
  }

  var media = window.matchMedia('(prefers-color-scheme: dark)');
  media.addEventListener('change', function () {
    if (!root.dataset.theme) updateControl();
  });

  updateControl();
}());
