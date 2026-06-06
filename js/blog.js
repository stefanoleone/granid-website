// Granid — blog.js (GWEB-55)
// Client-side topic filtering + pagination for the blog index. No build step,
// no network calls: every post is already in the DOM (good for SEO and no-JS
// fallback). This script only shows/hides cards and styles the first visible
// card of page 1 as the featured post.

document.addEventListener('DOMContentLoaded', () => {
  const grid = document.querySelector('[data-blog-grid]');
  if (!grid) return;

  const ITEMS_PER_PAGE = 4; // featured + 3 on page 1; tune as the blog grows
  const cards = Array.from(grid.querySelectorAll('.blog-card')); // DOM order = newest first
  const topicButtons = Array.from(document.querySelectorAll('.blog-topics button'));
  const pager = document.querySelector('[data-blog-pager]');
  const empty = document.querySelector('.blog-empty');

  let topic = 'all';
  let page = 1;

  const matches = (card) =>
    topic === 'all' ||
    (card.dataset.tags || '').split('|').indexOf(topic) !== -1;

  function render() {
    const filtered = cards.filter(matches);
    const totalPages = Math.max(1, Math.ceil(filtered.length / ITEMS_PER_PAGE));
    if (page > totalPages) page = totalPages;

    cards.forEach((c) => { c.hidden = true; c.classList.remove('is-featured'); });

    const start = (page - 1) * ITEMS_PER_PAGE;
    filtered.slice(start, start + ITEMS_PER_PAGE).forEach((card, i) => {
      card.hidden = false;
      // Featured treatment only in the unfiltered "All" view, on page 1.
      if (topic === 'all' && page === 1 && i === 0) card.classList.add('is-featured');
    });

    if (empty) empty.hidden = filtered.length !== 0;
    renderPager(totalPages);
  }

  function renderPager(totalPages) {
    if (!pager) return;
    pager.innerHTML = '';
    if (totalPages <= 1) { pager.hidden = true; return; }
    pager.hidden = false;

    const addBtn = (label, targetPage, opts = {}) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      if (opts.ariaLabel) b.setAttribute('aria-label', opts.ariaLabel);
      if (opts.disabled) b.disabled = true;
      if (opts.active) { b.classList.add('active'); b.setAttribute('aria-current', 'page'); }
      b.addEventListener('click', () => {
        page = targetPage;
        render();
        grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      pager.appendChild(b);
    };

    addBtn('‹', page - 1, { ariaLabel: 'Previous page', disabled: page === 1 });
    for (let p = 1; p <= totalPages; p++) {
      addBtn(String(p), p, { active: p === page, ariaLabel: 'Page ' + p });
    }
    addBtn('›', page + 1, { ariaLabel: 'Next page', disabled: page === totalPages });
  }

  topicButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      topic = btn.dataset.topic;
      page = 1;
      topicButtons.forEach((b) => {
        const on = b === btn;
        b.classList.toggle('active', on);
        b.setAttribute('aria-pressed', String(on));
      });
      render();
    });
  });

  render();
});
