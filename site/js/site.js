(function () {
  var root = document.documentElement;
  var toggle = document.querySelector('.theme-toggle');
  var themeValue = document.querySelector('.theme-value');
  var metaTheme = document.querySelector('meta[name="theme-color"]');
  var header = document.querySelector('.site-header');
  var menu = document.querySelector('.header-menu');
  var menuToggle = document.querySelector('.menu-toggle');
  var menuLabel = document.querySelector('.menu-toggle-label');

  function activeTheme() {
    return root.dataset.theme || 'light';
  }

  function updateControl() {
    if (!toggle) return;
    var theme = activeTheme();
    toggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    toggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    if (themeValue) themeValue.textContent = theme === 'dark' ? 'Dark' : 'Light';
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

  function setMenu(open) {
    if (!header || !menuToggle) return;
    header.classList.toggle('menu-open', open);
    menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (menuLabel) menuLabel.textContent = open ? 'Close' : 'Menu';
  }

  if (menuToggle && menu) {
    menuToggle.addEventListener('click', function () {
      setMenu(menuToggle.getAttribute('aria-expanded') !== 'true');
    });

    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        setMenu(false);
      });
    });

    document.addEventListener('click', function (event) {
      if (header && !header.contains(event.target)) setMenu(false);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menuToggle.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 820) setMenu(false);
    });
  }

  function activateTab(tab, moveFocus) {
    var tabset = tab.closest('[data-tabset]');
    if (!tabset) return;
    var tabs = Array.from(tabset.querySelectorAll('[role="tab"]'));
    tabs.forEach(function (item) {
      var selected = item === tab;
      item.setAttribute('aria-selected', selected ? 'true' : 'false');
      item.tabIndex = selected ? 0 : -1;
      var panel = document.getElementById(item.getAttribute('aria-controls'));
      if (panel) panel.hidden = !selected;
    });
    if (moveFocus) tab.focus();
  }

  document.querySelectorAll('[data-tabset]').forEach(function (tabset) {
    var tabs = Array.from(tabset.querySelectorAll('[role="tab"]'));
    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () {
        activateTab(tab, false);
      });
      tab.addEventListener('keydown', function (event) {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        var direction = event.key === 'ArrowRight' ? 1 : -1;
        var next = tabs[(index + direction + tabs.length) % tabs.length];
        activateTab(next, true);
      });
    });
  });

  if (window.location.hash) {
    var target = document.querySelector(window.location.hash);
    var hiddenPanel = target && target.closest('.directory-panel[hidden]');
    if (hiddenPanel) {
      var controllingTab = document.querySelector('[aria-controls="' + hiddenPanel.id + '"]');
      if (controllingTab) activateTab(controllingTab, false);
    }
  }

  updateControl();
}());
