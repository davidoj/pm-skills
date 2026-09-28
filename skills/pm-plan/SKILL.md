---
name: pm-plan
description: Draft (or refine) a project plan after elicitation — executive summary + expansions format, base-rate and capacity honesty, information-value sequencing. Use when enough context exists to plan, when refining an existing plan, or when converting a plan into tracker structure.
---

# pm-plan — draft a plan worth following

**Serves:** Forward Momentum, Truthful State (`PRINCIPLES.md`) — a plan with
honest base rates, capacity math, and checkpoints is one reality can't
quietly diverge from.

## The result you're producing

1. **A two-layer plan**: a standalone ~1-page Executive Summary (obstacles
   first, base-rate + strategy mode, working vision, plan-at-a-glance,
   causal theory, pre-mortem, first week) plus named expansions on request.
2. **Persisted before presented**: the full plan lands on a durable node in
   the active backend (`revise_context` on the project root or relevant
   parent) *before* the ES is shown — interrupted conversations must not
   lose the plan.
3. **Sequenced by information value**: cheapest learning that could
   invalidate later steps comes first; horizon-aware automate/defer calls
   per step (see `pm-horizons`).
4. **Convertible**: step format aligns with task creation (`pm-capture`),
   so approved sections become tracker items without rework.
5. **Readable**: section format comes from `drafting.md` (eval-tuned); the
   sentences inside it follow `~/Dev/pm-skills/STYLE.md`.

The full spec — synthesis prompt, exact section names, capacity modeling,
epistemic-honesty norms, verification checklists, improvement operators,
PM-defaults setup, timeline-estimation protocol — is in
[`drafting.md`](drafting.md). Read it before drafting; it is the skill.

## Backend vocabulary mapping

`drafting.md` is written in Kaibernetic terms. Map via the active adapter
(`~/Dev/pm-skills/backends/ACTIVE.md`):
- `context_md` on a node → the canonical context doc (`revise_context`)
- `global_context` / inheritable policies → the backend's inherited-context
  mechanism (Kaibernetic: `global_context`; Linear: team/project docs +
  labels — see adapter)
- `show_recent_work` / velocity queries → recent-completions data via
  `orient()` or the adapter's analytics path
- "convert to Kaibernetic goals" → `create(item)` per `pm-capture`

## Provenance

Ported near-verbatim from Kaibernetic's `SETUP_NEW_PROJECT_DRAFTING.md` —
this is the eval-tuned production drafting prompt (v3* lineage). It was
deliberately NOT rewritten into results-contract style: the format and
phrasing carry tuned value. Edit with care and ideally re-eval. The
capability-horizons reference was split out to `pm-horizons`; the
Kaibernetic-product "Post-Plan Onboarding" section (MCP setup instructions)
was dropped as product-specific.
