const UI = {
  fr: { copy: 'Copier', copied: 'Copié', close: 'Fermer' },
  en: { copy: 'Copy', copied: 'Copied', close: 'Close' },
};
const L = UI[document.documentElement.lang] || UI.en;
const burger = document.querySelector('.burger');
const links = [...document.querySelectorAll('.nav a')].map(a => [a.textContent, a.getAttribute('href')]);
burger.addEventListener('click', () => {
  const overlay = document.createElement('div'); overlay.className = 'drawer-overlay';
  const drawer = document.createElement('nav'); drawer.className = 'drawer';
  drawer.innerHTML = '<div class="drawer-head"><span class="wordmark">theogalh<span class="dot"></span></span><button class="btn btn-ghost btn-sm">' + L.close + '</button></div>'
    + links.map(([t, h]) => `<a href="${h}">${t}</a>`).join('');
  const close = () => { overlay.remove(); drawer.remove(); burger.setAttribute('aria-expanded', 'false'); };
  overlay.addEventListener('click', close);
  drawer.querySelector('button').addEventListener('click', close);
  drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  document.body.append(overlay, drawer);
  burger.setAttribute('aria-expanded', 'true');
});
document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', () => {
  navigator.clipboard.writeText(b.closest('.code-block').querySelector('code').innerText);
  b.textContent = L.copied; setTimeout(() => b.textContent = L.copy, 1200);
}));
