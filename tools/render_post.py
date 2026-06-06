#!/usr/bin/env python3
"""Render a Markdown blog post into a static, LinkedIn-shareable HTML page.

GWEB-55. This is NOT a build step: it is run manually on the author's machine,
its output is committed, and GitHub Pages serves the resulting pure HTML.

    python3 tools/render_post.py content/blog/<slug>/post.md

The rendered page lands at  blog/<slug>/index.html  (slug from front-matter).

Why a script and not hand-templated HTML: every post needs ~70 lines of head
boilerplate (favicons, Open Graph, Twitter, JSON-LD BlogPosting). Hand-copying
that per post guarantees drift in the sharing metadata that LinkedIn reads.
The renderer makes the metadata correct by construction.

Security: all front-matter values are HTML-escaped before they reach <meta>
content or the page body; JSON-LD is produced with json.dumps; the Markdown
subset is a fixed allowlist with NO raw-HTML passthrough.

Supported front-matter (between the leading '---' fences):
    title:     (required) post title
    slug:      (required) URL slug -> /blog/<slug>/
    date:      (required) ISO date, e.g. 2026-06-05
    author:    author byline (default: Granid)
    excerpt:   (required) one-line summary, used for meta description + OG
    lede:      optional standfirst paragraph rendered above the body
    og_image:  absolute path/URL for the share image
               (default: /og_image_1200x630.png)
    tags:      comma-separated list, e.g. "Data sovereignty, On-premise AI"

Supported Markdown body subset:
    ## H2 / ### H3
    paragraphs
    - unordered lists / 1. ordered lists
    > callout (blockquote)
    ```fenced code```
    ![alt](/path.svg "optional caption")    -> responsive figure
    [text](https://url)                      -> link
    **bold**  and  `inline code`
    {% video src="/assets/.../clip.mp4" poster="/assets/.../poster.png"
             caption="..." %}                -> responsive 16:9 self-hosted video
"""

import html
import json
import os
import re
import sys

SITE = "https://granid.ch"
DEFAULT_OG_IMAGE = "/og_image_1200x630.png"
WORDS_PER_MINUTE = 200

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── front-matter ────────────────────────────────────────────────────────────

def parse_front_matter(text):
    if not text.startswith("---"):
        sys.exit("error: file must start with a '---' front-matter fence")
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    for required in ("title", "slug", "date", "excerpt"):
        if not meta.get(required):
            sys.exit(f"error: front-matter is missing required key '{required}'")
    meta.setdefault("author", "Granid")
    meta.setdefault("og_image", DEFAULT_OG_IMAGE)
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    return meta, body.strip("\n")


# ── inline formatting (applied to already-escaped text) ──────────────────────

def render_inline(text):
    """Escape, then apply the inline allowlist. Order matters: code first so
    its contents are not re-processed for bold/links."""
    out = html.escape(text)

    # `inline code`
    out = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", out)

    # [text](url) — url is escaped; only http(s), mailto and root-relative allowed
    def link(m):
        label, url = m.group(1), m.group(2)
        if not re.match(r"^(https?:|mailto:|/)", url):
            return m.group(0)
        return f'<a href="{url}">{label}</a>'

    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)

    # **bold**
    out = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"<strong>{m.group(1)}</strong>", out)
    return out


# ── block parser ─────────────────────────────────────────────────────────────

VIDEO_RE = re.compile(r'\{%\s*video\s+(.*?)\s*%\}', re.DOTALL)
IMAGE_RE = re.compile(r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)$')
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


def safe_src(url):
    """Allow only root-relative or https media paths."""
    return url if re.match(r"^(/|https?:)", url) else ""


def render_video(raw_attrs):
    attrs = dict(ATTR_RE.findall(raw_attrs))
    src = safe_src(attrs.get("src", ""))
    if not src:
        return ""
    poster = safe_src(attrs.get("poster", ""))
    caption = html.escape(attrs.get("caption", ""))
    poster_attr = f' poster="{poster}"' if poster else ""
    cap_html = f"\n    <figcaption>{caption}</figcaption>" if caption else ""
    return (
        '  <figure class="article-video">\n'
        f'    <video controls preload="metadata"{poster_attr}>\n'
        f'      <source src="{src}" type="video/mp4">\n'
        '    </video>'
        f'{cap_html}\n'
        '  </figure>'
    )


def render_figure(alt, src, caption):
    src = safe_src(src)
    if not src:
        return ""
    alt = html.escape(alt)
    cap_html = f"\n    <figcaption>{html.escape(caption)}</figcaption>" if caption else ""
    return (
        '  <figure class="article-figure">\n'
        f'    <img src="{src}" alt="{alt}" loading="lazy">'
        f'{cap_html}\n'
        '  </figure>'
    )


def render_body(md):
    # Pull fenced code and video shortcodes out first so their contents are
    # never touched by the line-based parser.
    placeholders = {}

    def stash(htmlfrag):
        key = f"\x00{len(placeholders)}\x00"
        placeholders[key] = htmlfrag
        return key

    def code_block(m):
        code = html.escape(m.group(1))
        return "\n" + stash(f"  <pre><code>{code}</code></pre>") + "\n"

    md = re.sub(r"```[^\n]*\n(.*?)```", code_block, md, flags=re.DOTALL)
    md = VIDEO_RE.sub(lambda m: "\n" + stash(render_video(m.group(1))) + "\n", md)

    blocks = []
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        if line in placeholders:
            blocks.append(placeholders[line])
            i += 1
            continue

        if line.startswith("### "):
            blocks.append(f"  <h3>{render_inline(line[4:])}</h3>")
            i += 1
            continue
        if line.startswith("## "):
            blocks.append(f"  <h2>{render_inline(line[3:])}</h2>")
            i += 1
            continue

        # image on its own line -> figure
        img = IMAGE_RE.match(line.strip())
        if img:
            blocks.append(render_figure(img.group(1), img.group(2), img.group(3) or ""))
            i += 1
            continue

        # blockquote -> callout
        if line.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:])
                i += 1
            blocks.append(
                '  <blockquote class="article-callout">\n'
                f'    <p>{render_inline(" ".join(buf))}</p>\n'
                '  </blockquote>'
            )
            continue

        # lists
        if re.match(r"^[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i].strip()):
                items.append(render_inline(lines[i].strip()[2:]))
                i += 1
            lis = "\n".join(f"    <li>{it}</li>" for it in items)
            blocks.append(f"  <ul>\n{lis}\n  </ul>")
            continue
        if re.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i].strip()):
                items.append(render_inline(re.sub(r"^\d+\.\s", "", lines[i].strip())))
                i += 1
            lis = "\n".join(f"    <li>{it}</li>" for it in items)
            blocks.append(f"  <ol>\n{lis}\n  </ol>")
            continue

        # paragraph (gather consecutive plain lines)
        buf = []
        while i < len(lines) and lines[i].strip() and lines[i] not in placeholders \
                and not re.match(r"^(#{2,3} |> |[-*] |\d+\. )", lines[i].strip()) \
                and not IMAGE_RE.match(lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        blocks.append(f"  <p>{render_inline(' '.join(buf))}</p>")

    return "\n".join(blocks)


# ── page template ────────────────────────────────────────────────────────────

def reading_time(md):
    words = len(re.findall(r"\w+", md))
    return max(1, round(words / WORDS_PER_MINUTE))


def human_date(iso):
    """ISO date -> reader-friendly form, e.g. '5 June 2026'. Machine fields
    (article:published_time, JSON-LD) keep the ISO value."""
    import datetime
    return datetime.datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %B %Y")


def build_page(meta, body_html, md_body):
    url = f"{SITE}/blog/{meta['slug']}/"
    title = html.escape(meta["title"])
    desc = html.escape(meta["excerpt"])
    author = html.escape(meta["author"])
    og_image = meta["og_image"]
    if og_image.startswith("/"):
        og_image = SITE + og_image
    og_image = html.escape(og_image)
    mins = reading_time(md_body)

    tags_html = ""
    if meta["tags"]:
        chips = "\n".join(
            f'        <span class="article-tag">{html.escape(t)}</span>'
            for t in meta["tags"]
        )
        tags_html = f'\n      <div class="article-tags">\n{chips}\n      </div>'

    lede_html = ""
    if meta.get("lede"):
        lede_html = f'    <p class="lede">{render_inline(meta["lede"])}</p>\n'

    hero_html = ""
    if meta.get("hero"):
        hero_src = safe_src(meta["hero"])
        if hero_src:
            hero_html = (
                '      <figure class="article-hero">\n'
                f'        <img src="{html.escape(hero_src)}" alt="" loading="eager">\n'
                '      </figure>\n'
            )

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": meta["title"],
        "description": meta["excerpt"],
        "datePublished": meta["date"],
        "url": f"{SITE}/blog/{meta['slug']}/",
        "image": (SITE + meta["og_image"]) if meta["og_image"].startswith("/") else meta["og_image"],
        "author": {"@type": "Organization", "name": meta["author"]},
        "publisher": {
            "@type": "Organization",
            "name": "Granid",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE}/assets/images/granid_logo_black.png",
            },
        },
        "inLanguage": "en",
        "isPartOf": {"@type": "Blog", "name": "Granid Blog", "url": f"{SITE}/blog/"},
    }, indent=2, ensure_ascii=False)

    return TEMPLATE.format(
        title=title,
        desc=desc,
        author=author,
        url=html.escape(url),
        og_image=og_image,
        date=html.escape(meta["date"]),
        date_human=html.escape(human_date(meta["date"])),
        mins=mins,
        tags_html=tags_html,
        lede_html=lede_html,
        hero_html=hero_html,
        body=body_html,
        jsonld=jsonld,
    )


# {{ and }} are literal braces for str.format; the CSS link block has none.
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Granid</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon_dark.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="shortcut icon" href="/favicon.ico">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Granid">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="en_CH">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Granid Edge Intelligence">
  <meta property="article:published_time" content="{date}">
  <meta property="article:author" content="{author}">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_image}">

  <!-- Structured data -->
  <script type="application/ld+json">
{jsonld}
  </script>

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

  <article class="article">
    <div class="article-inner">
      <header class="article-header">
        <span class="eyebrow">Granid Blog</span>
        <h1>{title}</h1>
        <div class="article-meta">
          <span>{date_human}</span>
          <span>{author}</span>
          <span>{mins} min read</span>
        </div>{tags_html}
      </header>
{hero_html}
      <div class="article-body">
{lede_html}{body}
      </div>

      <aside class="article-cta">
        <p>Granid runs entirely on a Mac in your office. Your client data never leaves the building.</p>
        <div class="actions">
          <a href="/trial/" class="btn">Try free for 2 weeks</a>
          <a href="/hardware/production/" class="btn btn--sec">See recommended hardware</a>
        </div>
      </aside>

      <div class="article-back">
        <a href="/blog/">&larr; All articles</a>
      </div>
    </div>
  </article>

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
</body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 tools/render_post.py content/blog/<slug>/post.md")
    src_path = sys.argv[1]
    with open(src_path, encoding="utf-8") as fh:
        meta, md_body = parse_front_matter(fh.read())

    body_html = render_body(md_body)
    page = build_page(meta, body_html, md_body)

    out_dir = os.path.join(REPO_ROOT, "blog", meta["slug"])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)

    rel = os.path.relpath(out_path, REPO_ROOT)
    print(f"rendered: {rel}  ({reading_time(md_body)} min read, {len(meta['tags'])} tags)")


if __name__ == "__main__":
    main()
