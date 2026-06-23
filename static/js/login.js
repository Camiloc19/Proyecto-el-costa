/* ============================================================
   Taller El Costa — Login (grúa)
   - Engranaje dorado (mismo algoritmo de siempre)
   - Intro GSAP: la grúa entra, pasa el centro y revela el login
   - Intro 1 vez por sesión (sessionStorage), botón "Saltar intro",
     respeta prefers-reduced-motion y se salta si hay error/éxito.
   - Micro-interacción: botón "Ingresar" con estado "cargando".
   - Si no hay GSAP, el login queda visible y funcional (fallback).
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Engranaje dorado ---------- */
  const f = n => n.toFixed(3);
  function buildGear(cx, cy, n, rOut, rRoot, rInner) {
    const step = (2 * Math.PI) / n, th = step * 0.20, ch = 1.20;
    const px = (r, a) => cx + r * Math.cos(a);
    const py = (r, a) => cy + r * Math.sin(a);
    let d = '';
    for (let i = 0; i < n; i++) {
      const a = i * step - Math.PI / 2;
      const aRL = a - th * ch, aTL = a - th * 0.78, aTR = a + th * 0.78, aRR = a + th * ch;
      d += `${i === 0 ? 'M' : 'L'} ${f(px(rRoot, aRL))} ${f(py(rRoot, aRL))} `;
      d += `L ${f(px(rOut, aTL))} ${f(py(rOut, aTL))} L ${f(px(rOut, aTR))} ${f(py(rOut, aTR))} `;
      d += `L ${f(px(rRoot, aRR))} ${f(py(rRoot, aRR))} `;
      const next = (i + 1) * step - Math.PI / 2 - th * ch;
      d += `A ${rRoot} ${rRoot} 0 0 1 ${f(px(rRoot, next))} ${f(py(rRoot, next))} `;
    }
    d += `Z M ${f(cx + rInner)} ${f(cy)} A ${rInner} ${rInner} 0 1 0 ${f(cx - rInner)} ${f(cy)} A ${rInner} ${rInner} 0 1 0 ${f(cx + rInner)} ${f(cy)} Z`;
    return d;
  }
  const gearPath = document.getElementById('gearPath');
  if (gearPath) gearPath.setAttribute('d', buildGear(210, 210, 26, 208, 180, 142));

  const html    = document.documentElement;
  const skipBtn = document.getElementById('skipIntro');
  const car     = document.querySelector('.car');

  /* La clase .intro la pone el <head> solo si toca reproducir intro
     (no vista previa esta sesión, sin reduce-motion y sin error/éxito). */
  const shouldPlay = html.classList.contains('intro') && !!window.gsap;

  if (!shouldPlay) {
    html.classList.remove('intro');          // #reveal visible por CSS
    if (skipBtn) skipBtn.hidden = true;
    if (car) car.style.opacity = 0;
  } else {
    const gsap = window.gsap;
    let done = false;
    function markPlayed() {
      if (done) return; done = true;
      try { sessionStorage.setItem('introPlayed', '1'); } catch (e) {}
      if (skipBtn) skipBtn.hidden = true;
    }

    const stagger = gsap.utils.toArray('.stagger');

    // Estados iniciales (todo con transform/opacity)
    gsap.set('.gear-wrap', { opacity: 0, scale: 0.62, transformOrigin: '50% 50%' });
    gsap.set('.glow',      { opacity: 0, scale: 0.4,  transformOrigin: '50% 50%' });
    gsap.set('.sweep',     { opacity: 0, x: -180, skewX: -16 });
    gsap.set(stagger,      { opacity: 0, y: 18 });

    const tl = gsap.timeline({ onComplete: markPlayed });
    // 1) Resplandor crece + 2) el engranaje entra con escala
    tl.to('.glow',      { opacity: 1, scale: 1, duration: 0.9, ease: 'power2.out' }, 0)
      .to('.gear-wrap', { opacity: 1, scale: 1, duration: 1.1, ease: 'power3.out' }, 0.1)
      // 3) Pasada de luz dorada cruzando
      .to('.sweep',     { x: 560, opacity: 0.85, duration: 0.95, ease: 'power2.inOut' }, 0.55)
      .to('.sweep',     { opacity: 0, duration: 0.25 }, '>-0.15')
      // 4) Título → campos → botón → enlace, en cascada
      .to(stagger,      { opacity: 1, y: 0, duration: 0.6, stagger: 0.12, ease: 'power3.out' }, 0.85);

    if (skipBtn) {
      skipBtn.addEventListener('click', function () {
        tl.progress(1);   // salta al final al instante
        markPlayed();
      });
    }
  }

  /* ---------- Micro-interacción: estado "cargando" del botón ---------- */
  const form = document.querySelector('form[action$="/login"], form[method="POST"]');
  const btn  = document.querySelector('.login-btn');
  if (form && btn) {
    form.addEventListener('submit', function () {
      // El form hace su POST normal; solo mostramos el spinner y evitamos doble envío.
      btn.classList.add('loading');
    });
  }
})();
