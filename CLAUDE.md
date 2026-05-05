# Granid — Project Context

## Cross-repo context

This project is one of three coordinated Granid repos. Cross-repo concerns are owned by the spec at:

**`~/Lab/legalintelligence/ECOSYSTEM.md`** — authoritative cross-repo spec. **In case of conflict between this CLAUDE.md and ECOSYSTEM.md, ECOSYSTEM.md wins.** Read it before making structural changes (tier definitions, form schemas, endpoint contracts, hardware spec page URLs).

The other Granid repos:
- **`lab/legalintelligence`** — the on-premise product (Mac Mini install). Owns ECOSYSTEM.md.
- **`lab/granid-crm`** — internal CRM at `crm.granid.ch`. Signs license JWTs, owns trial issuance and (when implemented) Stripe payment processing.

This repo (`granid-website`) is the public marketing site at `granid.ch`. It renders forms; backend logic and persistence live in `granid-crm`.

Plane projects: `LEGALINT`, `GCRM`, `GWEB`. Cross-repo work for ECOSYSTEM.md alignment tracked in `LEGALINT-171`.

## Company

Granid is an on-premise AI platform for Swiss legal and accounting professionals. The core value proposition is local data sovereignty: hardware (Mac Mini M4 Pro, 64GB unified memory) deployed in the client's office, ensuring client data never leaves the building. This directly addresses Swiss attorney-client privilege obligations (Anwaltsgeheimnis, Art. 321 StGB, nDSG/FADP).

- Company name: Granid (derived from "granite" — solid, Swiss, indestructible)
- Domain: granid.ch (registered on Infomaniak)
- Email: stefano@granid.ch
- Tagline: "Human in the Loop"
- Legal structure: Einzelunternehmen now, GmbH after validation with paying clients
- Founder: Stefano Leone, based in Zurich

## Products

Per ECOSYSTEM.md, Granid currently ships a single product:

- **Legal Intelligence by Granid** — on-premise legal AI for Swiss law firms.

Reserved brand tokens for planned future products (not on the active roadmap):

- Meeting Intelligence by Granid
- Accounting Intelligence by Granid
- Compliance Intelligence by Granid

All product brand names ("Granid", "Legal Intelligence", "Meeting Intelligence", "Accounting Intelligence", "Compliance Intelligence") are **never translated**, even on DE/FR/IT pages.

## Competitor

STP.one / Winjur — legacy software aesthetics, cloud architecture. Their white paper acknowledges data privacy as the primary AI adoption risk but offers no architectural solution. Granid's on-premise model eliminates this liability entirely.

## Brand Positioning

Tech company proudly identified as such, contrasting STP.one/Winjur's legacy aesthetic. Target feeling: Anthropic / Notion / Stripe energy. Not a law firm, not a consultancy — a technology company that serves legal professionals.

## Website Brief

### Pages

See the "File Structure" section below for the full page tree (current + target). Every page exists in four languages — EN at the root, DE/FR/IT under their respective subdirectories.

### Languages
- English (default)
- German (DE)
- French (FR)
- Italian (IT)

### Design Direction
Modern Swiss institutional. Think Swiss International Style: clean typography, generous whitespace, sober colors, precision. Like SNB or Vontobel websites, but with tech energy. No gimmicks, no animations for the sake of it. Every element earns its place.

### Color Palette
Derive from the concept of granite: grays, deep charcoals, with a single accent color for CTAs. White or very light background. Dark text. The site should feel solid, trustworthy, and premium.

### Typography
A clean sans-serif. Inter, Geist, or similar. Two weights maximum (regular + semibold). Generous line height.

### Tiers, pricing, acquisition

Per ECOSYSTEM.md "License tiers". **Tier strings, seat caps, and acquisition path are normative cross-repo** — they must match the JWT `tier` claim consumed by Legal Intelligence and the CTAs rendered by this site.

| Tier | Seats (lawyers + secretaries combined) | Acquisition | Hardware | Pricing |
|------|----------------------------------------|-------------|----------|---------|
| **trial** | 1 professional | Self-service via `/trial` form → CRM activation flow | Any Mac with Apple Silicon, ≥ 8 GB RAM (lightweight; embeddings + LLM run on Granid-hosted OpenRouter) | Free, 2 weeks hard |
| **essential** | 1 professional | Self-service via `/buy/essential` → Stripe Checkout *(currently simulated, real Stripe deferred — see GWEB-12)* | Mac Mini M4 Pro 64 GB (fully local) | CHF 5,900 setup + CHF 990 / year |
| **professional** | up to 4 professionals (any mix) | Self-service via `/buy/professional` → Stripe Checkout *(simulated)* | Mac Mini M4 Pro 64 GB | CHF 12,500 setup + CHF 2,400 / year |
| **enterprise** | up to 15 professionals | Sales-led inquiry via `/contact-enterprise` form | Mac Mini M4 Pro 64 GB | CHF 24,000 setup + CHF 4,800 / year |

Acquisition row for Essential/Professional reflects the 2026-05-05 decision to use self-service Stripe Checkout instead of sales-led inquiry. ECOSYSTEM.md update tracked in `LEGALINT-171`.

Hardware spec pages are the single source of truth, linked from CRM emails — URLs must stay stable:
- `/hardware/trial` (trial spec, lightweight Apple Silicon)
- `/hardware/production` (paid spec, Mac Mini M4 Pro 64 GB)

### Forms

The legacy generic Formsubmit.co form on the homepage will be removed (`GWEB-16`) once the tier-specific funnels below are live. All new forms POST JSON to the CRM API; field schemas are normative in ECOSYSTEM.md.

| Path | Purpose | Endpoint | Tracked in |
|------|---------|----------|------------|
| `/trial` | Trial signup (9 fields + mandatory privacy checkbox) | `POST https://crm.granid.ch/api/v1/leads` | `GWEB-9`, `GWEB-10` |
| `/buy/<tier>` | Self-service paid checkout for Essential / Professional (currently simulated) | `POST https://crm.granid.ch/api/v1/checkout/draft` (when real) | `GWEB-12` |
| `/contact-enterprise` | Sales-led inquiry for Enterprise tier | TBD endpoint, see `LEGALINT-171` | `GWEB-14`, `GWEB-15` |

Every form includes a hidden `locale` field carrying the current page language (`en` / `de` / `fr` / `it`), so CRM email replies are localized.

### Technical Stack
- Pure HTML / CSS / JS (no frameworks, no build step)
- Hosted on GitHub Pages
- Custom domain: granid.ch
- DNS configured on Infomaniak pointing to GitHub Pages IPs
- SSL: automatic via GitHub Pages

### GitHub Pages DNS Configuration (for Infomaniak)
- A record: 185.199.108.153
- A record: 185.199.109.153
- A record: 185.199.110.153
- A record: 185.199.111.153
- CNAME: www -> stefanoleone.github.io
- CNAME file in repo root containing: granid.ch

### Repository
- Name: granid-website
- Owner: stefanoleone
- Branch: main
- GitHub Pages source: main branch, root directory

## Key Messaging

### Hero
The AI that never leaves your office. / L'IA qui ne quitte jamais votre bureau. / Die KI, die Ihr Büro nie verlässt. / L'AI che non lascia mai il tuo studio.

### Problem Statement
Every time you use cloud AI tools with client documents, you risk violating attorney-client privilege. Your clients trust you with their most sensitive information. That trust should not travel to external servers.

### Solution
Granid installs directly in your office. A dedicated device running AI that understands Swiss law in all four national languages. Your data stays in your building. Always.

### Differentiators
- On-premise: data never leaves the client's office
- Multilingual: DE/FR/IT/EN legal corpus
- Verified citations: every legal reference is checked
- Human in the Loop: AI assists, humans decide

## Content Tone
Professional, confident, understated. No hype, no buzzwords. Write as if addressing a senior partner at a top Swiss law firm. Short sentences. Facts over adjectives. Swiss precision in every word.

## File Structure

Current (today):

```
granid-website/
  CLAUDE.md
  CNAME
  index.html          (EN homepage)
  de/index.html       (DE homepage)
  fr/index.html       (FR homepage)
  it/index.html       (IT homepage)
  thanks.html         (EN — legacy, removed in GWEB-16)
  de/thanks.html      (legacy)
  fr/thanks.html      (legacy)
  it/thanks.html      (legacy)
  css/style.css
  js/main.js
  assets/images/, assets/fonts/
```

Target (after GWEB-3..15 land):

```
granid-website/
  index.html, de/, fr/, it/                                     (homepages — refreshed in GWEB-6..8)

  hardware/trial/index.html                                     (EN — GWEB-3)
  hardware/production/index.html                                (EN — GWEB-4)
  {de,fr,it}/hardware/{trial,production}/index.html              (GWEB-3, GWEB-4)

  trial/index.html                                              (EN trial form — GWEB-9, GWEB-10)
  trial-sent/index.html                                         (EN post-submit — GWEB-11)
  {de,fr,it}/trial/, {de,fr,it}/trial-sent/                      (GWEB-9, GWEB-11)

  buy/essential/index.html                                      (EN simulated checkout — GWEB-12)
  buy/professional/index.html                                   (EN simulated checkout — GWEB-12)
  buy/success/index.html, buy/cancelled/index.html              (EN — GWEB-13)
  {de,fr,it}/buy/<tier>/, /success/, /cancelled/                 (GWEB-12, GWEB-13)

  contact-enterprise/index.html                                 (EN — GWEB-14, GWEB-15)
  {de,fr,it}/contact-enterprise/                                 (GWEB-14)

  css/style.css, js/main.js, assets/
```

URL stability: `/hardware/trial`, `/hardware/production`, `/buy/success`, `/buy/cancelled` are linked from CRM emails — renaming requires a coordinated update in `granid-crm` email templates and in `legalintelligence/CLAUDE.md`.
