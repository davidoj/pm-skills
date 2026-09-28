---
name: pm-tune
description: Revise the PM system's own spec — backend conventions, adapter mappings, skill prescriptions — when documented practice diverges from actual practice. Use when friction recurs, a workaround gets used twice, a policy gap surfaces, or after switching backends.
---

# pm-tune — keep the spec matching the practice

**Serves:** every desideratum, one level up. The problem statement in
`PRINCIPLES.md` applies to the system's own configuration: conventions saved
without strategy and never maintained become a spec that reads authoritative
while describing a workflow nobody actually follows.

## Why this moment matters

Every workaround is a fork between documented and actual practice. Leave it
unrecorded and the next session inherits the documented version, hits the
same friction, and forks again — or worse, half the sessions follow the doc
and half follow the workaround, and Parallel Coherence dies at the meta
level. A spec that's cheap to revise only pays off if revising it is a
practiced move, not an event.

## The result you're producing

1. **The divergence is named concretely.** What happened, how often, and
   which layer it implicates — not "the workflow feels off."
2. **The fix lands at the cheapest layer that actually resolves it:**
   - workspace specifics → `backends/ACTIVE.md`
   - operation mappings / conventions → `backends/<backend>.md`
   - prescriptions → `skills/*/SKILL.md`
   - invariants → `PRINCIPLES.md` — highest bar; changing a desideratum is
     a strategy call, confirm with the user before touching it.
3. **Product feedback is routed out, not absorbed.** If the friction is a
   defect or limitation of the backend *product* (a broken tool, a missing
   API) rather than of your conventions, file it in that product's own
   tracker. Contorting the spec around a bug without recording the bug
   hides the bug.
4. **The change is committed with its rationale.** This repo's git history
   is the spec's decision log: the commit message says what practice
   diverged and why the new text matches reality. Push, so other machines
   and sessions inherit it.
5. **Recurrence gets promoted.** The second time you patch an instance of
   something, fix the spec instead. Systemic over one-off — always.

## Judgment guidance

- **Tune at boundaries, not mid-flow.** One-off annoyance mid-task: note it
  (`pm-log`) and keep working; revise at close or in a deliberate pass.
  Minimal-hot-path-overhead applies doubly to meta-work.
- **Expect a burst after a backend switch.** An adapter written from API
  docs gets corrected by practice. Schedule one deliberate tuning pass
  after the first week rather than drip-editing per session.
- **Eval-tuned artifacts are measured prose.** `pm-plan/drafting.md` and
  `pm-init/elicitation.md` carry tuned value — revise mechanics freely, but
  stylistic rewrites need a re-eval plan (see their provenance notes).
- **A surprising spec change is itself a Truthful State violation.** If a
  revision changes behavior other sessions rely on, leave a line where
  they'll see it (adapter changelog note, README), not just a commit.

## Backend

None — this skill edits the repo itself (`~/Dev/pm-skills`), then commits
and pushes. Product-defect spin-offs go through `pm-capture` against the
relevant product's tracker.
