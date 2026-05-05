(function () {
  var STORAGE_KEY = 'ace-theme';
  var DEFAULT = 'dark';

  function current() {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT;
  }

  function apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    // Sync Just the Docs' own chrome (sidebar, header, etc.)
    if (typeof jtd !== 'undefined' && jtd.setTheme) {
      jtd.setTheme(theme);
    }
  }

  function makeButton() {
    var btn = document.createElement('button');
    btn.id = 'theme-toggle';

    function update(theme) {
      btn.textContent = theme === 'dark' ? '☀' : '☾';
      btn.setAttribute('aria-label',
        theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      btn.title = btn.getAttribute('aria-label');
    }

    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      apply(next);
      update(next);
    });

    update(current());
    return btn;
  }

  document.addEventListener('DOMContentLoaded', function () {
    apply(current());

    var btn = makeButton();
    // Inject into Just the Docs' aux nav (top right), falling back up the tree
    var target = document.querySelector('.aux-nav') ||
                 document.querySelector('.main-header') ||
                 document.querySelector('.site-header');
    if (target) {
      target.appendChild(btn);
    }
  });
})();
