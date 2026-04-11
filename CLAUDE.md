# Granid — Project Context

## Company

Granid is an on-premise AI platform for Swiss legal and accounting professionals. The core value proposition is local data sovereignty: hardware (Mac Mini M4 Pro, 64GB unified memory) deployed in the client's office, ensuring client data never leaves the building. This directly addresses Swiss attorney-client privilege obligations (Anwaltsgeheimnis, Art. 321 StGB, nDSG/FADP).

- Company name: Granid (derived from "granite" — solid, Swiss, indestructible)
- Domain: granid.ch (registered on Infomaniak)
- Email: stefano@granid.ch
- Tagline: "Human in the Loop"
- Legal structure: Einzelunternehmen now, GmbH after validation with paying clients
- Founder: Stefano Leone, based in Zurich

## Products

- Legal Intelligence by Granid
- Accounting Intelligence by Granid
- Compliance Intelligence by Granid

## Competitor

STP.one / Winjur — legacy software aesthetics, cloud architecture. Their white paper acknowledges data privacy as the primary AI adoption risk but offers no architectural solution. Granid's on-premise model eliminates this liability entirely.

## Brand Positioning

Tech company proudly identified as such, contrasting STP.one/Winjur's legacy aesthetic. Target feeling: Anthropic / Notion / Stripe energy. Not a law firm, not a consultancy — a technology company that serves legal professionals.

## Website Brief

### Pages
- Homepage: hero + problem + solution + three pricing tiers + contact form + footer
- Thank you page: confirmation after form submission
- Same structure replicated in 4 languages

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

### Pricing Tiers (current, subject to revision)

Essential:
- Setup: CHF 5,900
- Annual: CHF 990/yr
- Target: solo practitioners and small firms

Professional:
- Setup: CHF 12,500
- Annual: CHF 2,400/yr
- Target: mid-size firms

Enterprise:
- Setup: CHF 24,000
- Annual: CHF 4,800/yr
- Target: large firms with SSO/OIDC, remote access, MFA

Each tier unlocks the next MCP connector; the previous connector graduates to active intelligence services.

### Contact Form
Using Formsubmit.co (free, no submission limits). Form posts to stefano@granid.ch. After submission, redirect to /grazie.html (or language-appropriate thank you page).

Form fields:
- Email (required)
- Name of the firm/studio (required)
- Number of lawyers/professionals (optional)
- Message / what interests you most (optional)

Hidden fields:
- _captcha: false
- _next: redirect to thank you page

```html
<form action="https://formsubmit.co/stefano@granid.ch" method="POST">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="https://granid.ch/thanks.html">
  <!-- form fields here -->
</form>
```

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
```
granid-website/
  CLAUDE.md
  CNAME
  index.html          (EN - default)
  de/index.html       (DE)
  fr/index.html       (FR)
  it/index.html       (FR)
  thanks.html         (EN)
  de/thanks.html      (DE)
  fr/thanks.html      (FR)
  it/thanks.html      (IT)
  css/
    style.css
  js/
    main.js
  assets/
    images/
    fonts/
```
