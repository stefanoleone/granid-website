---
name: No em dash in user-visible copy
description: Em dash (—, U+2014) is banned in customer-facing strings. Replace with comma, colon, parentheses, or a sentence break.
type: feedback
---

Never use em dash (`—`, U+2014) in any string a visitor of `granid.ch` can read: page copy, headings, subtitles, CTAs, button labels, form labels, hints, error messages, `<title>` and `<meta>` tags, `aria-*` / `title` / `alt` attributes, and JS i18n blocks.

**Why:** Stefano flagged on 2026-05-07. The site targets senior partners at Swiss law firms. Em dash reads as a stylistic tic and dilutes the calm, factual register Granid wants. Forcing the writer to choose comma vs colon vs parentheses vs sentence break also produces tighter prose.

**How to apply:**

- **Em dash (`—`, U+2014)**: always a finding. Replace contextually:
  - Comma when the clause flows with the sentence: `Granid runs locally — no data leaves the office.` → `Granid runs locally, with no data leaving the office.`
  - Colon when the second clause defines or expands: `One promise — your data stays in the building.` → `One promise: your data stays in the building.`
  - Parentheses when it's a true aside that could be skipped: `Apple Silicon (M1–M4) — Intel is not supported.` → `Apple Silicon (M1, M2, M3, or M4). Intel is not supported.`
  - Sentence break for compliance lines or split thoughts: `nothing leaves the office — for any data, ever.` → `Nothing leaves the office. Not for any data, ever.`

- **En dash (`–`, U+2013)**: allowed **only** in numeric ranges (`5–15 professionals`, `M1–M4`, `1–3 weeks`). Anywhere else, treat it like em dash.

- **Hyphen (`-`, U+002D)**: stays as-is. Used for compound words.

- This applies to all four languages (EN/DE/FR/IT). DE has a tradition of compound nouns; em dashes there usually become commas or split sentences. FR and IT often replace em dashes with `:` or `,`. EN tends toward comma or sentence break.

- The grep to find them: `grep -nE '[—–]' file.html` lists both em and en dashes. Spot-check each match — en dashes inside numeric ranges are fine.
