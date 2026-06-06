#!/usr/bin/env python3
"""Generate the blog index page from all posts under content/blog/.

GWEB-55. NOT a build step: run manually after adding or editing a post, the
output (blog/index.html) is committed, GitHub Pages serves static HTML.

    python3 tools/render_blog.py

Layout mirrors the requested reference (LlamaIndex-style): a topics sidebar,
the newest post featured, the rest in a 3-column grid, and a paginator. Topic
filtering, the featured treatment, and pagination are all applied client-side
by js/blog.js — every post ships in the HTML for SEO and no-JS fallback.
"""
import datetime
import glob
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_post import parse_front_matter, SITE  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def human_date(iso):
    return datetime.datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %B %Y")


def load_posts():
    posts = []
    for md in glob.glob(os.path.join(REPO_ROOT, "content", "blog", "*", "post.md")):
        with open(md, encoding="utf-8") as fh:
            meta, _ = parse_front_matter(fh.read())
        posts.append(meta)
    posts.sort(key=lambda m: m["date"], reverse=True)
    return posts


def topic_list(posts):
    """Unique tags in newest-first order of first appearance."""
    seen = []
    for p in posts:
        for t in p["tags"]:
            if t not in seen:
                seen.append(t)
    return seen


def render_card(post):
    hero = post.get("hero", "/og_image_1200x630.png")
    data_tags = html.escape("|".join(post["tags"]))
    primary = html.escape(post["tags"][0]) if post["tags"] else ""
    return f'''        <li class="blog-card" data-tags="{data_tags}">
          <a href="/blog/{html.escape(post['slug'])}/">
            <img class="blog-card__media" src="{html.escape(hero)}" alt="" loading="lazy">
            <div class="blog-card__body">
              <span class="blog-card__meta">{html.escape(human_date(post['date']))} &middot; {primary}</span>
              <h3>{html.escape(post['title'])}</h3>
              <p>{html.escape(post['excerpt'])}</p>
            </div>
          </a>
        </li>'''


def render_topics(topics):
    items = ['          <li><button type="button" data-topic="all" class="active" aria-pressed="true">All</button></li>']
    for t in topics:
        items.append(
            f'          <li><button type="button" data-topic="{html.escape(t)}" '
            f'aria-pressed="false">{html.escape(t)}</button></li>'
        )
    return "\n".join(items)


def build_index(posts):
    cards = "\n".join(render_card(p) for p in posts)
    topics = render_topics(topic_list(posts))
    return TEMPLATE.format(cards=cards, topics=topics)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog | Granid</title>
  <meta name="description" content="Notes on on-premise AI, data sovereignty, and Swiss legal technology from the team building Granid.">
  <link rel="canonical" href="https://granid.ch/blog/">
  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon_dark.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="shortcut icon" href="/favicon.ico">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Granid">
  <meta property="og:title" content="Granid Blog">
  <meta property="og:description" content="Notes on on-premise AI, data sovereignty, and Swiss legal technology.">
  <meta property="og:url" content="https://granid.ch/blog/">
  <meta property="og:locale" content="en_CH">
  <meta property="og:image" content="https://granid.ch/og_image_1200x630.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Granid Edge Intelligence">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Granid Blog">
  <meta name="twitter:description" content="Notes on on-premise AI, data sovereignty, and Swiss legal technology.">
  <meta name="twitter:image" content="https://granid.ch/og_image_1200x630.png">

  <!-- Analytics: GoatCounter snippet (LEGALINT-216) to be wired here once the
       self-hosted instance is live. Intentionally omitted until then. -->

  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/geist-latin.woff2" crossorigin>
  <link rel="stylesheet" href="/css/fonts.css">
  <link rel="stylesheet" href="/css/granid-imports.css">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

  <nav>
    <div class="container">
      <a href="/" class="nav-logo"><img src="/assets/images/granid_logo_black_transparent.svg" alt="Granid"></a>
      <button class="nav-toggle" aria-label="Menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-links">
        <li class="has-submenu">
          <button class="submenu-trigger" type="button" aria-expanded="false" aria-haspopup="true">Products</button>
          <ul class="submenu">
            <li><a href="/">Legal Intelligence</a></li>
            <li><a href="/products/voice-intelligence/">Voice Intelligence</a></li>
            <li><a href="/products/meeting-intelligence/">Meeting Intelligence</a></li>
          </ul>
        </li>
        <li><a href="/#problem">Security</a></li>
        <li><a href="/#products">Plans</a></li>
        <li><a href="/hardware/production/">Hardware</a></li>
        <li><a href="/blog/" class="active">Blog</a></li>
        <li><a href="/contact-us/">Contact</a></li>
        <li class="nav-lang">
          <a href="/blog/" class="active">EN</a>
          <span class="lang-off" title="Available in English only">DE<span class="visually-hidden"> (available in English only)</span></span>
          <span class="lang-off" title="Available in English only">FR<span class="visually-hidden"> (available in English only)</span></span>
          <span class="lang-off" title="Available in English only">IT<span class="visually-hidden"> (available in English only)</span></span>
        </li>
        <li><a href="/trial/" class="btn btn--sm">Start your trial</a></li>
      </ul>
    </div>
  </nav>

  <section class="blog-index-head">
    <div class="container">
      <span class="eyebrow">Granid Blog</span>
      <h1>Notes from the office that never leaves.</h1>
      <p class="lede">On-premise AI, data sovereignty, and Swiss legal technology, written for the people responsible for keeping client data confidential.</p>
    </div>
  </section>

  <section class="blog-list">
    <div class="container blog-layout">
      <aside class="blog-sidebar">
        <h2>Topics</h2>
        <ul class="blog-topics">
{topics}
        </ul>
      </aside>

      <section class="blog-main" aria-labelledby="latest-heading">
        <h2 id="latest-heading" class="visually-hidden">Latest articles</h2>
        <ol class="blog-grid" data-blog-grid>
{cards}
          <li class="blog-empty" hidden>No articles in this topic yet.</li>
        </ol>
        <div class="blog-pager" data-blog-pager role="navigation" aria-label="Blog pagination"></div>
      </section>
    </div>
  </section>

  <footer>
    <div class="container">
      <div class="footer-left">Granid, Edge Intelligence. Switzerland.</div>
      <div class="footer-right">
        <a href="/blog/">Blog</a>
        <a href="/terms/">Terms &amp; Conditions</a>
        <a href="https://www.linkedin.com/company/granid" target="_blank" rel="noopener noreferrer">LinkedIn</a>
      </div>
    </div>
  </footer>

  <script src="/js/main.js"></script>
  <script src="/js/blog.js"></script>
</body>
</html>
"""


def main():
    posts = load_posts()
    if not posts:
        sys.exit("no posts found under content/blog/*/post.md")
    out = os.path.join(REPO_ROOT, "blog", "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build_index(posts))
    print(f"rendered: blog/index.html  ({len(posts)} posts, "
          f"{len(topic_list(posts))} topics)")


if __name__ == "__main__":
    main()
