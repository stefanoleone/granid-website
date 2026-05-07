# granid-website — Personal Project Rules

## Language

- All code, comments, and dev-facing documentation in English.
- The only exception is user-facing copy on the site itself, which exists in EN + DE + FR + IT under the localized subdirectories (`/`, `/de/`, `/fr/`, `/it/`).
- Brand tokens (`Granid`, `Legal Intelligence`, `Meeting Intelligence`, `Accounting Intelligence`, `Compliance Intelligence`) are never translated.

## Workflow

The full workflow is in `.claude/dev-workflow.md` and is injected automatically at session start. Specialist agents fire pre-merge based on the change-type matrix in that file. Don't skip the auto-review step.

## Branch policy

One branch per Plane ticket. Branch name `gweb-N-short-description`. Never commit substantive work to `main`. PR review and merge happen via `gh pr create` / `gh pr merge`.

## Cross-repo authority

`~/Lab/legalintelligence/ECOSYSTEM.md` is the cross-repo spec. Tier names, seat caps, form schemas, endpoint contracts, hardware-page URLs, and JWT claim names come from there. In any conflict between this repo's CLAUDE.md and ECOSYSTEM.md, ECOSYSTEM.md wins. Updates to ECOSYSTEM.md are tracked in the Plane `LEGALINT` project.
