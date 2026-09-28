---
name: pm-orient
description: Situational awareness across all tracked work — what needs the user, what's moving, what's going stale. Use at session start, after a break, or whenever the user asks "where are we / what's next / check in".
---

# pm-orient — the check-in

**Serves:** Attention Routing, Truthful State, Flow Continuity (`PRINCIPLES.md`).

## Why this moment matters

Cold starts are expensive: without a deliberate check-in, it takes a dozen
messages of the user narrating state before work can begin. And unrouted
attention is how things die — the ask sitting on a task nobody looks at, the
in-flight work quietly going stale. One good orientation read fixes both.

## The result you're producing

After your check-in, the user knows — in a single read, without asking
follow-ups:

1. **What needs them.** Every outstanding ask flagged to the user, verbatim,
   always expanded. This section is never summarized away.
2. **What's moving.** In-flight work, freshest first. Healthy items get one
   line each; this is the section you compress.
3. **What's going stale.** In-flight items with no recent activity, expanded
   with enough context to act on — and a question, not an assumption:
   stale often means "user paused it deliberately," so ask, don't autopsy.
4. **What just finished** and **what the current priorities are** — enough to
   confirm the in-flight set actually serves the stated priorities, and to
   say so if it doesn't.

Open with a one-line summary before any sections ("2 need you · 6 in flight ·
3 going stale") so the user can decide how much to read.

## Judgment guidance

- **Compress green, expand red.** Freshness heuristic: healthy ≤3 days since
  last activity, aging 3–7, stale beyond. The failure mode is the
  fifty-item wall — a dashboard nobody reads routes no attention at all.
- **Cross-check against reality where you can.** If you're in a repo, recent
  commits/PRs are ground truth the tracker may lag: reconcile, and flag
  discrepancies ("this says in-progress but the PR merged Tuesday") rather
  than repeating them. A dashboard that lies is worse than none.
- **End with a recommendation.** Orientation without a proposed next action
  is a status report, not a check-in. Name the one or two things you'd do
  next and why.

## Leave the read on screen

If `~/.config/pm/hud.json` exists, the user is running the pinned HUD — update
it as the last step of the check-in, using the schema in `pm-hud`. The headline
and the closing recommendation you just produced are exactly its `headline` and
`next` fields, so this costs one file write, not a second analysis.

Set `generated_at` to now **only because you just read the tracker**. If you are
answering from earlier context without a fresh read, leave the file alone: a
stale read that looks stale is worth more than a fresh-looking one that isn't.

## Backend

Read `~/Dev/pm-skills/backends/ACTIVE.md`, then use the active adapter's
`orient()` mapping. If the backend offers a prebuilt dashboard call, prefer
it; otherwise assemble from the adapter's query recipes.
