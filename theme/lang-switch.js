(function () {
  'use strict';

  var LANGS = [
    { code: 'en', label: 'English', prefix: '/SkillDesignBook/' },
    { code: 'zh', label: '中文',    prefix: '/SkillDesignBook/zh/' }
  ];

  function currentLang() {
    var path = window.location.pathname;
    if (path.indexOf('/SkillDesignBook/zh/') === 0 || path.indexOf('/SkillDesignBook/zh') === 0) {
      return 'zh';
    }
    return 'en';
  }

  function pageSuffix() {
    var path = window.location.pathname;
    var lang = currentLang();
    var prefix = lang === 'zh'
      ? '/SkillDesignBook/zh/'
      : '/SkillDesignBook/';
    var suffix = path.replace(prefix, '');
    return suffix || 'index.html';
  }

  function switchUrl(targetCode) {
    var target = LANGS.find(function (l) { return l.code === targetCode; });
    if (!target) return '#';
    return target.prefix + pageSuffix();
  }

  function createSwitcher() {
    var lang = currentLang();
    var other = lang === 'en' ? 'zh' : 'en';
    var otherLang = LANGS.find(function (l) { return l.code === other; });

    var btn = document.createElement('a');
    btn.href = switchUrl(other);
    btn.className = 'lang-switch-btn';
    btn.title = otherLang.label;
    btn.textContent = otherLang.label;

    btn.setAttribute('style', [
      'display: inline-flex',
      'align-items: center',
      'padding: 4px 12px',
      'border: 1px solid var(--sidebar-fg)',
      'border-radius: 4px',
      'font-size: 0.85em',
      'color: var(--sidebar-fg)',
      'text-decoration: none',
      'margin-left: 8px',
      'cursor: pointer',
      'transition: background 0.15s ease'
    ].join(';'));

    btn.addEventListener('mouseenter', function () {
      btn.style.background = 'var(--sidebar-active)';
    });
    btn.addEventListener('mouseleave', function () {
      btn.style.background = 'transparent';
    });

    return btn;
  }

  function inject() {
    var iconLinks = document.querySelector('.right-buttons');
    if (iconLinks) {
      iconLinks.prepend(createSwitcher());
      return;
    }

    var menuBar = document.querySelector('.menu-bar');
    if (menuBar) {
      menuBar.appendChild(createSwitcher());
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
