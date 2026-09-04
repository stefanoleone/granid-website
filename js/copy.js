// Granid — copy.js (GWEB-101)
// Adds a Copy button to prompt blocks (.article-body pre.wrap). The buttons
// are injected here so that without JS the blocks stay plain selectable
// text; requires the async clipboard API (secure contexts only).

document.addEventListener('DOMContentLoaded', () => {
  if (!navigator.clipboard || !navigator.clipboard.writeText) return;
  const blocks = document.querySelectorAll('.article-body pre.wrap');
  if (!blocks.length) return;

  // Polite live region: some screen readers do not re-announce the focused
  // button when its label flips to "Copied", so confirm here as well.
  const status = document.createElement('div');
  status.className = 'visually-hidden';
  status.setAttribute('role', 'status');
  document.body.appendChild(status);
  const announce = (text) => {
    status.textContent = '';
    setTimeout(() => { status.textContent = text; }, 50);
  };

  blocks.forEach((pre) => {
    const code = pre.querySelector('code');
    if (!code) return;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pre-copy';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy prompt to clipboard');

    btn.addEventListener('click', () => {
      navigator.clipboard.writeText(code.textContent.trim()).then(() => {
        btn.textContent = 'Copied';
        btn.classList.add('is-done');
        announce('Prompt copied to clipboard.');
      }).catch(() => {
        btn.textContent = 'Copy failed';
        announce('Copy failed. Select the text to copy it.');
      });
      setTimeout(() => {
        btn.textContent = 'Copy';
        btn.classList.remove('is-done');
      }, 2000);
    });

    pre.classList.add('has-copy');
    pre.appendChild(btn);
  });
});
