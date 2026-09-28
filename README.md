# pm-skills

Portable project-management skills for AI agents, split out of
[Kaibernetic](https://kaibernetic.ai)'s embedded guidance. The skills carry
the opinionated "how to work" layer (session orientation, task pickup,
progress logging, spin-off capture, session close); the tracker underneath is
pluggable via backend adapter docs.

**Status: public, in daily use.** Backend is Linear (since 2026-09-02).
Kaibernetic, the hosted product these came out of, retired its service in
September 2026; its adapter stays here as a reference implementation.

**What you do yourself:** ask for `pm-orient` to check back in, and ask to
close out (`pm-close`, or `close-session` for close plus a re-orient and an
eval) when you stop. Pickup, logging and capture happen as the agent works.

## Layout

```
PRINCIPLES.md          The why: desiderata, design principles, operations vocabulary
STYLE.md               How tracker text reads: summary first, appendix after, plain sentences
skills/
  pm-orient/           Situational awareness + attention routing (the check-in)
  pm-pickup/           Start work on a task without going in blind
  pm-log/              Progress logging that makes work resumable
  pm-capture/          New tasks & spin-offs that actually resurface
  pm-close/            Session close: truthful state + named next step
  pm-init/             Consultative elicitation for new/fuzzy projects
  pm-plan/             Plan drafting (eval-tuned ES + expansions format)
  pm-horizons/         AI capability-horizon reference + defer/automate framework
  pm-tune/             Revise this system's own spec when practice diverges from it
  pm-setup/            Install/repair the system on a machine: skills visible everywhere,
                       backend MCP registered + authenticated, adapter matched to reality
  pm-hud/              The pinned always-on-top window that displays the latest orient read
  close-session/       Session close: pm-close, then pm-orient, then the desiderata eval
                       (compact mode = persist only, before context compaction)
backends/
  ACTIVE.md            Pointer: which backend is live, plus the conventions that hold for any
                       workspace; identifying details go in the gitignored ACTIVE.local.md
  kaibernetic.md       Operations → Kaibernetic MCP tools (reference; the service is retired)
  linear.md            Operations → Linear MCP / GraphQL
scripts/
  migrate_kaibernetic_to_linear.py   Active-slice migration (dry-run by default)
  linear_apply_plan.py               Apply a reconciliation plan (GraphQL fallback, dry-run default)
  pm_hud.py                          Always-on-top renderer for ~/.config/pm/hud.json (stdlib, no network)
data/                  Local scratch (gitignored)
```

## Design

Skills **prescribe** (opinionated, editable, results-oriented); backend docs
**describe** (neutral tool mappings). Each skill states the result it must
produce and anchors it in the desiderata in `PRINCIPLES.md`; the concrete tool
calls come from whichever adapter `backends/ACTIVE.md` points at. Swapping
trackers means swapping one pointer, not rewriting the way you work.

## Install (Claude Code)

Simplest: paste this repository's link into your assistant and ask it to set
the skills up. It will follow `pm-setup`.

By hand, symlink the skills into your user-level skills directory:

```bash
for s in ~/Dev/pm-skills/skills/*; do ln -sfn "$s" ~/.claude/skills/$(basename "$s"); done
```

The skills reference this repo at `~/Dev/pm-skills`; adjust paths in
`skills/*/SKILL.md` if you clone elsewhere.

Or just invoke **`pm-setup`**, which does the symlinking, registers and
authenticates the backend MCP server, and verifies the adapter against a live
read instead of assuming it.

## Provenance

Extracted from Kaibernetic's SETUP_SYSTEM_INSTRUCTIONS, MCP tool guidance, and
the Workflow Experience initiative's desiderata — recast from step-prescriptive
checklists into results contracts. See `PRINCIPLES.md` for the philosophy.

## License

MIT. See `LICENSE`.
