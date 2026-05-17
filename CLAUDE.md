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

Granid is an on-premise AI platform for Swiss legal and accounting professionals. The core value proposition is local data sovereignty: the software runs on a Mac (Apple Silicon, 64 GB unified memory) the client owns and keeps in the firm's office, ensuring client data never leaves the building. This directly addresses Swiss attorney-client privilege obligations (Anwaltsgeheimnis, Art. 321 StGB, nDSG/FADP). Hardware is **not** bundled with any tier — see "Tiers, pricing, acquisition" below.

- Company name: Granid (derived from "granite" — solid, Swiss, indestructible)
- Domain: granid.ch (registered on Infomaniak)
- Email: stefano@granid.ch
- Tagline: "Human in the Loop"
- Legal structure: Einzelunternehmen now, GmbH after validation with paying clients
- Founder: Stefano Leone, based in Zurich

## Products

Granid currently ships:

- **Legal Intelligence by Granid** — on-premise legal AI for Swiss law firms (flagship: tabular document review).
- **Voice Intelligence by Granid** — on-device legal dictation with personal vocabulary. Integrated into Legal Intelligence from the **Professional** tier upwards. Tracked in the Plane project `VOICEINT`.

Reserved brand tokens for products on the roadmap but not yet shipping:

- Meeting Intelligence by Granid — coming soon, included with **Enterprise**.
- Accounting Intelligence by Granid
- Compliance Intelligence by Granid

All product brand names ("Granid", "Legal Intelligence", "Voice Intelligence", "Meeting Intelligence", "Accounting Intelligence", "Compliance Intelligence") and the corporate descriptor "Edge Intelligence" (used in the site footer) are **never translated**, even on DE/FR/IT pages.

**Naming note.** `legalintelligence/business/pricing.md` and `ECOSYSTEM.md` still use the provisional token "Talk Intelligence". The site uses the definitive "Voice Intelligence" — alignment in the legalintelligence repo is tracked as `LEGALINT-193`.

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

Commercial source of truth: **`~/Lab/legalintelligence/business/pricing.md`** (introduced by LEGALINT-192). JWT `tier` claim and seat enforcement contract: **`ECOSYSTEM.md` § License tiers**. The table below mirrors `business/pricing.md` — keep it in sync.

| Tier | Seats | Acquisition | Recommended hardware (BYO) | Pricing (excl. VAT) |
|------|-------|-------------|----------------------------|---------------------|
| **trial** | 1 professional | Self-service via `/trial` form → CRM activation flow | Any Mac with Apple Silicon, ≥ 8 GB RAM (lightweight; embeddings + LLM run on Granid-hosted OpenRouter) | Free, 2 weeks hard |
| **essential** | 1 professional | Self-service via `/buy/essential` → Stripe Checkout *(currently simulated, real Stripe deferred — see GWEB-12)* | Mac Mini Apple Silicon, 64 GB unified RAM | CHF 990 / year |
| **professional** | up to 4 professionals | Self-service via `/buy/professional` → Stripe Checkout *(simulated)* | Mac Mini Apple Silicon, 64 GB unified RAM | CHF 2 990 / year |
| **enterprise** | Custom (default 15, operator-overridable) | Sales-led inquiry via `/contact-enterprise` form | Mac Studio Apple Silicon, 64 GB+ unified RAM | Contact us |

**Hardware is not included in any tier.** Customers acquire their own Mac and install the software on it. `/hardware/production` is a *recommended specs* page, not a sales page.

Features (cumulative — each tier inherits from the tier above):

| Feature | Essential | Professional | Enterprise |
|---------|-----------|--------------|------------|
| Legal Intelligence (tabular document review, Swiss legal corpus, verified citations) | ✓ | ✓ | ✓ |
| Voice Intelligence (on-device legal dictation with custom vocabulary) | — | ✓ | ✓ |
| Meeting Intelligence *(coming soon)* | — | — | ✓ |

**Pricing display contract** (per `business/pricing.md`): every paid price card and CTA on the site **must** carry the "excl. VAT" qualifier (Swiss VAT 8.1% standard rate as of 2026-05-15).

Hardware spec pages are linked from CRM emails — URLs must stay stable:
- `/hardware/trial` (trial spec, lightweight Apple Silicon)
- `/hardware/production` (paid recommended specs: Mac Mini for Essential/Professional, Mac Studio for Enterprise)

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

  terms/index.html                                              (EN T&C — GWEB-24)
  {de,fr,it}/terms/                                              (GWEB-24)

  css/style.css, js/main.js, assets/
```

URL stability: `/hardware/trial`, `/hardware/production`, `/buy/success`, `/buy/cancelled` are linked from CRM emails — renaming requires a coordinated update in `granid-crm` email templates and in `legalintelligence/CLAUDE.md`.
