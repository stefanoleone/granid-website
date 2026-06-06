#!/usr/bin/env python3
"""Generate a branded, decorative SVG hero/thumbnail for a blog post.

GWEB-55. Run manually; output committed. On-brand placeholder art so posts
have a card thumbnail and article hero without sourcing photography.

    python3 tools/make_hero.py <slug> "Title text" [variant]

Writes assets/blog/<slug>/hero.svg. `variant` (int) picks a motif so adjacent
cards look distinct. The art is PURELY decorative — no title text is baked in,
because the card/article already renders the title and an image cropped with
object-fit:cover would clip any embedded words. Motifs are full-bleed so they
crop gracefully at any aspect ratio. Granite palette (see
vendor/granid-ds/tokens/01-primitives.css): ink #1C1917, stone #E7E5E4 /
#F5F5F4 / #D6D3D1, accent red #DA281C.

The `title` argument is kept for the SVG aria-label only.
"""
import html
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each variant: (background, full-bleed motif markup over a 1200x630 canvas).
MOTIFS = [
    # 0 — light stone, large centred ring + accent disc
    ("#F5F5F4",
     '<circle cx="600" cy="315" r="240" fill="none" stroke="#E7E5E4" stroke-width="40"/>'
     '<circle cx="600" cy="315" r="150" fill="none" stroke="#D6D3D1" stroke-width="24"/>'
     '<circle cx="600" cy="315" r="60" fill="#DA281C"/>'),
    # 1 — ink, concentric rings with accent inner
    ("#1C1917",
     '<circle cx="600" cy="315" r="260" fill="none" stroke="#2A2724" stroke-width="44"/>'
     '<circle cx="600" cy="315" r="170" fill="none" stroke="#44403C" stroke-width="28"/>'
     '<circle cx="600" cy="315" r="78" fill="none" stroke="#DA281C" stroke-width="22"/>'),
    # 2 — light, full-bleed diagonal bands + one accent band
    ("#FAFAF9",
     '<g stroke-width="70">'
     '<line x1="-100" y1="730" x2="800" y2="-170" stroke="#EFEDEB"/>'
     '<line x1="100" y1="730" x2="1000" y2="-170" stroke="#E7E5E4"/>'
     '<line x1="300" y1="730" x2="1200" y2="-170" stroke="#DA281C"/>'
     '<line x1="520" y1="830" x2="1420" y2="-70" stroke="#E7E5E4"/>'
     '</g>'),
    # 3 — light, full-canvas dot grid with one accent dot
    ("#F5F5F4",
     ''.join(
        f'<circle cx="{80 + c*120}" cy="{75 + r*120}" r="13" '
        f'fill="{"#DA281C" if (r==2 and c==5) else "#D6D3D1"}"/>'
        for r in range(5) for c in range(10))),
    # 4 — ink, offset arcs sweeping the canvas
    ("#1C1917",
     '<path d="M-50 630 A 650 650 0 0 1 600 -20" fill="none" stroke="#2A2724" stroke-width="46"/>'
     '<path d="M200 650 A 560 560 0 0 1 760 90" fill="none" stroke="#44403C" stroke-width="30"/>'
     '<path d="M520 700 A 520 520 0 0 1 1040 180" fill="none" stroke="#DA281C" stroke-width="24"/>'),
    # 5 — light, vertical granite columns + accent column
    ("#FAFAF9",
     '<g>'
     '<rect x="60" y="0" width="120" height="630" fill="#EFEDEB"/>'
     '<rect x="300" y="0" width="120" height="630" fill="#E7E5E4"/>'
     '<rect x="540" y="0" width="120" height="630" fill="#DA281C"/>'
     '<rect x="780" y="0" width="120" height="630" fill="#E7E5E4"/>'
     '<rect x="1020" y="0" width="120" height="630" fill="#EFEDEB"/>'
     '</g>'),
]


def make_hero(slug, title, variant=0):
    bg, motif = MOTIFS[variant % len(MOTIFS)]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-label="{html.escape(title)}">
  <rect width="1200" height="630" fill="{bg}"/>
  {motif}
</svg>
'''
    out_dir = os.path.join(REPO_ROOT, "assets", "blog", slug)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "hero.svg")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(svg)
    return os.path.relpath(out, REPO_ROOT)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('usage: python3 tools/make_hero.py <slug> "Title" [variant]')
    variant = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    print("wrote", make_hero(sys.argv[1], sys.argv[2], variant))
