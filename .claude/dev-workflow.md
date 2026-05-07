# granid-website — Development Workflow

You are working on `granid.ch`, a static HTML/CSS/JS marketing site hosted on GitHub Pages, available in EN/DE/FR/IT. Every session on this repo follows the steps below in order.

This workflow is injected into every session by a `SessionStart` hook (see `.claude/settings.json`). Treat it as the default plan unless the user explicitly overrides it.

## Step 1 — Ticket

Every change is tracked in the Plane project **Granid Website (`GWEB`)**. Before any code is written:

- If the user names a ticket (e.g., "do GWEB-14"), open it via `mcp__plane__retrieve_work_item_by_identifier` and read the description in full.
- If the user describes work without a ticket, ask whether to create one first or to proceed informally. Default to creating one for anything bigger than a one-line copy fix.
- Mark the ticket `in_progress` before starting (state UUID in the Granid Website project: `3267e329-65e9-4901-b763-996fd2043b74`).

## Step 2 — Plan (when needed)

For non-trivial work — multi-file changes, new pages, anything touching forms or CRM contracts, or anything affecting `/hardware/*` or `/buy/*` URLs that CRM emails link to — invoke the `tech-lead` subagent before writing code. The plan should fit in ≤ 30 lines and name the reviewers that will fire pre-merge.

Skip Step 2 for: single-string copy edits, single-CSS spacing tweaks, mechanical multi-language fan-outs of an already-approved page.

## Step 3 — Branch

Always work on a new branch, never directly on `main`. Branch name: `gweb-N-short-description` matching the Plane ticket (e.g., `gweb-14-15-enterprise-form`). One branch per ticket.

`main` only receives merges via PR. The only exception is committing pre-existing WIP that was already on `main` to clear the working tree before starting a new ticket.

## Step 4 — Implement

Write the code. Constraints from `CLAUDE.md`:

- Pure HTML / CSS / JS. No build step. No frameworks.
- Every visible change ships in EN + DE + FR + IT in the same commit.
- Brand tokens (`Granid`, `Legal Intelligence`, `Meeting Intelligence`, `Accounting Intelligence`, `Compliance Intelligence`) are never translated.
- Form schemas, tier names, seat caps, and CRM endpoint contracts come from `~/Lab/legalintelligence/ECOSYSTEM.md` — that doc wins over local CLAUDE.md.
- Test locally on the dev server (`python3 -m http.server 4173` from the repo root) before considering a step done.

## Step 5 — Auto-review (specialist agents)

Before committing, invoke the relevant specialist subagents based on what changed. The mapping below is normative — fire them automatically without asking the user, unless the user explicitly says "skip review":

| Change type | Reviewers (in order, all must approve) |
|-------------|----------------------------------------|
| New page (any path) | `ux-flow-reviewer` → `content-copy-reviewer` |
| Copy-only edit on existing page | `content-copy-reviewer` |
| New form, or any change to a `<form>` | `ux-flow-reviewer` → `content-copy-reviewer` → `security-auditor` |
| New JS submit handler / new `fetch()` to external origin | `security-auditor` → `ux-flow-reviewer` |
| Nav, language switcher, or CTA change | `ux-flow-reviewer` → `content-copy-reviewer` |
| New `<script src="...">` or `<link rel="...">` to external origin | `security-auditor` |
| `<meta>` changes (CSP, robots, referrer, og:*) | `security-auditor` (CSP/robots/referrer) or `content-copy-reviewer` (og:*) |
| Hardware-spec URL or CRM-linked URL change | `tech-lead` (cross-repo coordination) → `ux-flow-reviewer` → `content-copy-reviewer` |
| `.claude/` agent or workflow config | `tech-lead` only |
| Pure CSS visual tweak (no responsive impact, no contrast change, no focus state change) | none |

If a reviewer reports issues at severity Critical or Major, fix them first and re-invoke the same reviewer. Minor findings can be deferred to a follow-up ticket — note the deferral in the PR body and create the ticket.

## Step 6 — Commit & Push

Commit only after every relevant reviewer has reported no Critical / Major issues. Conventional commit message format:

```
GWEB-N: <short imperative verb phrase>

<body — explain why, not what; mention any deferred Minor findings
and the follow-up ticket they were filed against>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

Push the branch with `git push -u origin <branch>`.

## Step 7 — PR & Merge

Open the PR via `gh pr create` with a Summary + Test plan. Default base is `main`. The PR body should include:

- One-line summary of each commit if the branch has multiple commits
- Out-of-scope items deferred to follow-up tickets, with the ticket IDs
- Any cross-repo coordination needed (e.g., "blocked on `GCRM` endpoint X" or "ECOSYSTEM.md update tracked in `LEGALINT-N`")

Merge with `gh pr merge <N> --merge` once the user confirms. Mark all involved Plane tickets as Done.

After merge, sync local `main` (`git checkout main && git pull`) before starting the next ticket.

## Notes

- The Plane workspace has three projects: `LEGALINT` (Legal Intelligence product), `GCRM` (CRM backend), `GWEB` (this site). Cross-repo coordination items live in `LEGALINT` (e.g., ECOSYSTEM.md updates).
- Tickets blocked on the CRM (anything that needs `crm.granid.ch/api/v1/*` to be live) carry the `blocked-by-crm` label and ship the UI without a working backend — the form renders, validation runs, and the network call fails with the generic error until the CRM is up.
- `.DS_Store`, `assets/`, and `.claude/` are currently untracked. Don't add them to commits unless explicitly asked.
