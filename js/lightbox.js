// Granid — lightbox.js (GWEB-101)
// Click-to-zoom for article figures. Progressive enhancement over the plain
// .figure-zoom anchor: without JS, and on small screens (where the browser's
// native image view gives pinch zoom and a back gesture), the link simply
// opens the full-size file.

document.addEventListener('DOMContentLoaded', () => {
  const zoomLinks = document.querySelectorAll('.article-figure a.figure-zoom');
  if (!zoomLinks.length) return;

  let overlay = null;
  let img = null;
  let caption = null;
  let closeBtn = null;
  let lastTrigger = null;

  const close = () => {
    overlay.hidden = true;
    document.body.classList.remove('lightbox-open');
    if (lastTrigger) lastTrigger.focus();
  };

  const build = () => {
    overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.hidden = true;
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');

    // The visible caption carries the description, so the overlay image
    // itself stays decorative (empty alt) to avoid double announcements.
    img = document.createElement('img');
    img.alt = '';
    caption = document.createElement('p');
    caption.className = 'lightbox-caption';
    closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'lightbox-close';
    closeBtn.setAttribute('aria-label', 'Close full-size image');
    closeBtn.textContent = '×';

    overlay.append(closeBtn, img, caption);
    document.body.appendChild(overlay);

    // A click anywhere in the overlay closes it; so does Escape. The close
    // button is the dialog's only focusable element, so keep Tab on it.
    overlay.addEventListener('click', close);
    closeBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') e.preventDefault();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !overlay.hidden) close();
    });
  };

  zoomLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      if (window.matchMedia('(max-width: 768px)').matches) return;
      e.preventDefault();
      if (!overlay) build();
      const source = link.querySelector('img');
      const alt = source ? source.alt : '';
      img.src = link.href;
      caption.textContent = alt;
      overlay.setAttribute('aria-label', alt || 'Full-size image');
      overlay.hidden = false;
      document.body.classList.add('lightbox-open');
      lastTrigger = link;
      closeBtn.focus();
    });
  });
});
