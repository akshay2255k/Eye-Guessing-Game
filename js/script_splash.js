(() => {
  const bar = document.getElementById('progressBar');
  const percent = document.getElementById('percent');
  const timer = document.getElementById('timer');
  const orb = document.getElementById('cursorOrb');
  const splash = document.getElementById('splash');

  // 8 seconds
  const duration = 8000;
  const start = performance.now();

  let completed = false;

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);

    const eased = 1 - Math.pow(1 - progress, 1.8);

    // Progress bar
    bar.style.width = `${eased * 100}%`;

    // Percentage
    percent.textContent = `${String(
      Math.round(eased * 100)
    ).padStart(2, '0')}%`;

    // Timer
    timer.textContent = Math.max(
      0,
      8 - progress * 8
    ).toFixed(2).padStart(5, '0');

    if (progress < 1) {
      requestAnimationFrame(tick);
    } else if (!completed) {
      completed = true;

      // Show completed state
      splash.classList.add('complete');

      document.querySelector('.status').innerHTML =
        '<b></b> READY';

      // After 8 seconds go to templates/home.html
      window.location.href = 'templates/home.html';
    }
  }

  requestAnimationFrame(tick);

  // Custom cursor
  window.addEventListener('pointermove', (e) => {
    orb.style.left = `${e.clientX}px`;
    orb.style.top = `${e.clientY}px`;
  });

  // Cursor click animation
  splash.addEventListener('pointerdown', () => {
    orb.style.transform =
      'translate(-50%,-50%) scale(1.8)';

    setTimeout(() => {
      orb.style.transform =
        'translate(-50%,-50%) scale(1)';
    }, 220);
  });
})();